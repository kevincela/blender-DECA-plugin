import bpy
import sys
import subprocess
import os
import importlib
from collections import namedtuple

bl_info = {
    "name": "DECA",
    "author": "Kevin Cela, Francesco Gaudeni, Michele Marchetti",
    "description": "Addon which makes use of DECA to reconstruct face meshes from images",
    "blender": (2, 90, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}

from .DECAMeshCreator import DECAMeshCreator
from .DECAAnimCreator import DECAAnimCreator
from .DECAPluginPanel import DecaPluginPanel
from .DECAAddonPreferences import DECAAddonPreferences

Dependency = namedtuple("Dependency", ["module", "package", "version"])
dependencies = [
    Dependency(module="torch", package=None, version="1.7.1"),
    Dependency(module="torchvision", package=None, version="0.8.2"),
    Dependency(module="face_alignment", package="face-alignment", version=None),
    Dependency(module="scipy", package=None, version=None),
    Dependency(module="chumpy", package=None, version=None),
    Dependency(module="skimage", package="scikit-image", version=None),
    Dependency(module="yaml", package="PyYAML", version=None),
    Dependency(module="cv2", package="opencv-python", version=None),
    Dependency(module="pytorch3d", package=None, version=None),
]
dependencies_installed = False

def install_pip():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools"], check=True)

def import_module(module_name):
    importlib.import_module(module_name)

def install_module(module_name, package_name=None, version=None):
    if package_name is None:
        package_name = module_name

    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    if package_name == "pytorch3d" and sys.platform == "linux":
        import torch
        version_str="".join([
            f"py3{sys.version_info.minor}_cu",
            torch.version.cuda.replace(".",""),
            f"_pyt{torch.__version__[0:5:2]}"
        ])
        subprocess.run([sys.executable, "-m", "pip", "install", "pytorch3d", "-f", f"https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/{version_str}/download.html"], check=True, env=environ_copy)
    else:
        if version is not None:
            package_name = package_name + "==" + version
        print(package_name)
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, env=environ_copy)

class DECA_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "deca.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def execute(self, context):
        if sys.platform == "windows":
            self.report({"ERROR"}, "Feature not supported for Windows, use the README to install the dependencies!")
            return {"CANCELLED"}
        try:
            install_pip()
            for dependency in dependencies:
                install_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          version=dependency.version)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        for cls in classes:
            bpy.utils.register_class(cls)

        return {"FINISHED"}

init_classes = [DECAAddonPreferences, DECA_OT_install_dependencies]
classes = [DECAAnimCreator, DECAMeshCreator, DecaPluginPanel]

def register():
    global dependencies_installed
    dependencies_installed = False
    
    for cl in init_classes:
        bpy.utils.register_class(cl)

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module)

        dependencies_installed = True
    except ModuleNotFoundError:
        return

    for cl in classes:
        bpy.utils.register_class(cl)


def unregister():
    for cl in init_classes:
        bpy.utils.unregister_class(cl)
    
    if dependencies_installed:
        for cl in classes:
            bpy.utils.unregister_class(cl)


if __name__ == "__main__":
    register()
