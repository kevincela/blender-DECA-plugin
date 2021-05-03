import bpy
import torch
import sys
import os
from .decalib.deca import DECA
from .decalib.datasets import datasets
from .decalib.utils import util
from .decalib.utils.config import cfg as deca_cfg

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class DECAMeshCreator(bpy.types.Operator):
    bl_idname = "mesh.add_object_deca"
    bl_label = "Add image to generate a face mesh with DECA"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        device = 'cpu'

        deca_cfg.model.use_tex = False
        deca = DECA(config = deca_cfg, device=device)

        imagedata = datasets.TestData(self.filepath, iscrop=True, face_detector='fan')
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

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(
        DECAMeshCreator.bl_idname,
        text="Add face mesh using DECA",
        icon='PLUGIN')