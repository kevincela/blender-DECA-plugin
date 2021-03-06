import bpy
import sys
import os
from math import radians

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class DECAAnimCreator(bpy.types.Operator):
    bl_idname = "mesh.add_anim_deca"
    bl_label = "Add animation from folder"

    directory: bpy.props.StringProperty(name="Folder", description="Folder to use for DECA", subtype="DIR_PATH")

    def execute(self, context):
        from .decalib.deca import DECA
        from .decalib.datasets import datasets
        from .decalib.utils import util
        from .decalib.utils.config import cfg as deca_cfg
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        if addon_prefs.use_cuda:
            device = 'cuda'
        else:
            device = 'cpu'

        deca_cfg.model.use_tex = False
        deca = DECA(config = deca_cfg, device=device)

        imagedata = datasets.TestData(self.directory, device=device, iscrop=True, face_detector='fan')

        face_collection = bpy.data.collections.new("Faces")
        context.scene.collection.children.link(face_collection)
        objects = []

        for i in range(len(imagedata)):
            print("Processing image n " + str(i + 1))
            name = imagedata[i]['imagename']
            images = imagedata[i]['image'].to(device)[None,...]

            if i == 0:
                codedict = deca.encode(images)
            else:
                exp_codedict = deca.encode(images)
                codedict['pose'][:,3:] = exp_codedict['pose'][:,3:]
                codedict['exp'] = exp_codedict['exp']

            opdict, _ = deca.decode(codedict)

            mesh = bpy.data.meshes.new(name)
            obj = bpy.data.objects.new(mesh.name, mesh)
            face_collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            dense_vertices, detail_faces = deca.get_detail_mesh(opdict)
            dense_vertices_arr = dense_vertices.tolist()
            detail_faces_arr = detail_faces.tolist()
            mesh.from_pydata(dense_vertices_arr, [], detail_faces_arr)
            obj.rotation_euler = (radians(90), 0, 0)

            objects.append(obj)

        print("Generating animation")

        for obj in objects:
            obj.hide_viewport = False
            obj.hide_render = False

        for i in range(len(objects)-1) :
            context.view_layer.objects.active = objects[i]
            bpy.ops.object.modifier_add(type='SHRINKWRAP')
            context.object.modifiers["Shrinkwrap"].wrap_method = 'NEAREST_SURFACEPOINT'
            context.object.modifiers["Shrinkwrap"].wrap_mode = 'OUTSIDE'
            context.object.modifiers["Shrinkwrap"].target = objects[i+1]
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier="Shrinkwrap")

        countframe=0
        for (j, obj) in enumerate(objects):
            context.view_layer.objects.active = obj
            
            if j != 0: 
                obj.hide_viewport = True
                obj.hide_render = True
                obj.keyframe_insert('hide_viewport', frame= -1 )
                obj.keyframe_insert('hide_render', frame= -1 )

            obj.hide_viewport = False
            obj.hide_render = False
            obj.keyframe_insert('hide_viewport', frame=countframe)
            obj.keyframe_insert('hide_render', frame=countframe)

            if j != (len(objects) - 1):
                bpy.context.object.active_shape_key_index = 1
                shrinkwrap = obj.data.shape_keys.key_blocks["Shrinkwrap"]
                shrinkwrap.value = 0
                shrinkwrap.keyframe_insert("value", frame=countframe)
                shrinkwrap.value = 1
                countframe = countframe + addon_prefs.frame_distance
                shrinkwrap.keyframe_insert("value", frame=countframe)
                obj.hide_viewport = True
                obj.hide_render = True
                obj.keyframe_insert('hide_viewport', frame=countframe)
                obj.keyframe_insert('hide_render', frame=countframe)
            else:
                obj.keyframe_insert("location", frame=countframe)

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}