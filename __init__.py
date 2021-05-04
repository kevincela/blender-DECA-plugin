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

from .DECAMeshCreator import DECAMeshCreator
from .DECAAnimCreator import DECAAnimCreator
from .DECAPluginPanel import DecaPluginPanel
from .DECAAddonPreferences import DECAAddonPreferences

def register():
    bpy.utils.register_class(DECAMeshCreator)
    bpy.utils.register_class(DECAAnimCreator)
    bpy.utils.register_class(DecaPluginPanel)
    bpy.utils.register_class(DECAAddonPreferences)


def unregister():
    bpy.utils.unregister_class(DECAMeshCreator)
    bpy.utils.unregister_class(DECAAnimCreator)
    bpy.utils.unregister_class(DecaPluginPanel)
    bpy.utils.unregister_class(DECAAddonPreferences)


if __name__ == "__main__":
    register()
