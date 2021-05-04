import bpy
import torch
import sys
import os
from math import radians
from .decalib.deca import DECA
from .decalib.datasets import datasets
from .decalib.utils import util
from .decalib.utils.config import cfg as deca_cfg

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class DECAAnimCreator(bpy.types.Operator):
    bl_idname = "mesh.add_anim_deca"
    bl_label = "Add animation from folder"

    directory: bpy.props.StringProperty(name="Folder", description="Folder to use for DECA", subtype="DIR_PATH")

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        if addon_prefs.use_cuda:
            device = 'cuda'
        else:
            device = 'cpu'

        deca_cfg.model.use_tex = False
        deca = DECA(config = deca_cfg, device=device)

        imagedata = datasets.TestData(self.directory, device=device, iscrop=True, face_detector='fan')

        for i in range(len(imagedata)):
            print("Processing image n " + str(i))
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
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            dense_vertices, detail_faces = deca.get_detail_mesh(opdict)
            dense_vertices_arr = dense_vertices.tolist()
            detail_faces_arr = detail_faces.tolist()
            mesh.from_pydata(dense_vertices_arr, [], detail_faces_arr)
            obj.rotation_euler = (radians(90), 0, 0)

            ## AGGIUNGERE ANIMAZIONE

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}