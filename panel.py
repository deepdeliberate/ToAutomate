import bpy

from . import operators
from bpy.props import IntProperty, BoolProperty, StringProperty

class TAMTOBJECT_PT_3DView_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "To Automate Panel"
    bl_idname = "TO_AUTOMATE_PT_3D_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"

    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        row.label(text = "3D Object Operators")
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
        box4 = layout.box()
        box3.label(text = "Collection Organizer", icon = "OUTLINER_COLLECTION")
        r1 = box3.column()
        row1 = box3.row()
        r1.prop(tamt, "ORG_p_col", text = "Source", icon="OUTLINER_COLLECTION")
        row1.prop(tamt, "ORG_option", text="Parent?")
        if tamt.ORG_option:
            row1.prop(tamt, "ORG_name", text="Name", icon="PARTICLES")

        box3.operator(operators.OBJECT_OT_TAMT_COLORGANIZE.bl_idname, text = "Organize")

        box4.label(text="Collection De-Organizer", icon="OUTLINER_COLLECTION")
        row2 = box4.row()
        row3 = box4.row()
        row2.prop(tamt, "DORG_obj", text="Parent Object", icon="PARTICLES")
        row3.prop(tamt, "DORG_option", text="Root Col?")
        if tamt.DORG_option:
            row3.prop(tamt, "DORG_name", text = "Name", icon="OUTLINER_COLLECTION")
        box4.prop(tamt,"del_emp", text="Delete Empties?")
        box4.operator(operators.OBJECT_OT_TAMT_COL_REORGANIZE.bl_idname, text = "Reset Collections")

class TAMT_PT_MeshOperators_panel(bpy.types.Panel):
    """ Mesh Ops Panel"""
    bl_label = "Mesh Operators"
    bl_idname = "TO_AUTOMATE_PT_MESH_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"
    # bl_parent_id = "to_automate.3D_panel"

    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
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

        mat_box = main_box.box()
        col = mat_box.column()
        col.label(text = 'MATERIALS MENU')
        row1 = col.row()
        row1.prop(tamt, "base_mat", text = "Material")
        row1.prop(tamt, "rem_old_mat", text = "Del Old")
        col = col.column()
        row3 = col.row()
        row4 = col.row()
        col.operator(operators.OBJECT_OT_TAMT_MESH_ADDMAT.bl_idname, text="Add Material")
        col.operator(operators.OBJECT_OT_TAMT_MESH_REMMATS.bl_idname, text="Del Materials")
        col.operator(operators.OBJECT_OT_TAMT_MESH_CLEANMATS.bl_idname, text = "Clean UP")

    
class TAMT_PT_UVOperators_panel(bpy.types.Panel):
    """ UV Panel"""
    bl_label = "UV Operators"
    bl_idname = "TO_AUTOMATE_PT_UV_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"

    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        mbox = layout.box()
        col = mbox.column()

        col.label(text='UV PRE-CHECK')
        col.operator(operators.OBJECT_OT_TAMT_UV_OFFCHECK.bl_idname, text = "UV Offset")
        col.operator(operators.OBJECT_OT_TAMT_UV_OFFSET.bl_idname, text= "Add UV Offset")
        col.operator(operators.OBJECT_OT_TAMT_UV_SplitCheck.bl_idname, text = "Split-Island Check")

        help_box = layout.box()
        col2 = help_box.column()
        col2.label(text = "UV HELP MENU")
        col2.operator(operators.OBJECT_OT_TAMT_UV_MARKSHARPSEAM.bl_idname, text = "Mark Sharp Seam")
        col2.operator(operators.OBJECT_OT_TAMT_UV_MARKOUTERSEAM.bl_idname, text = "Mark Boundary Seam")

        # UVMap Create, Rename, Delete
        edit_box1 = layout.box()
        col3 = edit_box1.column()
        col3.label(text = "Create UVMap")
        col3.prop(tamt, "uvmap_name", text = "Name")
        col3.prop(tamt,"uvmap_mk_active", text="Make Active")
        col3.operator(operators.OBJECT_OT_TAMT_UV_Create.bl_idname, text = "Create UVMap")


        uv_ren_option = tamt.uvmap_ren_enum
        edit_box2 = layout.box()
        col4 = edit_box2.column()
        col4.label(text = "Rename UVMap")
        col4.prop(tamt, "uvmap_ren_enum", text = "Select")
        if uv_ren_option == 'OP1':
            col4.prop(tamt, "uvmap_ren_name", text = "UV Name", icon="UV")
        elif uv_ren_option == 'OP2':
            col4.prop(tamt, "uvmap_f_name", text ="Find", icon = "UV")
            col4.prop(tamt, "uvmap_ren_name", text = "Replace", icon= "UV")
            row1 = col4.row()
            row1.prop(tamt, "uvmap_ren_create", text = "Create")
            row1.prop(tamt,"uvmap_ren_active", text="Make Active")
        col4.operator(operators.OBJECT_OT_TAMT_UV_Rename.bl_idname, text = "Rename UVMap")
        
        uv_del_option = tamt.uvmap_del_enum
        edit_box3 = layout.box()
        col5 = edit_box3.column()
        col5.label(text = "Delete UVMap")
        col5.prop(tamt, "uvmap_del_enum", text = "Delete")
        if uv_del_option != 'OP1':
            # Delete Active UV
            col5.prop(tamt,"uvmap_del_name", text = "Name")
        col5.operator(operators.OBJECT_OT_TAMT_UV_Remove.bl_idname, text = "Delete UVMap")            

