import bpy

class PluginPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DECA"

class DecaPluginPanel(PluginPanel, bpy.types.Panel):
    bl_idname = "DECA_PT_plugin_panel"
    bl_label = "Add face meshes and animations with DECA"

    def draw(self, context):
        layout = self.layout
        addon_prefs = context.preferences.addons[__package__].preferences
        box = layout.box()
        box.label(text="DECA Tools")
        box.operator("mesh.add_object_deca")
        row = box.row()
        row.operator("mesh.add_anim_deca")
        box_pref = layout.box()
        box_pref.label(text="Preferences plugin")
        box_pref.prop(addon_prefs, "frame_distance")
        box_pref.prop(addon_prefs, "use_cuda")
        