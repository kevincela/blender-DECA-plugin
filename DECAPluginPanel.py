import bpy

class PluginPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DECA"
    bl_options = {"DEFAULT_CLOSED"}


class DecaPluginPanel(PluginPanel, bpy.types.Panel):
    bl_idname = "DECA_plugin_panel"
    bl_label = "Add face meshes and animations with DECA"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="DECA Tools")
        box.operator("mesh.add_object_deca")
        row = box.row()
        row.operator("mesh.add_anim_deca")