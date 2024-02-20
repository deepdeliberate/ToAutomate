import bpy

from . import operators
from bpy.props import IntProperty, BoolProperty, StringProperty

class OBJECT_PT_3DView_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "To Automate Panel"
    bl_idname = "to_automate_3D_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"

    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        row.label(text = "To Automate Art Process")
        box = layout.box()
        col = box.column()

        col.prop(tamt, 'low_suffix', text = "Low Suffix", expand= True)
        col.prop(tamt, 'high_suffix' , text = "High Suffix", expand  = False)
        col.operator(operators.OBJECT_OT_TAMT_rename.bl_idname, text = "Rename")
        
        col.label(text = "Collection Names")
        row1 = col.row()
        row2 = col.row()
        row1.prop(tamt, 'move_LP', text = "LP Collection")
        row1.prop(tamt, 'col_LP', text = "", expand= False)
        row2.prop(tamt, 'move_HP', text= "HP Collection")
        row2.prop(tamt, 'col_HP', text = "", expand=False)

def register_classes():
    bpy.utils.register_class(OBJECT_PT_3DView_panel)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_3DView_panel)

