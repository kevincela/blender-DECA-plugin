import bpy

class DECAAddonPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    frame_distance: bpy.props.IntProperty(
        name="Distance between frames in animation (ms)",
        default=200,
    )
    use_cuda: bpy.props.BoolProperty(
        name="Use CUDA for computation",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Preferences for the addon")
        layout.prop(self, "frame_distance")
        layout.prop(self, "use_cuda")
        layout.operator("deca.install_dependencies", icon="CONSOLE")