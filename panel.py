# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 




import bpy

from . import operators
from . import utils
from . import utils_panel
from bpy.props import IntProperty, BoolProperty, StringProperty

class TAMTOBJECT_PT_3DView_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "To Automate"
    bl_idname = "TO_AUTOMATE_PT_3D_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "To Automate"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        row.label(text = "3D Object Operators")
        box = layout.box()
        r1 = box.row(align=True)
        r2 = box.row(align=True)
        col = box.column()

        first = col.row()
        split = r1.split(factor=0.5, align=True)
        split.label(text="Low Suffix")
        split.prop(tamt, 'low_suffix', text = "", expand= True)

        s2 = r2.split(factor=0.5, align=True)
        s2.label(text="High Suffix")
        s2.prop(tamt, 'high_suffix' , text = "", expand  = False)
        col.operator(operators.OBJECT_OT_TAMT_rename.bl_idname, text = "Rename")
        

        my_rnm_ord_type = tamt.rnm_ord_type 
        col.label(text = "Object Organize Method")
        col.prop(tamt, 'rnm_ord_type', text = "Method")
        
        main_row = col.row()
        row1 = col.row().split(factor=0.3, align=True)
        row2 = col.row().split(factor=0.3, align=True)
        row_mid = col.row()
        row3 = col.row()

        if my_rnm_ord_type == 'OP1':
            row1.prop(tamt, 'move_LP', text = "LP Col")
            row2.prop(tamt, 'move_HP', text= "HP Col" )


        if my_rnm_ord_type == 'OP1':
            main_row.label(text = "Collection Names")
            row1.prop(tamt, 'col_LP', text = "", expand= False, icon = "OUTLINER_COLLECTION")
            row2.prop(tamt, 'col_HP', text = "", expand=False, icon = "OUTLINER_COLLECTION")
        

        if my_rnm_ord_type != 'OP1':
            row3.label(text="Parent Col")
            row3.prop(tamt, 'rnm_ord_parent', text = "")


# -------  Selecting Significant Other ----------------
        
        box2 = layout.box()
        box2.label(text = "Selection Menu")

        col2 = box2.row(align=True)
        col3 = box2.row(align=True)
        row4 = col2.split(factor=0.5)
        row4.label(text="Select Object")
        row4.prop(tamt, 'col_sel_enum', text = "")
        
        sel_enum = tamt.col_sel_enum
        if sel_enum == 'OP2':
            sel_row = col3.row()
            sel_row.prop(tamt,"opt_col_sel", text = "Deselect")

        col3.operator(operators.OBJECT_OT_TAMT_select.bl_idname, text = "Select")

