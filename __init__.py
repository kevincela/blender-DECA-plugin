import bpy
import sys

bl_info = {
    "name": "DECA",
    "author": "KC, FG, MM",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}

from .DECAMeshCreator import DECAMeshCreator, menu_func
# sys.path.append('/home/kevincela/.local/lib/python3.9/site-packages')
# sys.path.append('/usr/local/lib/python3.9/site-packages')
# VEDERE FLAG --python-use-system-env


def register():
    bpy.utils.register_class(DECAMeshCreator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(DECAMeshCreator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


if __name__ == "__main__":
    register()