class TAMT_PT_EXPORTCOL_PANEL(bpy.types.Panel):
    """ Export Collection Panel"""
    bl_label = "Export System"
    bl_idname = "TO_AUTOMATE_PT_EXPCOL_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"

    def draw(self, context):
        tamt = context.scene.tamt
        collection = tamt.export_collection

        layout = self.layout
        row = layout.box()
        row.label(text="Collection Exporter")

        row.prop(tamt.export_presets, "selected_preset")
        row.operator(operators.OBJECT_OT_TAMT_EXPORTCOLL.bl_idname, text="EXPORT")
        row.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_CREATEPRESET.bl_idname, text = "Add Preset" )
        row.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_REMPRESET.bl_idname, text= "Delete Preset")

        if len(collection.presets) > 0:

            preset_index = int(tamt.export_presets.selected_preset)
            preset = collection.presets[preset_index]

            row.prop(preset, "name")
            row.prop(preset,"exp_meshSource", text = "Export Type", icon = "OBJECT_DATA")
            row.prop(preset, "exp_nameMethod", text = "Set File Name")
            if preset.exp_nameMethod == 'OP2':
                row.prop(preset, "exp_name")
            row.prop(preset, "exp_format", text = "Export as", icon = "EXPORT")
            if not preset.exp_inDirectory:
                row.prop(preset, "exp_meshPath")
            
            row.prop(preset, "exp_openSubstance", text = "Substance File?", icon = "BLANK1")

            exp_sepSppName = preset.exp_separateSppName
            if preset.exp_openSubstance:
                row.prop(preset,"exp_separateSppName", text = "Diff Spp Name")
                if exp_sepSppName:
                    row.prop(preset,"exp_sppName", text = "Name Spp")
                row.prop(preset, "exp_sppPath", text= "Path Spp", icon="SHADING_TEXTURE")
                row.prop(preset, "exp_sppTexPath", text= "Textures Path", icon = "TEXTURE")
            
            row.prop(preset, "exp_inDirectory", text = "Use File Directory")
            row.prop(context.scene, "exp_tngt", text = "Triangulate")
            row.prop(preset, "exp_targetKeyframe", text = "Export Frame")

            

            row = layout.row()
            row1 = row.box()

            if preset.exp_meshSource == 'OP1':
                collection_group = preset.inc_collections if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections

                
                row1.label(text = "Export Collection Selection Menu:")
                row1.prop(preset,"collection_type", expand=True)
                
                row1.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_ADDCOL.bl_idname, text = "Add Collection")
                row1.prop(preset,"collections_expanded", text="EDIT Collections", icon="NONE")
                
                if preset.collections_expanded:
                    row1.label(text="INCLUDED Collections" if preset.collection_type == 'INC_COLLECTIONS' else "EXCLUDED Collections")
                
                
                if preset.collections_expanded:
                    for i, item in enumerate(collection_group):
                        index = preset.inc_collections_index if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections_index
                        row = row1.row()
                        row.prop(item, "collection")
                        op = row.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_REMCOL.bl_idname, text = "", icon="X").index = i

        



classes = (
    TAMTOBJECT_PT_3DView_panel,
    TAMT_PT_MeshOperators_panel,
    TAMT_PT_UVOperators_panel,
    TAMT_PT_EXPORTCOL_PANEL,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)

