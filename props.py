import bpy

from . import utils
from bpy.props import PointerProperty



class CollectionItem(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(
        name = "Collection",
        type = bpy.types.Collection,
    )

class exportPresetActive(bpy.types.PropertyGroup):
    selected_preset: bpy.props.EnumProperty(name = "Preset", items =  utils.update_presets )

class fbxExportProperties(bpy.types.PropertyGroup):
    object_types: bpy.props.EnumProperty(
        name="Object Types",
        description="Object Types to Export",
        options={'ENUM+FLAG'},
        items=[
            ('ARMATURE', "Armature", ""),
            ('CAMERA', "Camera", ""),
            ('EMPTY', "Empty", ""),
            ('LIGHT', "Light", ""),
            ('MESH', "Mesh", ""),
            ('OTHER', "Other", ""),
        ],
        default = {'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}
    )

    use_custom_props: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Use Custom Prpoerties",
        default=False,
    )


    # -------------------------------  Transform ------------------------------------------------------




    global_scale: bpy.props.FloatProperty(name="Scale", description="Scale all data (Some importers do not support scaled armatures!)", default=1.0, min=0.001, max=1000)

    apply_unit_scale: bpy.props.BoolProperty(
        name="Apply Unit Scale",
        description="Apply Unit Scale",
        default=True,
    )

    apply_scale_options: bpy.props.EnumProperty(
        name="Scale",
        description="Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way)"
        items=[
            ('FBX_SCALE_NONE', "All Local", "Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0"),
            ('FBX_SCALE_UNITS', "FBX Units Scale", "Apply custom scaling to each object transformation, and units scaling to FBX scale"),
            ('FBX_SCALE_CUSTOM', "FBX Custom Scale", "Apply custom scaling to FBX scale, and units scaling to each object transformation")
            ('FBX_SCALE_ALL', "FBX All", "Apply custom scaling and units scaling to FBX scale"),
        ],
        default='FBX_SCALE_NONE'
    )

    use_space_transform: bpy.props.BoolProperty(
        name="Use Space Transform",
        description="Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is",
        default= True,
    )

    bake_space_transform: bpy.props.BoolProperty(
        name= "Apply Transform",
        description="Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)"
    )

    axis_forward: bpy.props.EnumProperty(
        name="Forward",
        items=[
            ('X', "X Forward", ""),
            ('Y', "Y Forward", ""),
            ('Z', "Z Forward", ""),
            ('-X', "-X Forward", ""),
            ('-Y', "-Y Forward", ""),
            ('-Z', "-Z Forward", ""),
        ],
        default= = '-Z',
    )

    axis_up: bpy.props.EnumProperty(
        name="UP",
        items=[
            ('X',"X Up", ""),
            ('Y',"Y Up", ""),
            ('Z',"Z Up", ""),
            ('-X',"-X Up", ""),
            ('-Y',"-Y Up", ""),
            ('-Z',"-Z Up", ""),
        ],
        default='Y',
    )


    # -------------------------------  Geometry ------------------------------------------------------


    use_mesh_modifiers: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to mesh objects (except Armature ones) - WARNING: prevents exporting shape keys",
        default=True,
    )

    mesh_smooth_type: bpy.props.EnumProperty(
        name="Smoothing",
        description="Export smoothing information (prefer ‘Normals Only’ option if your target importer understand split normals)",
        items=[
            ('OFF',"Normals Only", "Export only normals instead of writing edge or face smoothing data"),
            ('FACE',"Face", "Write face smoothing"),
            ('EDGE',"Edge", "Write Edge smoothing"),
        ],
        default='OFF',
    )

    colors_type: bpy.props.EnumProperty(
        name="Vertex Colors",
        description="Export vertex color attributes",
        items=[
            ('NONE', "None", "Do not export color attributes"),
            ('SRGB', "sRGB", "Export colors in sRGB color space"),
            ('LINEAR', "Linear", "Export colors in linear color space"),
        ],
        default='SRGB',
    )

    prioritize_active_color: bpy.props.BoolProperty(
        name="Prioritize Active Color", 
        description="Make sure active color will be exported first. Could be important since some other software can discard other color attributes besides the first one",
        default= False,
    )

    use_subsurf: bpy.props.BoolProperty(
        name="Export Subdivision Surface",
        description="Export the last Catmull-Rom subdivision modifier as FBX subdivision (does not apply the modifier even if ‘Apply Modifiers’ is enabled)",
        default=False,
    )

    use_mesh_edges: bpy.props.BoolProperty(
        name="Loose Edges",
        description="Export loose edges (as two-vertices polygons)",
        default=False,
    )
    use_tspace: bpy.props.BoolProperty(
        name="Tangent Space",
        description="Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!)",
        default=False,
    )
    use_triangles: bpy.props.BoolProperty(
        name="Triangulate Faces",
        description="Convert all faces to triangles",
        default=False,
    )

    # -------------------------------  Armature ------------------------------------------------------



    add_leaf_bones: bpy.props.BoolProperty(
        name="Add Leaf Bones",
        description="Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)",
        default=True,
    )

    primary_bone_axis: bpy.props.EnumProperty(
        name="Primary Bone Axis",
        items=[
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ],
        default='Y',
    )

    secondary_bone_axis: bpy.props.EnumProperty(
        name="Secondary Bone Axis",
        items=[
            ('X', "X Axis", ""),
            ('Y', "Y Axis", ""),
            ('Z', "Z Axis", ""),
            ('-X', "-X Axis", ""),
            ('-Y', "-Y Axis", ""),
            ('-Z', "-Z Axis", ""),
        ],
        default='X',
    )

    use_armature_deform_only: bpy.props.BoolProperty(
        name="Only Deform Bones",
        description="Only write deforming bones (and non-deforming ones when they have deforming children)",
        default=False,
    )

    armature_node_type: bpy.props.EnumProperty(
        name="Armature FBX Node Type",
        description="FBX type of node (object) used to represent Blender’s armatures (use the Null type unless you experience issues with the other app, as other choices may not import back perfectly into Blender…)",
        items=[
            ('NULL', "Null", "‘Null’ FBX node, similar to Blender’s Empty (default)"),
            ('ROOT', "Root", "‘Root’ FBX node, supposed to be the root of chains of bones…."),
            ('LIMBNODE',"LimbNode", "‘LimbNode’ FBX node, a regular joint between two bones…."),
        ],
        default= 'NULL',
    )


    # -------------------------------  Animation ------------------------------------------------------

    
    bake_anim: bpy.props.BoolProperty(
        name="Baked Animation",
        description = "Export baked keyframe animation",
        default=False,
    )

    bake_anim_use_all_bones: bpy.props.BoolProperty(
        name="Key All Bones",
        description = "Force exporting at least one key of animation for all bones (needed with some target applications, like UE4)",
        default=True,
    )

    bake_anim_use_nla_strips: bpy.props.BoolProperty(
        name="NLA Strips",
        description = "Export each non-muted NLA strip as a separated FBX’s AnimStack, if any, instead of global scene animation",
        default=True,
    )

    bake_anim_use_all_actions: bpy.props.BoolProperty(
        name="All Actions",
        description = "Export each action as a separated FBX’s AnimStack, instead of global scene animation (note that animated objects will get all actions compatible with them, others will get no animation at all)",
        default=True,
    )

    bake_anim_force_startend_keying: bpy.props.BoolProperty(
        name="Force Start/End Keying",
        description = "Always add a keyframe at start and end of actions for animated channels",
        default=True,
    )

    bake_anim_step: bpy.props.FloatProperty(
        name="Sampling Rate",
        description = "How often to evaluate animated values (in frames)",
        default=1.00,
        min=0.01,
        max=100,
    )
    bake_anim_simplify_factor: bpy.props.FloatProperty(
        name="Simplify",
        description = "How much to simplify baked values (0.0 to disable, the higher the more simplified)",
        default=1.00,
        min=0,
        max=100,
    )






