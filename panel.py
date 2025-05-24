import bpy

from . import operators
from bpy.props import IntProperty, BoolProperty, StringProperty

class TAMTOBJECT_PT_3DView_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "To Automate Panel"
    bl_idname = "to_automate.3D_panel"
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
        

        my_rnm_ord_type = tamt.rnm_ord_type 
        col.label(text = "Object Organize Method")
        col.prop(tamt, 'rnm_ord_type', text = "Method")
        
        main_row = col.row()
        row1 = col.row()
        row2 = col.row()
        row_mid = col.row()
        row3 = col.row()

        if my_rnm_ord_type != 'OP3':
            main_row.label(text = "Collection Names")
            row1.prop(tamt, 'col_LP', text = "Low Col", expand= False)
            row2.prop(tamt, 'col_HP', text = "High Col", expand=False)
        
        if my_rnm_ord_type == 'OP1':
            row1.prop(tamt, 'move_LP', text = "LP Collection")
            row2.prop(tamt, 'move_HP', text= "HP Collection")

        if my_rnm_ord_type == 'OP3':
            row_mid.prop(tamt,'rnm_ord_3rd', text = "Object Col")

        if my_rnm_ord_type != 'OP1':
            row3.prop(tamt, 'rnm_ord_parent', text = "Parent Col")


# -------  Selecting Significant Other ----------------
        
        box2 = layout.box()
        col2 = box2.column()
        col2.label(text = "Selection Menu")
        col2.prop(tamt, 'col_sel_enum', text = "Select Objects")
        
        sel_enum = tamt.col_sel_enum
        if sel_enum == 'OP2':
            sel_row = col2.row()
            sel_row.prop(tamt,"opt_col_sel", text = "Deselect Original Objects")

        col2.operator(operators.OBJECT_OT_TAMT_select.bl_idname, text = "Select")

# ------- Collection Organize/De-Organize

        box3 = layout.box()
        box3.label(text = "Collection Organizer", icon = "OUTLINER_COLLECTION")
        row1 = box3.row()
        row1.prop(tamt, "ORG_option", text="Parent?", icon="BLANK1")
        row1.prop(tamt, "ORG_name", text="Name", icon="PARTICLES")
        box3.operator(operators.OBJECT_OT_TAMT_COLORGANIZE.bl_idname, text = "Organize")

        box3.label(text="Collection De-Organizer", icon="OUTLINER_COLLECTION")
        row2 = box3.row()
        row2.prop(tamt, "DORG_option", text="Root Col?", icon="BLANK1")
        row2.prop(tamt, "DORG_name", text = "Name", icon="OUTLINER_COLLECTION")
        box3.prop(tamt,"del_emp", text="Delete Empties?")
        box3.operator(operators.OBJECT_OT_TAMT_COL_REORGANIZE.bl_idname, text = "Reset Collections")

class TAMT_PT_MeshOperators_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "Mesh Operators"
    bl_idname = "to_automate.Mesh_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"
    # bl_parent_id = "to_automate.3D_panel"

    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        row.label(text = "Mesh Operations")
        main_box = layout.box()
        mods = main_box.box()
        col = main_box.column()

        mods.label(text='Add Modifiers')
        mods.prop(tamt, "NewMod", text = "CREATE New")

        mods.prop(tamt, "sym_obj_name", text = "Mir Obj")

        row = col.row()
        col1 = row.column()
        col1.operator(operators.OBJECT_OT_TAMT_MOD_TRIANGULATE.bl_idname, text="TRIANGULATE", icon="MOD_TRIANGULATE")
        col1.operator(operators.OBJECT_OT_TAMT_MOD_MIRROR.bl_idname, text = "MIRROR", icon="MOD_MIRROR")
        col1.operator(operators.OBJECT_OT_TAMT_MOD_ARRAY.bl_idname, text = "Dynamic Array", icon="MOD_ARRAY")
        col1.operator(operators.OBJECT_OT_TAMT_MOD_WGHTNRM.bl_idname, text = "Weighted Normal", icon="MOD_NORMALEDIT")

        col1.prop(tamt, "shift_uv", text="SHIFT UV", icon="BLANK1")

        row1 = col.column()
        row2 = row1.row()
        if tamt.shift_uv:
            row2.prop(tamt,"shift_uvu", text="U")
            row2.prop(tamt,"shift_uvv", text="V")







classes = (
    TAMTOBJECT_PT_3DView_panel,
    TAMT_PT_MeshOperators_panel,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)

