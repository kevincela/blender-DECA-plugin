import bpy
import sys
import os
from math import radians

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class DECAMeshCreator(bpy.types.Operator):
    bl_idname = "mesh.add_object_deca"
    bl_label = "Add mesh from image"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

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

        imagedata = datasets.TestData(self.filepath, device=device, iscrop=True, face_detector='fan')
        name = imagedata[0]['imagename']
        images = imagedata[0]['image'].to(device)[None,...]
        codedict = deca.encode(images)
        opdict, _ = deca.decode(codedict)

        mesh = bpy.data.meshes.new("DECAmesh")
        obj = bpy.data.objects.new(mesh.name, mesh)
        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        dense_vertices, detail_faces = deca.get_detail_mesh(opdict)
        dense_vertices_arr = dense_vertices.tolist()
        detail_faces_arr = detail_faces.tolist()
        mesh.from_pydata(dense_vertices_arr, [], detail_faces_arr)
        obj.rotation_euler = (radians(90), 0, 0)

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(
        DECAMeshCreator.bl_idname,
        text="Add face mesh using DECA",
        icon='PLUGIN')