class exportProperties(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(name="Preset Name")

    exp_nameMethod: bpy.props.EnumProperty(
        name="Choose Naming Method",
        description="Select how the export file should be named",
        items=[('OP1',"Project file name","Uses the name of blend file saved and it automatically adds corresponding suffix"),
                ('OP2',"Custom Name","Set a custom name and it automatically adds corresponding suffix")])
    
    exp_name: bpy.props.StringProperty(
        name="File name",
        description="Set the file name for the Exports",
        default="My_Export")
    
    exp_meshPath: bpy.props.StringProperty(
        name="Config Path",
        update= utils.update_mesh_path,
        description="Define the root path of the Export file",
        default="",
        subtype="DIR_PATH",
        )
    
    exp_inDirectory: bpy.props.BoolProperty(
        name="Save in same folder as .blend",
        description="Uses the same directory as of the .blend file",
        default=False)
    
    exp_meshSource: bpy.props.EnumProperty(
        name="Export Source",
        description="Select Export Method",
        items=[('OP1',"Collection Objects","Export Specific Collection, Include or Exclude Collections to Export"),
                ('OP2',"Selected Objects","Exports the selected objects only!")])
    
    exp_format : bpy.props.EnumProperty(
        name="Export File Type",
        description="Select File Extensions",
        items=[('OP1',"FBX Export","Exports the file as Project.fbx"),
                ('OP2',"OBJ Export","Export the file as Project.obj"),
                ('OP3',"USD Export", "Export as file.usdc"),
                ('OP4',"DAE Export","Export as .dae (Collada)")])
    
    exp_editPresetDetails: bpy.props.BoolProperty(
        name = "Edit Preset",
        description="Edit Properties of Preset.",
        default= False,
    )

    exp_triangulate: bpy.props.BoolProperty(
        name = 'Triangulate',
        description="Triangulate the meshes during export",
        default= True,
    )
    
    exp_openSubstance: bpy.props.BoolProperty(
        name = "Open Substance Painter",
        description="Open Substance Painter with the new exported mesh",
        default= False,
    )

    exp_separateSppName: bpy.props.BoolProperty(
        name="Different name for Spp file",
        description="Select to have different name for spp file than the export file",
        default= False,
    )

    exp_sppName: bpy.props.StringProperty(
        name="Spp File Name",
        description="Add Name for the Substance file to save as",
        default="")

    exp_sppPath: bpy.props.StringProperty(
        name="Spp file Path",
        update= utils.update_spp_path,
        description="Add location for the project.spp file to save in.",
        default="",
        subtype="DIR_PATH")
    
    exp_sppTexPath: bpy.props.StringProperty(
        name="Textures file Path",
        update= utils.update_sppTex_path,
        description="Add location for the Spp textures export files.",
        default="",
        subtype="DIR_PATH")
    
    exp_targetKeyframe: bpy.props.IntProperty(
        name= "Set Export at Frame",
        description="Select the keyframe at which to export object",
        default= 0,
    )

    exp_for_batch: bpy.props.BoolProperty(
        name="Enable in Batch Export",
        description="Enable this preset for the Batch Export",
        default= False
    )

    
    inc_collections: bpy.props.CollectionProperty(type= CollectionItem)
    inc_collections_index: bpy.props.IntProperty(name = "Collections Index", default= -1)

    exc_collections: bpy.props.CollectionProperty(type= CollectionItem)
    exc_collections_index: bpy.props.IntProperty(name = "Collections Index", default= -1)


    collections_expanded: bpy.props.BoolProperty(name="Collections Expanded",description= "Edit Collections to Include or Exclude" ,default=True)

    def get_col_type_items(self, context):
        items = [
            ('INC_COLLECTIONS', f"Include Collection ({len(self.inc_collections)})", "Select Collections to Include"),
            ('EXC_COLLECTIONS', f"Exclude Collection ({len(self.exc_collections)})", "Select Collections to Exclude")
        ]
        return items

    collection_type: bpy.props.EnumProperty(
        name = "Collection Type",
        items=get_col_type_items,
        default= 0
    )

    



class exportCollection(bpy.types.PropertyGroup):
    presets: bpy.props.CollectionProperty(type = exportProperties)




class TAMT_Addon_Props(bpy.types.PropertyGroup):
    """ Class to define all the properties of the addon"""

    #   --------------  Renamer Menu  ------------------
    
    low_suffix: bpy.props.StringProperty(
        name= "Low Suffix",
        description="Low Poly Object Suffix",
        default = "_LP",
    )
    high_suffix: bpy.props.StringProperty(
        name = "High Suffix",
        description="High Poly Suffix",
        default = "_HP",
    )

    move_HP: bpy.props.BoolProperty(
        name = "Move HPs to HP Collection",
        description = "Move the HP object into high poly collection",
        default = True,
    )
    move_LP: bpy.props.BoolProperty(
        name = "Move LPs to LP Collection",
        description = "Move the LP object into low poly collection",
        default = True,
    )

    col_HP: bpy.props.StringProperty(
        name = "High Poly Collection",
        default = "HP_Col"
    )
    col_LP: bpy.props.StringProperty(
        name = "Low Poly Collection",
        default = "LP_Col"
    )

    # Select significant other
    opt_col_sel: bpy.props.BoolProperty(
        name = "Select the Original Object",
        default = False
    )

    col_sel_enum: bpy.props.EnumProperty(
        name="",
        description= "Menu to Select Objects",
        items= [('OP1', "Non-matching objects", "Select Objects having no matching low or high objects from the collections"),
                ('OP2', "Significant Other","Select the counter high / low object for the selected objects")]
    )

    # ----------- Rename organization type ---------------------
    rnm_ord_type: bpy.props.EnumProperty(
        name = "",
        description = "Organization Method for Renaming LP & HP objects",
        items = [('OP1', "Separate Low-High","Move LP and HP to common LP and HP Collections"),
                 ('OP2', "Object Collection", "Move LP and HP objects under Object's name Collection"),
                 ]
                #  ('OP3', "Multi-Object Organize", "Organizes multiple LP and HP named objects to Object named / LP-HP Collection")
    )
    rnm_ord_3rd: bpy.props.BoolProperty(
        name = "",
        description= "Make Individual Object Collection for all objects, if off moves selected objects sorted by their suffix",
        default= False
    )

    rnm_ord_parent: bpy.props.StringProperty(
        name = "Parent Collection",
        description= "Name for Parent collection of the object collections / if empty : under Scene Collection",
        default = "P_Col"
    )

    # ------- Collection Organize/De-Organize -------------

    ORG_name: bpy.props.StringProperty(
        name="Targe Object Name",
        description="Name for the root Parent Object",
        default="ROOT"
    )

    ORG_p_col: bpy.props.PointerProperty(type = bpy.types.Collection,
                                         name="Source Collection to Organize",
                                        description="Select the Top-level collection of heirarchy to convert")

    ORG_option: bpy.props.BoolProperty(
        name="Make Master parent for final heirarchy",
        description="If enabled Makes an Top Level Object and puts the src Col objects in it",
        default=False) 
    
    DORG_name: bpy.props.StringProperty(
        name="Collection Name",
        description="Name for the root Collection",
        default="Main Collection")
    
    DORG_obj: bpy.props.PointerProperty(type = bpy.types.Object,
                                        name="Source Object to De-organize",
                                        description="Select the Top-parent object of heirarchy to convert")
        
    DORG_option: bpy.props.BoolProperty(
        name="Make Master Parent Collection",
        description="Enabled: Makes a new Parent Collection ontop of Final Root Collection",
        default=False)   
        
    del_emp: bpy.props.BoolProperty(
        name="Delete Empties?",
        description="If enabled, deletes the parent empties",
        default=True)    

    # --------- Modifier Menu -------------------
    shift_uv: bpy.props.BoolProperty(
        name="SHIFT UVs",
        description="Shift mirror part's UV along x to 1",
        default=True)
    
    shift_uvu: bpy.props.BoolProperty(
        name="SHIFT U",
        description="Shift mirror part's UV along x to 1",
        default=True)
    
    shift_uvv: bpy.props.BoolProperty(
        name="SHIFT V",
        description="Shift mirror part's UV along y to 1",
        default=False)
    
    sym_obj_name: bpy.props.StringProperty(
        name="Sym Object",
        description="Name for the symmetry Empty object",
        default="All_sym") 
    
    NewMod: bpy.props.BoolProperty(
        name="Create Modifier",
        description="Create new modifier even if already in the selected_objects, Only Mirror and Array ",
        default=True)
    
    ##   Material Menu
    base_mat: bpy.props.PointerProperty( type = bpy.types.Material)

    apply_mat: bpy.props.BoolProperty(
        name = "Apply to Object",
        description="If Enabled, the material will be applied to mesh's faces",
        default=False
    )
    
    rem_old_mat: bpy.props.BoolProperty(
        name = "Remove Materials",
        description= "Remove old materials and then Add New",
        default= False
    )

    # UVMap Menu
    # Add UV Map default name to preferences?

    uvmap_name: bpy.props.StringProperty(
        name= "UVMap Name",
        description="Name of the UVMap",
        default='UVMap' 
    )

    uvmap_mk_active: bpy.props.BoolProperty(
        name="Make UVMap Active",
        description="Make UVMap as active UVMap for work",
        default= True 
    )

    # uvmap_mk_activerender: bpy.props.BoolProperty(
    #     name="Make UVMap Active Render",
    #     description="Make Active UVMap as active Render",
    #     default= True
    # )

    uvmap_del_name: bpy.props.StringProperty(
        name = "UV Name",
        description= "New UVMap Name",
        default="UVMap"
    )

    uvmap_del_enum: bpy.props.EnumProperty(
        name = "Delete Method",
        description="Select method to delete UVs",
        items=[('OP1',"Active UV","Removes the active UV from UV stack"),
                ('OP2',"UV named","Remove UV with specific Name"),
                ('OP3',"Except Name", "Remove all UVs except the one named above")],
    )

    uvmap_ren_name: bpy.props.StringProperty(
        name = "UV Name",
        description= "UVMap Name",
        default="UVMap"
    )

    uvmap_ren_enum: bpy.props.EnumProperty(
        name = "Rename Method",
        description="Select method to delete UVs",
        items=[('OP1',"Rename Active","Renames the active UV of the object"),
                ('OP2',"Find & Rename","Search and Renames the UV")],
    )
    
    uvmap_ren_active: bpy.props.BoolProperty(
        name="Make Active",
        description = "Rename and Make active",
        default = True
    )

    uvmap_f_name: bpy.props.StringProperty(
        name= "Find UVMap named as",
        description="Find the UVMap of given name",
        default='UV_0'
    )

    uvmap_rep_name: bpy.props.StringProperty(
        name = "Replacement Name",
        description= "Replace the Found UV with this name",
        default = 'UVMap'
    )

    uvmap_ren_create: bpy.props.BoolProperty(
        name="Create UV",
        description = "Create if not found?",
        default = True
    )

    

    # Export Menu

    export_collection: bpy.props.PointerProperty(type = exportCollection)
    export_presets: bpy.props.PointerProperty(type = exportPresetActive)


    



classes = (
    CollectionItem,
    exportPresetActive,
    exportBatchPresetItem,
    exportProperties,
    exportCollection,
    TAMT_Addon_Props,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.tamt = PointerProperty(type = TAMT_Addon_Props)

def unregister_classes():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.tamt