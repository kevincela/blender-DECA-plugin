import bpy

class DECAAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    frame_distance: bpy.props.IntProperty(
        name="Distance between frames in animation",
        default=10,
    )
    use_cuda: bpy.props.BoolProperty(
        name="Use CUDA for computation",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Preferences for the addon")
        layout.operator("deca.install_dependencies", icon="CONSOLE")