# ------- Collection Organize/De-Organize

        box3 = layout.box()
        box4 = layout.box()
        box3.label(text = "Collection Organizer", icon = "OUTLINER_COLLECTION")

        r1 = box3.row(align=True)
        r2 = box3.row(align=True)
        r11 = r1.split(factor=0.4, align=True)
        r11.label(text="Source Col")
        r11.prop(tamt, "ORG_p_col", text = "", icon="OUTLINER_COLLECTION")
        r2.prop(tamt, "ORG_option", text="Parent?")
        if tamt.ORG_option:
            r2.prop(tamt, "ORG_name", text="", icon="PARTICLES")

        box3.operator(operators.OBJECT_OT_TAMT_COLORGANIZE.bl_idname, text = "Organize")

        box4.label(text="Collection De-Organizer", icon="OUTLINER_COLLECTION")
        r3 = box4.row()
        r4 = box4.row()
        r31 = r3.split(factor=0.4, align=True)
        r31.label(text="Parent Object")
        r31.prop(tamt, "DORG_obj", text="", icon="PARTICLES")
        r4.prop(tamt, "DORG_option", text="Root Col?")
        if tamt.DORG_option:
            r4.prop(tamt, "DORG_name", text = "", icon="OUTLINER_COLLECTION")
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
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        tamt = context.scene.tamt

        layout = self.layout
        row = layout.row(align = True)
        main_box = layout.box()
        mods = main_box.box()
        col = main_box.column()

        mods.label(text='Add Modifiers')
        mods.prop(tamt, "NewMod", text = "Create New")

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


        # Material Menu

        mat_box = main_box.box()
        col = mat_box.column()
        col.label(text = 'MATERIALS MENU')
        row1 = col.row(align=True)
        r2 = col.row(align=True)
        r1 = row1.split(factor=0.4, align=True)
        r1.label(text="Material")
        r1.prop(tamt, "base_mat", text = "")
        r2.prop(tamt, "rem_old_mat", text = "Delete Old Material")
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
    bl_options = {'DEFAULT_CLOSED'}


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
            col4.prop(tamt, "uvmap_ren_create", text = "Create")
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
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        tamt = context.scene.tamt
        collection = tamt.export_collection

        layout = self.layout
        b_row = layout.box()
        row = layout.box()


        ## Batch Export Menu
        b_row.label(text = "Batch Export Presets")

        all_presets = collection.presets

        if len(all_presets) > 0:
            col = b_row.column(align=True)
            col.label(text="PRESETS TO INCLUDE")
            head_row = col.row(align=True)
            r1 = head_row.row()
            r2 = head_row.row()
            r1.row().operator(operators.OBJECT_OT_TAMT_BatchSelectDeselectAll.bl_idname, text = "All").select_all = True
            r2.row().operator(operators.OBJECT_OT_TAMT_BatchSelectDeselectAll.bl_idname, text = "None").select_all = False
            col.separator()
            flow = col.column_flow(columns=2, align=True)
            for i,item in enumerate(all_presets):
                frow = flow.row(align=True)
                frow.prop(item, "exp_for_batch", text = f"{item.name}", icon="BLANK1")
            lrow = b_row.row(align=True)
            lrow.operator( operators.OBJECT_OT_TAMT_BATCHEXPORT.bl_idname, text = "Batch Export", icon = 'PLAY')

        else:  
            row1 = b_row.column()
            row1.label(text = "No Export Presets available", icon = 'INFO')

        row.label(text="Collection Exporter")

        r1 = row.row(align=True)
        p_icon_only = False
        if len(collection.presets) > 0:
            p_icon_only = True
        r1.prop(tamt.export_presets, "selected_preset", text="", icon="COLLAPSEMENU", icon_only=p_icon_only)
        if len(collection.presets) > 0:
            preset_index = int(tamt.export_presets.selected_preset)
            preset = collection.presets[preset_index]
            r1.prop(preset,"name", text="")
        r1.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_CREATEPRESET.bl_idname, text = "", icon = "ADD" )
        r1.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_REMPRESET.bl_idname, text= "", icon = 'REMOVE')

        row.operator(operators.OBJECT_OT_TAMT_EXPORTCOLL.bl_idname, text="EXPORT")
        
        if len(collection.presets) > 0:

            preset_index = int(tamt.export_presets.selected_preset)
            preset = collection.presets[preset_index]

            row.prop(preset,"exp_meshSource", text = "Source", icon = "OBJECT_DATA")
            row.prop(preset, "exp_nameMethod", text = "Name by")
            if preset.exp_nameMethod == 'OP2':
                row.prop(preset, "exp_name", text = "Name")
            r1 = row.row()
            r1.prop(preset, "exp_format", text = "Type", icon = "EXPORT")
            r1.operator(operators.OBJECT_OT_TAMT_EXPORT_TYPE_SETTINGS.bl_idname, text="", icon="TOOL_SETTINGS")

            if not preset.exp_inDirectory:
                row.prop(preset, "exp_meshPath", text="Path")
            
            row.prop(preset, "exp_openSubstance", text = "Substance File?", icon = "BLANK1")

            exp_sepSppName = preset.exp_separateSppName
            if preset.exp_openSubstance:
                row.prop(preset,"exp_separateSppName", text = "Diff Spp Name")
                if exp_sepSppName:
                    row.prop(preset,"exp_sppName", text = "Name Spp")
                row.prop(preset, "exp_sppPath", text= "Path Spp", icon="SHADING_TEXTURE")
                row.prop(preset, "exp_sppTexPath", text= "Textures Path", icon = "TEXTURE")
            
            option_row = row.row().split(factor=0.5, align=True)
            option_row.prop(preset, "exp_triangulate", text = "Triangulate",  icon="BLANK1")
            option_row.prop(preset, "exp_inDirectory", text = "Use File Directory")
            row.prop(preset, "exp_targetKeyframe", text = "Export Frame")
            

            if preset.exp_meshSource == 'OP1':
                row = layout.row()
                row1 = row.box()
                collection_group = preset.inc_collections if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections

                
                row1.label(text = "Export Collection Selection Menu:")
                row2 = row1.row().split(factor= 0.2, align= True)
                row2.label (text= "Target:")
                row2.prop(preset,"collection_type", expand= True)
                
                row1.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_ADDCOL.bl_idname, text = "Add Collection")
                row1.prop(preset,"collections_expanded", text="EDIT Collections", icon="BLANK1")
                
                if preset.collections_expanded:
                    row1.label(text="INCLUDED Collections" if preset.collection_type == 'INC_COLLECTIONS' else "EXCLUDED Collections")
                
                
                if preset.collections_expanded:
                    if  len (collection_group) > 0:
                        for i, item in enumerate(collection_group):
                            index = preset.inc_collections_index if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections_index
                            row = row1.row()
                            row.prop(item, "collection")
                            op = row.operator(operators.OBJECT_OT_TAMT_EXPORTCOL_REMCOL.bl_idname, text = "", icon="X").index = i
                    else:
                        row1.row().label(text = "No Collections, Add Collection to get started")

        



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

