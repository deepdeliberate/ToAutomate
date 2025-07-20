# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 





import bpy

from . import utils
from bpy.props import PointerProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty



class TAMT_CollectionItem(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(
        name = "Collection",
        type = bpy.types.Collection,
    )

class exportPresetActive(bpy.types.PropertyGroup):
    selected_preset: bpy.props.EnumProperty(name = "Preset", items =  utils.update_presets )


class TAMT_fbxExportProperties(bpy.types.PropertyGroup):
    preset_name: bpy.props.StringProperty(
        name= "FBX Preset Name",
        description= "Name for this FBX preset",
        default= 'Preset',
    )

    object_types: bpy.props.EnumProperty(
        name="Object Types",
        description="Object Types to Export",
        options={'ENUM_FLAG'},
        items=[
            ('ARMATURE', "Armature", ""),
            ('CAMERA', "Camera", ""),
            ('EMPTY', "Empty", ""),
            ('LIGHT', "Light", ""),
            ('MESH', "Mesh", ""),
            ('OTHER', "Other", ""),
        ],
        default = {'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'},
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
        description="Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way)",
        items=[
            ('FBX_SCALE_NONE', "All Local", "Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0"),
            ('FBX_SCALE_UNITS', "FBX Units Scale", "Apply custom scaling to each object transformation, and units scaling to FBX scale"),
            ('FBX_SCALE_CUSTOM', "FBX Custom Scale", "Apply custom scaling to FBX scale, and units scaling to each object transformation"),
            ('FBX_SCALE_ALL', "FBX All", "Apply custom scaling and units scaling to FBX scale"),
        ],
        default='FBX_SCALE_NONE',
    )

    use_space_transform: bpy.props.BoolProperty(
        name="Use Space Transform",
        description="Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is",
        default= True,
    )

    bake_space_transform: bpy.props.BoolProperty(
        name= "Apply Transform",
        description="Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)",
        default=False,
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
        default = '-Z',
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
        items= utils.fbx_smooth_grp_items,
        default=0,
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

    armature_nodetype: bpy.props.EnumProperty(
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

class TAMT_objExportProperties(bpy.types.PropertyGroup):
    preset_name: bpy.props.StringProperty(
        name= "OBJ Preset Name",
        description= "Name for this OBJ preset",
        default= 'Preset',
    )

    export_animation: bpy.props.BoolProperty(
        name="Export Animation",
        description="Export multiple frames instead of the current frame only",
        default=False,
    )

    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="The first frame to be exported",
        default=0,
    )

    end_frame: bpy.props.IntProperty(
        name= "End Frame",
        description= "The last frame to be exported",
        default=0,
    )

    forward_axis: bpy.props.EnumProperty(
        name= "Forward Axis",
        items=[
            ('X', "X", "Positive X axis"),
            ('Y', "Y", "Positive Y axis"),
            ('Z', "Z", "Positive Z axis"),
            ('NEGATIVE_X', "-X", "Negative X axis"),
            ('NEGATIVE_Y', "-Y", "Negative Y axis"),
            ('NEGATIVE_Z', "-Z", "Negative Z axis"),
        ],
        default= 'NEGATIVE_Z',
    )

    up_axis: bpy.props.EnumProperty(
        name= "Up Axis",
        items=[
            ('X', "X", "Positive X axis"),
            ('Y', "Y", "Positive Y axis"),
            ('Z', "Z", "Positive Z axis"),
            ('NEGATIVE_X', "-X", "Negative X axis"),
            ('NEGATIVE_Y', "-Y", "Negative Y axis"),
            ('NEGATIVE_Z', "-Z", "Negative Z axis"),
        ],
        default= 'Y',
    )


    global_scale: bpy.props.FloatProperty(
        name= "Scale",
        description= "Value by which to enlarge or shrink the objects with respect to the world's origin",
        default= 1.0,
        min=  0.0001,
        max= 10000,
    )

    apply_modifiers: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to exported meshes",
        default=False,
    )

    export_eval_mode: bpy.props.EnumProperty(
        name= "Object Properties",
        description= "Determines properties like object visibility, modifiers etc., where they differ for Render and Viewport",
        items=[
            ('DAG_EVAL_RENDER', "Render", "Export objects as they appear in render."),
            ('DAG_EVAL_VIEWPORT', "Viewport", "Export objects as they appear in the viewport"),
        ],
        default= 'DAG_EVAL_VIEWPORT',
    )

    export_selected_objects: bpy.props.BoolProperty(
        name="Export Selected Objects",
        description="Export only selected objects instead of all supported objects",
        default=False,
    )

    export_uv: bpy.props.BoolProperty(
        name="Export UVs",
        description="Export UVs of the meshes",
        default=True,
    )

    export_normals: bpy.props.BoolProperty(
        name="Export Normals",
        description="Export per-face normals if the face is flat-shaded, per-face-per-loop normals if smooth-shaded",
        default=True,
    )

    export_colors: bpy.props.BoolProperty(
        name="Export Colors",
        description="Export per-vertex colors",
        default=False,
    )

    export_materials: bpy.props.BoolProperty(
        name="Export Materials",
        description="Export MTL library. There must be a Principled-BSDF node for image textures to be exported to the MTL file",
        default=True,
    )

    export_pbr_extensions: bpy.props.BoolProperty(
        name="Export Materials with PBR Extensions",
        description="Export MTL library using PBR extensions (roughness, metallic, sheen, coat, anisotropy, transmission)",
        default=False,
    )

    path_mode: bpy.props.EnumProperty(
        name="Path Mode",
        description= "Method used to reference paths",
        items=[
            ('AUTO',"Auto", "Use relative paths with subdirectories only."),
            ('ABSOLUTE', "Absolute", "Always write absolute paths."),
            ('RELATIVE', "Relative", "Write relative paths where possible"),
            ('MATCH', "Match", "Match absolute/relative setting with input path."),
            ('STRIP', "Strip", "Write filename only."),
            ('COPY', "Copy", "Copy the file to the destination path."),
        ],
        default='AUTO',
    )

    export_triangulated_mesh: bpy.props.BoolProperty(
        name="Export Triangulated Mesh",
        description="All ngons with four or more vertices will be triangulated. Meshes in the scene will not be affected. Behaves like Triangulate Modifier with ngon-method: “Beauty”, quad-method: “Shortest Diagonal”, min vertices: 4",
        default=True,
    )

    export_curves_as_nurbs: bpy.props.BoolProperty(
        name="Export Curves as NURBS",
        description="Export curves in parametric form instead of exporting as mesh",
        default=False,
    )

    export_object_groups: bpy.props.BoolProperty(
        name="Export Object Groups",
        description="Append mesh name to object name, separated by a ‘_’",
        default=False,
    )

    export_material_groups: bpy.props.BoolProperty(
        name="Export Material Groups",
        description="Generate an OBJ group for each part of a geometry using a different material",
        default=False,
    )

    export_vertex_groups: bpy.props.BoolProperty(
        name="Export Vertex Groups",
        description="Export the name of the vertex group of a face. It is approximated by choosing the vertex group with the most members among the vertices of a face",
        default=False,
    )

    export_smooth_groups: bpy.props.BoolProperty(
        name="Export Smooth Groups",
        description="Every smooth-shaded face is assigned group “1” and every flat-shaded face “off”",
        default=False,
    )

    smooth_group_bitflags: bpy.props.BoolProperty(
        name="Generate Bitflags for Smooth Groups",
        description="",
        default=False,
    )

class TAMT_usdExportProperties(bpy.types.PropertyGroup):
    preset_name: bpy.props.StringProperty(
        name= "USD Preset Name",
        description= "Name for this USD preset",
        default= 'Preset',
    )

    visible_objects_only: bpy.props.BoolProperty(
        name="Visible Only",
        description="Only export visible objects. Invisible parents of exported objects are exported as empty transforms",
        default=False,
    )

    export_animation: bpy.props.BoolProperty(
        name="Animation",
        description="Export all frames in the render frame range, rather than only the current frame",
        default=False,
    )

    export_hair: bpy.props.BoolProperty(
        name="Hair",
        description="Export hair particle systems as USD curves",
        default=False,
    )
    
    export_uvmaps: bpy.props.BoolProperty(
        name="UV Maps",
        description="Include all mesh UV maps in the export",
        default=True,
    )

    rename_uvmaps: bpy.props.BoolProperty(
        name= "Rename UV Maps",
        description="Rename active render UV map to “st” to match USD conventions",
        default=True,
    )


    export_mesh_colors: bpy.props.BoolProperty(
        name="Color Attributes",
        description="Include mesh color attributes in the export",
        default=True,
    )


    export_normals: bpy.props.BoolProperty(
        name="Normals",
        description="Include normals of exported meshes in the export",
        default=True,
    ) 

    export_materials: bpy.props.BoolProperty(
        name="Materials",
        description="Export viewport settings of materials as USD preview materials, and export material assignments as geometry subsets",
        default=True,
    )

    export_subdivision: bpy.props.EnumProperty(
        name="Subdivision",
        description="Choose how subdivision modifiers will be mapped to the USD subdivision scheme during export",
        items=[
            ('IGNORE',"Ignore", ""),
            ('TESSELLATE',"Tessellate", ""),
            ('BEST_MATCH',"Best Match", ""),
        ],
        default='BEST_MATCH', 
    )

    export_armatures: bpy.props.BoolProperty(
        name="Armatures",
        description="Export armatures and meshes with armature modifiers as USD skeletons and skinned meshes",
        default=True,
    )

    only_deform_bones:bpy.props.BoolProperty(
        name="Only Deform Bones",
        description="Only export deform bones and their parents",
        default=False, 
    )

    export_shapekeys: bpy.props.BoolProperty(
        name="Shape Keys",
        description="Export shape keys as USD blend shapes",
        default=True,
    )

    use_instancing: bpy.props.BoolProperty(
        name = "Instancing",
        description= "Export instanced objects as references in USD rather than real objects",
        default=False,   
    )

    evaluation_mode: bpy.props.EnumProperty(
        name="Use Settings for",
        description="Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering",
        items=[
            ('RENDER',"Render", "Use Render settings for object visibility, modifier settings, etc."),
            ('VIEWPORT',"Viewport", "Use Viewport settings for object visibility, modifier settings, etc."),
        ],
        default='RENDER',
    )
    
    generate_preview_surface: bpy.props.BoolProperty(
        name="USD Preview Surface",
        description="Network, Generate an approximate USD Preview Surface shader representation of a Principled BSDF node network",
        default=True,
    )

    generate_materialx_network: bpy.props.BoolProperty(
        name="MaterialX Network",
        description="Generate a MaterialX network representation of the materials",
        default=False,
    )
    
    convert_orientation: bpy.props.BoolProperty(
        name="Convert Orientation",
        description="Convert orientation axis to a different convention to match other",
        default=False,
    ) 

    generate_preview_surface: bpy.props.BoolProperty(
    name="USD Preview Surface Network",
    description="Generate an approximate USD Preview Surface shader representation of a Principled BSDF node network",
    default=False,
)

    generate_materialx_network: bpy.props.BoolProperty(
        name="MaterialX Network",
        description="Generate a MaterialX network representation of the materials",
        default=False,
    )

    convert_orientation: bpy.props.BoolProperty(
        name="Convert Orientation",
        description="Convert orientation axis to a different convention to match other applications",
        default=False,
    )

    export_global_forward_selection: bpy.props.EnumProperty(
        name="Forward Axis",
        description="Forward Axis",
        items=[
            ('X', "X", "Positive X axis"),
            ('Y', "Y", "Positive Y axis"),
            ('Z', "Z", "Positive Z axis"),
            ('NEGATIVE_X', "-X", "Positive X axis"),
            ('NEGATIVE_Y', "-Y", "Positive X axis"),
            ('NEGATIVE_Z', "-Z", "Positive X axis"),
        ],
        default='NEGATIVE_Z',
    )

    export_global_up_selection: bpy.props.EnumProperty(
        name="Up Axis",
        description="Up Axis",
        items=[
            ('X', "X", "Positive X axis"),
            ('Y', "Y", "Positive Y axis"),
            ('Z', "Z", "Positive Z axis"),
            ('NEGATIVE_X', "-X", "Positive X axis"),
            ('NEGATIVE_Y', "-Y", "Positive X axis"),
            ('NEGATIVE_Z', "-Z", "Positive X axis"),
        ],
        default='Y',
    )

    export_textures: bpy.props.BoolProperty(
        name="Export Textures",
        description="If exporting materials, export textures referenced by material nodes to a ‘textures’ directory in the same directory as the USD file",
        default=False,
    )

    export_textures_mode: bpy.props.EnumProperty(
        name="Export Textures",
        description="Texture export method",
        items=[
            ('KEEP',"Keep", "Use original location of textures"),
            ('PRESERVE',"Preserve", "Preserve file paths of textures from already imported USD files. Export remaining textures to a ‘textures’ folder next to the USD file."),
            ('NEW',"New Path", "Export textures to a ‘textures’ folder next to the USD file"),
        ],
        default='NEW',
    )

    overwrite_textures: bpy.props.BoolProperty(
        name="Overwrite Textures",
        description="Overwrite existing files when exporting textures",
        default=False,
    )

    relative_paths: bpy.props.BoolProperty(
        name="Relative Paths",
        description="Use relative paths to reference external files (i.e. textures, volumes) in USD, otherwise use absolute paths",
        default=False,
    )

    xform_op_mode: bpy.props.EnumProperty(
        name="Xform Ops",
        description="The type of transform operators to write",
        items=[
            ('TRS', "Translate, Rotate, Scale", "Export with Translate, rotate, and scale Xform operators"),
            ('TOS', "Translate, Orient, Scale", "Export with Translate, orient quaternion, and scale Xform operators"),
            ('MAT', "Matrix", "Export matrix operator"),
        ],
        default='TRS',
    )

    # Doubtful
    root_prim_path: bpy.props.StringProperty(
        name="Root Prim",
        description="If set, add a transform primitive with the given path to the stage as the parent of all exported data",
        default='/root',
    )

    export_custom_properties: bpy.props.BoolProperty(
        name="Custom Properties",
        description="Export custom properties as USD attributes",
        default=False,
    )

    custom_properties_namespace: bpy.props.StringProperty(
        name="Namespace",
        description="If set, add the given namespace as a prefix to exported custom property names. This only applies to property names that do not already have a prefix (e.g., it would apply to name ‘bar’ but not ‘foo:bar’) and does not apply to blender object and data names which are always exported in the ‘userProperties:blender’ namespace",
        default='userProperties',
    )

    author_blender_name: bpy.props.BoolProperty(
        name="Blender Names",
        description="Author USD custom attributes containing the original Blender object and object data names",
        default=True,
    )

    convert_world_material: bpy.props.BoolProperty(
        name="World Dome Light",
        description="Convert the world material to a USD dome light. Currently works for simple materials, consisting of an environment texture connected to a background shader, with an optional vector multiply of the texture color",
        default=True,
    )

    allow_unicode: bpy.props.BoolProperty(
        name="Allow Unicode",
        description="Preserve UTF-8 encoded characters when writing USD prim and property names (requires software utilizing USD 24.03 or greater when opening the resulting files)",
        default=False,
    )

    export_meshes: bpy.props.BoolProperty(
        name="Meshes",
        description="Export all meshes",
        default=True,
    )

    export_lights: bpy.props.BoolProperty(
        name="Lights",
        description="Export all lights",
        default=True,
    )

    export_cameras: bpy.props.BoolProperty(
        name="Cameras",
        description="Export all cameras",
        default=True,
    )

    export_curves: bpy.props.BoolProperty(
        name="Curves",
        description="Export all curves",
        default=True,
    )

    export_points: bpy.props.BoolProperty(
        name="Point Clouds",
        description="Export all point clouds",
        default=True,
    )

    export_volumes: bpy.props.BoolProperty(
        name="Volumes",
        description="Export all volumes",
        default=True,
    )

    triangulate_meshes: bpy.props.BoolProperty(
        name="Triangulate Meshes",
        description="Triangulate meshes during export",
        default=True,
    )


    quad_method: bpy.props.EnumProperty(
        name="Quad Method",
        description="Method for splitting the quads into triangles",
        items = [
            ('BEAUTY', "Beauty", "Split the quads in nice triangles, slower method"),
            ('FIXED', "Fixed", "Split the quads on the first and third vertices"),
            ('FIXED_ALTERNATIVE', "Fixed Alternative", "Split the quads on the 2nd and 4th vertices"),
            ('SHORTEST_DIAGONAL', "Shortest Diagonal", "Split the quads along their shortest diagonal"),
            ('LONGEST_DIAGONAL', "Longest Diagonal", "Split the quads along their longest diagonal"),
        ],
        default='SHORTEST_DIAGONAL',
    )

    ngon_method: bpy.props.EnumProperty(
        name="Polygons",
        description="Method for splitting the quads into triangles",
        items = [
            ('BEAUTY',"Beauty","Arrange the new triangles evenly (slow)"),
            ('CLIP',"Clip","Split the polygons with an ear clipping algorithm"),
        ],
        default='BEAUTY',
    )

    usdz_downscale_size: bpy.props.EnumProperty(
        name="USDZ Custom Downscale Size",
        description="Custom size for downscaling exported textures",
        items=[
            ('KEEP', "Keep", "Keep all current texture sizes."),
            ('256', "256", "Resize to a maximum of 256 pixels."),
            ('512', "512", "Resize to a maximum of 512 pixels."),
            ('1024', "1024", "Resize to a maximum of 1024 pixels."),
            ('2048', "2048", "Resize to a maximum of 2048 pixels."),
            ('4096', "4096", "Resize to a maximum of 4096 pixels."),
            ('CUSTOM', "Custom", "Resize to a maximum of 256 pixels."),
        ],
        default='KEEP',
    )

    usdz_downscale_custom_size: bpy.props.IntProperty(
        name="USDZ Custom Downscale Size",
        description="Custom size for downscaling exported textures",
        default=128,
        min=64,
        max=16384,
    )

    merge_parent_xform: bpy.props.BoolProperty(
        name="Merge parent Xform",
        description="Merge USD primitives with their Xform parent if possible. USD does not allow nested UsdGeomGprims, intermediary Xform prims will be defined to keep the USD file valid when encountering object hierarchies.",
        default=False,
    )

    convert_scene_units: bpy.props.EnumProperty(
        name="Units",
        description="Set the USD Stage meters per unit to the chosen measurement, or a custom value",
        items=[
            ('METERS', "Meters", "Scene meters per unit to 1.0."),
            ('KILOMETERS', "Kilometers", "Scene meters per unit to 1000.0."),
            ('CENTIMETERS', "Centimeters", "Scene meters per unit to 0.01."),
            ('MILLIMETERS', "Millimeters", "Scene meters per unit to 0.001."),
            ('INCHES', "Inches", "Scene meters per unit to 0.0254."),
            ('FEET', "Feet", "Scene meters per unit to 0.3048."),
            ('YARDS', "Yards", "Scene meters per unit to 0.9144."),
            ('CUSTOM', "Custom", "Specify a custom scene meters per unit value."),
        ],
        default='METERS',
    )

    meters_per_unit: bpy.props.FloatProperty(
        name="Meters Per Unit",
        description="Custom value for meters per unit in the USD Stage",
        default=1.0,
        min= 0.0001,
        max=1000,
    )

class TAMT_daeExportProperties(bpy.types.PropertyGroup):
    preset_name: bpy.props.StringProperty(
        name= "DAE Preset Name",
        description= "Name for this DAE preset",
        default= 'Preset',
    )
    
    apply_modifiers: bpy.props.BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to exported mesh (non destructive)",
        default=True,
    )

    export_mesh_type: bpy.props.IntProperty(
        name= "Resolution",
        description="Modifier resolution for export",
        default=0,
    )

    export_mesh_type_selection: bpy.props.EnumProperty(
        name="Resolution",
        description= "Modifier resolution for export",
        items=[
            ('view', "Viewport", "Apply modifier's viewport settings"),
            ('render', "Render", "Apply modifier's render settings")
        ],
        default= 'view',
    )

    export_global_forward_selection: bpy.props.EnumProperty(
        name= "Global Forward Axis",
        description= "Global Forward axis for export",
        items= [
            ('X', "X", "Global Forward is positive X Axis"),
            ('Y', "Y", "Global Forward is positive Y Axis"),
            ('Z', "Z", "Global Forward is positive Z Axis"),
            ('-X', "-X", "Global Forward is negative X Axis"),
            ('-Y', "-Y", "Global Forward is negative Y Axis"),
            ('-Z', "-Z", "Global Forward is negative Z Axis"),
        ],
        default= 'Y',
    )

    export_global_up_selection: bpy.props.EnumProperty(
        name= "Global Up Axis",
        description= "Global Up axis for export",
        items= [
            ('X', "X", "Global Up is positive X Axis"),
            ('Y', "Y", "Global Up is positive Y Axis"),
            ('Z', "Z", "Global Up is positive Z Axis"),
            ('-X', "-X", "Global Up is negative X Axis"),
            ('-Y', "-Y", "Global Up is negative Y Axis"),
            ('-Z', "-Z", "Global Up is negative Z Axis"),
        ],
        default= 'Z',
    )

    apply_global_orientation: bpy.props.BoolProperty(
        name="Apply Global Orientation",
        description="Rotate all root objects to match the global orientation settings otherwise set the global orientation per Collada asset",
        default=False,
    )

    # selected: bpy.props.BoolProperty(
    #     name="Selection Only",
    #     description="Export only selected elements",
    #     default=False,
    # )

    # include_children: bpy.props.BoolProperty(
    #     name="Include Children",
    #     description="Export all children of selected objects (even if not selected)",
    #     default=False,
    # )

    # include_armatures: bpy.props.BoolProperty(
    #     name="Include Armatures",
    #     description="Export related armatures (even if not selected)",
    #     default=False,
    # )

    # include_shapekeys: bpy.props.BoolProperty(
    #     name="Include Shape Keys",
    #     description="Export all Shape Keys from Mesh Objects",
    #     default=False,
    # )

    deform_bones_only: bpy.props.BoolProperty(
        name="Deform Bones Only",
        description="Only export deforming bones with armatures",
        default=False,
    )

    include_animations: bpy.props.BoolProperty(
        name="Include Animations",
        description="Export animations if available (exporting animations will enforce the decomposition of node transforms into <translation> <rotation> and <scale> components)",
        default=False,
    )

    include_all_actions: bpy.props.BoolProperty(
        name="Include all Actions",
        description="Export also unassigned actions (this allows you to export entire animation libraries for your character(s))",
        default=True,
    )

    export_animation_type_selection: bpy.props.EnumProperty(
        name= "Key Type",
        description="Type for exported animations (use sample keys or Curve keys)",
        items=[
            ('sample', "Samples", "Export Sampled points guided by sampling rate"),
            ('keys', "Curves", "Export Curves (note: guided by curve keys)."),
        ],
        default= 'sample',
    )

    sampling_rate: bpy.props.IntProperty(
        name="Sampling Rate",
        description= "The distance between 2 keyframes (1 to key every frame)",
        min=1,
        default= 1,
    )

    keep_smooth_curves: bpy.props.BoolProperty(
        name="Keep Smooth curves",
        description="Export also the curve handles (if available) (this does only work when the inverse parent matrix is the unity matrix, otherwise you may end up with odd results)",
        default=False,
    )

    keep_keyframes: bpy.props.BoolProperty(
        name="Keep Keyframes",
        description="Use existing keyframes as additional sample points (this helps when you want to keep manual tweaks)",
        default=False,
    )

    keep_flat_curves: bpy.props.BoolProperty(
        name="All Keyed Curves",
        description="Export also curves which have only one key or are totally flat",
        default=False,
    )

    active_uv_only: bpy.props.BoolProperty(
        name="Only Selected UV Map",
        description="Export only the selected UV Map",
        default=False,
    )

    use_texture_copies: bpy.props.BoolProperty(
        name="Copy",
        description="Copy textures to same folder where the .dae file is exported",
        default=True,
    )

    triangulate: bpy.props.BoolProperty(
        name="Triangulate",
        description="Export polygons (quads and n-gons) as triangles",
        default=True,
    )

    use_object_instantiation: bpy.props.BoolProperty(
        name="Use Object Instances",
        description="Instantiate multiple Objects from same Data",
        default=True,
    )

    use_blender_profile: bpy.props.BoolProperty(
        name="Use Blender Profile",
        description="Export additional Blender specific information (for material, shaders, bones, etc.)",
        default=True,
    )

    sort_by_name: bpy.props.BoolProperty(
        name="Sort by Object name",
        description="Sort exported data by Object name",
        default=False,
    )

    export_object_transformation_type: bpy.props.IntProperty(
        name= "Transform",
        description= "Object Transformation type for translation, scale and rotation",
        default= 0,
    )

    export_object_transformation_type_selection: bpy.props.EnumProperty(
        name= "Transform",
        description= "Object Transformation type for translation, scale and rotation",
        items=[
            ('matrix', "Matrix", "Use <matrix> representation for exported transformations."),
            ('decomposed', "Decomposed", "Use <rotate>, <translate> and <scale> representation for exported transformations."),
        ],
        default= 'matrix',
    )

    export_animation_transformation_type: bpy.props.IntProperty(
        name= "Transform",
        description= "Transformation type for translation, scale and rotation. Note: The Animation transformation type in the Anim Tab is always equal to the Object transformation type in the Geom tab",
        default= 0,
    )

    export_animation_transformation_type_selection: bpy.props.EnumProperty(
        name= "Transform",
        description= "Transformation type for translation, scale and rotation. Note: The Animation transformation type in the Anim Tab is always equal to the Object transformation type in the Geom tab",
        items=[
            ('matrix', "Matrix", "Use <matrix> representation for exported transformations."),
            ('decomposed', "Decomposed", "Use <rotate>, <translate> and <scale> representation for exported transformations."),
        ],
        default= 'matrix',
    )

    open_sim: bpy.props.BoolProperty(
        name="Export to SL/OpenSim",
        description="Compatibility mode for Second Life, OpenSimulator and other compatible online worlds",
        default=False,
    )

    limit_precision: bpy.props.BoolProperty(
        name="Limit Precision",
        description="Reduce the precision of the exported data to 6 digits",
        default=False,
    )

    keep_bind_info: bpy.props.BoolProperty(
        name="Keep Bind Info",
        description="Store Bindpose information in custom bone properties for later use during Collada export",
        default=False,
    )

class TAMT_gltfExportProperties(bpy.types.PropertyGroup):
    preset_name: bpy.props.StringProperty(
        name= "GLTF Preset Name",
        description= "Name for this GLTF preset",
        default= 'Preset',
    )

    export_import_convert_lighting_mode: EnumProperty(
        name='Lighting Mode',
        items=(
            ('SPEC', 'Standard', 'Physically-based glTF lighting units (cd, lx, nt)'),
            ('COMPAT', 'Unitless', 'Non-physical, unitless lighting. Useful when exposure controls are not available'),
            ('RAW', 'Raw (Deprecated)', 'Blender lighting strengths with no conversion'),
        ),
        description='Optional backwards compatibility for non-standard render engines. Applies to lights',  # TODO: and emissive materials',
        default='SPEC'
    )

    gltf_export_id: StringProperty(
        name='Identifier',
        description=(
            'Identifier of caller (in case of add-on calling this exporter). '
            'Can be useful in case of Extension added by other add-ons'
        ),
        default=''
    )

    # gltfpack properties
    export_use_gltfpack: BoolProperty(
        name='Use Gltfpack',
        description='Use gltfpack to simplify the mesh and/or compress its textures',
        default=False,
    )

    export_gltfpack_tc: BoolProperty(
        name='KTX2 Compression',
        description='Convert all textures to KTX2 with BasisU supercompression',
        default=True,
    )

    export_gltfpack_tq: IntProperty(
        name='Texture Encoding Quality',
        description='Texture encoding quality',
        default=8,
        min=1,
        max=10,
    )

    export_gltfpack_si: FloatProperty(
        name='Mesh Simplification Ratio',
        description='Simplify meshes targeting triangle count ratio',
        default=1.0,
        min=0.0,
        max=1.0,
    )

    export_gltfpack_sa: BoolProperty(
        name='Aggressive Mesh Simplification',
        description='Aggressively simplify to the target ratio disregarding quality',
        default=False,
    )

    export_gltfpack_slb: BoolProperty(
        name='Lock Mesh Border Vertices',
        description='Lock border vertices during simplification to avoid gaps on connected meshes',
        default=False,
    )

    export_gltfpack_vp: IntProperty(
        name='Position Quantization',
        description='Use N-bit quantization for positions',
        default=14,
        min=1,
        max=16,
    )

    export_gltfpack_vt: IntProperty(
        name='Texture Coordinate Quantization',
        description='Use N-bit quantization for texture coordinates',
        default=12,
        min=1,
        max=16,
    )

    export_gltfpack_vn: IntProperty(
        name='Normal/Tangent Quantization',
        description='Use N-bit quantization for normals and tangents',
        default=8,
        min=1,
        max=16,
    )

    export_gltfpack_vc: IntProperty(
        name='Vertex Color Quantization',
        description='Use N-bit quantization for colors',
        default=8,
        min=1,
        max=16,
    )

    export_gltfpack_vpi: EnumProperty(
        name='Vertex Position Attributes',
        description='Type to use for vertex position attributes',
        items=(('Integer', 'Integer', 'Use integer attributes for positions'),
               ('Normalized', 'Normalized', 'Use normalized attributes for positions'),
               ('Floating-point', 'Floating-point', 'Use floating-point attributes for positions')),
        default='Integer',
    )

    export_gltfpack_noq: BoolProperty(
        name='Disable Quantization',
        description='Disable quantization; produces much larger glTF files with no extensions',
        default=True,
    )

    export_gltfpack_kn: BoolProperty(
        name='Keep Named Nodes',
        description='Restrict some optimization to keep named nodes and meshes attached to named nodes so that named nodes can be transformed externally',
        default=False,
    )

    export_format: EnumProperty(
        name='Format',
        description=(
            'Output format. Binary is most efficient, '
            'but JSON may be easier to edit later'
        ),
        items=(('GLB', 'glTF Binary (.glb)',
              'Exports a single file, with all data packed in binary form. '
              'Most efficient and portable, but more difficult to edit later'),
             ('GLTF_SEPARATE', 'glTF Separate (.gltf + .bin + textures)',
              'Exports multiple files, with separate JSON, binary and texture data. '
              'Easiest to edit later')),
        default=0,  # Warning => If you change the default, need to change the default filter too
    )

    ui_tab: EnumProperty(
        items=(('GENERAL', "General", "General settings"),
               ('MESHES', "Meshes", "Mesh settings"),
               ('OBJECTS', "Objects", "Object settings"),
               ('ANIMATION', "Animation", "Animation settings")),
        name="ui_tab",
        description="Export setting categories",
    )

    export_copyright: StringProperty(
        name='Copyright',
        description='Legal rights and conditions for the model',
        default=''
    )

    export_image_format: EnumProperty(
        name='Images',
        items=(('AUTO', 'Automatic',
                'Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. '
                'For other formats, use PNG'),
               ('JPEG', 'JPEG Format (.jpg)',
                'Save images as JPEGs. (Images that need alpha are saved as PNGs though.) '
                'Be aware of a possible loss in quality'),
               ('WEBP', 'WebP Format',
                'Save images as WebPs as main image (no fallback)'),
               ('NONE', 'None',
                'Don\'t export images'),
               ),
        description=(
            'Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web '
            'applications due to the smaller file size. Alternatively they can be omitted if they are not needed'
        ),
        default='AUTO'
    )

    export_image_add_webp: BoolProperty(
        name='Create WebP',
        description=(
            "Creates WebP textures for every texture. "
            "For already WebP textures, nothing happens"
        ),
        default=False
    )

    export_image_webp_fallback: BoolProperty(
        name='WebP Fallback',
        description=(
            "For all WebP textures, create a PNG fallback texture"
        ),
        default=False
    )

    export_texture_dir: StringProperty(
        name='Textures',
        description='Folder to place texture files in. Relative to the .gltf file',
        default='',
    )

    export_jpeg_quality: IntProperty(
        name='JPEG Quality',
        description='Quality of JPEG export',
        default=75,
        min=0,
        max=100
    )

    export_image_quality: IntProperty(
        name='Image Quality',
        description='Quality of image export',
        default=75,
        min=0,
        max=100
    )

    export_keep_originals: BoolProperty(
        name='Keep Original',
        description=('Keep original textures files if possible. '
                     'WARNING: if you use more than one texture, '
                     'where pbr standard requires only one, only one texture will be used. '
                     'This can lead to unexpected results'
                     ),
        default=False,
    )

    export_texcoords: BoolProperty(
        name='UVs',
        description='Export UVs (texture coordinates) with meshes',
        default=True
    )

    export_normals: BoolProperty(
        name='Normals',
        description='Export vertex normals with meshes',
        default=True
    )

    export_gn_mesh: BoolProperty(
        name='Geometry Nodes Instances (Experimental)',
        description='Export Geometry nodes instance meshes',
        default=False
    )

    export_draco_mesh_compression_enable: BoolProperty(
        name='Draco Mesh Compression',
        description='Compress mesh using Draco',
        default=False
    )

    export_draco_mesh_compression_level: IntProperty(
        name='Compression Level',
        description='Compression level (0 = most speed, 6 = most compression, higher values currently not supported)',
        default=6,
        min=0,
        max=10
    )

    export_draco_position_quantization: IntProperty(
        name='Position Quantization Bits',
        description='Quantization bits for position values (0 = no quantization)',
        default=14,
        min=0,
        max=30
    )

    export_draco_normal_quantization: IntProperty(
        name='Normal Quantization Bits',
        description='Quantization bits for normal values (0 = no quantization)',
        default=10,
        min=0,
        max=30
    )

    export_draco_texcoord_quantization: IntProperty(
        name='Texcoord Quantization Bits',
        description='Quantization bits for texture coordinate values (0 = no quantization)',
        default=12,
        min=0,
        max=30
    )

    export_draco_color_quantization: IntProperty(
        name='Color Quantization Bits',
        description='Quantization bits for color values (0 = no quantization)',
        default=10,
        min=0,
        max=30
    )

    export_draco_generic_quantization: IntProperty(
        name='Generic Quantization Bits',
        description='Quantization bits for generic values like weights or joints (0 = no quantization)',
        default=12,
        min=0,
        max=30
    )

    export_tangents: BoolProperty(
        name='Tangents',
        description='Export vertex tangents with meshes',
        default=False
    )

    export_materials: EnumProperty(
        name='Materials',
        items=(
            ('EXPORT',
             'Export',
             'Export all materials used by included objects'),
            ('PLACEHOLDER',
             'Placeholder',
             'Do not export materials, but write multiple primitive groups per mesh, keeping material slot information'),
            ('VIEWPORT',
            'Viewport',
            'Export minimal materials as defined in Viewport display properties'),
            ('NONE',
             'No export',
             'Do not export materials, and combine mesh primitive groups, losing material slot information')),
        description='Export materials',
        default='EXPORT')

    export_unused_images: BoolProperty(
        name='Unused Images',
        description='Export images not assigned to any material',
        default=False)

    export_unused_textures: BoolProperty(
        name='Prepare Unused Textures',
        description=(
            'Export image texture nodes not assigned to any material. '
            'This feature is not standard and needs an external extension to be included in the glTF file'
        ),
        default=False)

    export_vertex_color: EnumProperty(
        name='Use Vertex Color',
        items=(
            ('MATERIAL', 'Material',
             'Export vertex color when used by material'),
            ('ACTIVE', 'Active',
             'Export active vertex color'),
            ('NAME', 'Name',
             'Export vertex color with this name'),
            ('NONE', 'None',
             'Do not export vertex color')),
        description='How to export vertex color',
        default='MATERIAL'
    )

    export_vertex_color_name: StringProperty(
        name='Vertex Color Name',
        description='Name of vertex color to export',
        default='Color'
    )

    export_all_vertex_colors: BoolProperty(
        name='Export All Vertex Colors',
        description=(
            'Export all vertex colors, even if not used by any material. '
            'If no Vertex Color is used in the mesh materials, a fake COLOR_0 will be created, '
            'in order to keep material unchanged'
        ),
        default=True
    )

    export_active_vertex_color_when_no_material: BoolProperty(
        name='Export Active Vertex Color When No Material',
        description='When there is no material on object, export active vertex color',
        default=True
    )

    export_attributes: BoolProperty(
        name='Attributes',
        description='Export Attributes (when starting with underscore)',
        default=False
    )

    use_mesh_edges: BoolProperty(
        name='Loose Edges',
        description=(
            'Export loose edges as lines, using the material from the first material slot'
        ),
        default=False,
    )

    use_mesh_vertices: BoolProperty(
        name='Loose Points',
        description=(
            'Export loose points as glTF points, using the material from the first material slot'
        ),
        default=False,
    )

    export_cameras: BoolProperty(
        name='Cameras',
        description='Export cameras',
        default=False
    )

    use_selection: BoolProperty(
        name='Selected Objects',
        description='Export selected objects only',
        default=False
    )

    use_visible: BoolProperty(
        name='Visible Objects',
        description='Export visible objects only',
        default=False
    )

    use_renderable: BoolProperty(
        name='Renderable Objects',
        description='Export renderable objects only',
        default=False
    )

    use_active_collection_with_nested: BoolProperty(
        name='Include Nested Collections',
        description='Include active collection and nested collections',
        default=True
    )

    use_active_collection: BoolProperty(
        name='Active Collection',
        description='Export objects in the active collection only',
        default=False
    )

    use_active_scene: BoolProperty(
        name='Active Scene',
        description='Export active scene only',
        default=False
    )

    collection: StringProperty(
        name="Source Collection",
        description="Export only objects from this collection (and its children)",
        default="",
    )

    at_collection_center: BoolProperty(
        name="Export at Collection Center",
        description="Export at Collection center of mass of root objects of the collection",
        default=False,
    )

    export_extras: BoolProperty(
        name='Custom Properties',
        description='Export custom properties as glTF extras',
        default=False
    )

    export_yup: BoolProperty(
        name='+Y Up',
        description='Export using glTF convention, +Y up',
        default=True
    )

    export_apply: BoolProperty(
        name='Apply Modifiers',
        description='Apply modifiers (excluding Armatures) to mesh objects -'
                    'WARNING: prevents exporting shape keys',
        default=False
    )

    export_shared_accessors: BoolProperty(
        name='Shared Accessors',
        description='Export Primitives using shared accessors for attributes',
        default=False
    )

    export_animations: BoolProperty(
        name='Animations',
        description='Exports active actions and NLA tracks as glTF animations',
        default=True
    )

    export_frame_range: BoolProperty(
        name='Limit to Playback Range',
        description='Clips animations to selected playback range',
        default=False
    )

    export_frame_step: IntProperty(
        name='Sampling Rate',
        description='How often to evaluate animated values (in frames)',
        default=1,
        min=1,
        max=120
    )

    export_force_sampling: BoolProperty(
        name='Always Sample Animations',
        description='Apply sampling to all animations',
        default=True
    )

    export_sampling_interpolation_fallback: EnumProperty(
        name='Sampling Interpolation Fallback',
        items=(('LINEAR', 'Linear', 'Linear interpolation between keyframes'),
               ('STEP', 'Step', 'No interpolation between keyframes'),
        ),
        description='Interpolation fallback for sampled animations, when the property is not keyed',
        default='LINEAR'
    )

    export_pointer_animation: BoolProperty(
        name='Export Animation Pointer (Experimental)',
        description='Export material, Light & Camera animation as Animation Pointer. '
                    'Available only for baked animation mode \'NLA Tracks\' and \'Scene\'',
        default=False
    )

    export_animation_mode: EnumProperty(
        name='Animation Mode',
        items=(('ACTIONS', 'Actions',
                'Export actions (actives and on NLA tracks) as separate animations'),
               ('ACTIVE_ACTIONS', 'Active actions merged',
                'All the currently assigned actions become one glTF animation'),
               ('BROADCAST', 'Broadcast actions',
                'Broadcast all compatible actions to all objects. '
                'Animated objects will get all actions compatible with them, '
                'others will get no animation at all'),
               ('NLA_TRACKS', 'NLA Tracks',
                'Export individual NLA Tracks as separate animation'),
               ('SCENE', 'Scene',
                'Export baked scene as a single animation')
               ),
        description='Export Animation mode',
        default='ACTIONS'
    )

    export_nla_strips_merged_animation_name: StringProperty(
        name='Merged Animation Name',
        description=(
            "Name of single glTF animation to be exported"
        ),
        default='Animation'
    )

    export_def_bones: BoolProperty(
        name='Export Deformation Bones Only',
        description='Export Deformation bones only',
        default=False
    )

    export_hierarchy_flatten_bones: BoolProperty(
        name='Flatten Bone Hierarchy',
        description='Flatten Bone Hierarchy. Useful in case of non decomposable transformation matrix',
        default=False
    )

    export_hierarchy_flatten_objs: BoolProperty(
        name='Flatten Object Hierarchy',
        description='Flatten Object Hierarchy. Useful in case of non decomposable transformation matrix',
        default=False
    )

    export_armature_object_remove: BoolProperty(
        name='Remove Armature Object',
        description=(
            'Remove Armature object if possible. '
            'If Armature has multiple root bones, object will not be removed'
        ),
        default=False
    )

    export_leaf_bone: BoolProperty(
        name='Add Leaf Bones',
        description=(
            'Append a final bone to the end of each chain to specify last bone length '
            '(use this when you intend to edit the armature from exported data)'
        ),
        default=False
    )

    export_optimize_animation_size: BoolProperty(
        name='Optimize Animation Size',
        description=(
            "Reduce exported file size by removing duplicate keyframes"
        ),
        default=True
    )

    export_optimize_animation_keep_anim_armature: BoolProperty(
        name='Force Keeping Channels for Bones',
        description=(
            "If all keyframes are identical in a rig, "
            "force keeping the minimal animation. "
            "When off, all possible channels for "
            "the bones will be exported, even if empty "
            "(minimal animation, 2 keyframes)"
        ),
        default=True
    )

    export_optimize_animation_keep_anim_object: BoolProperty(
        name='Force Keeping Channel for Objects',
        description=(
            "If all keyframes are identical for object transformations, "
            "force keeping the minimal animation"
        ),
        default=False
    )

    export_optimize_disable_viewport: BoolProperty(
        name='Disable Viewport for Other Objects',
        description=(
            "When exporting animations, disable viewport for other objects, "
            "for performance"
        ),
        default=False
    )

    export_negative_frame: EnumProperty(
        name='Negative Frames',
        items=(('SLIDE', 'Slide',
                'Slide animation to start at frame 0'),
               ('CROP', 'Crop',
                'Keep only frames above frame 0'),
               ),
        description='Negative Frames are slid or cropped',
        default='SLIDE'
    )

    export_anim_slide_to_zero: BoolProperty(
        name='Set All glTF Animation Starting at 0',
        description=(
            "Set all glTF animation starting at 0.0s. "
            "Can be useful for looping animations"
        ),
        default=False
    )

    export_bake_animation: BoolProperty(
        name='Bake All Objects Animations',
        description=(
            "Force exporting animation on every object. "
            "Can be useful when using constraints or driver. "
            "Also useful when exporting only selection"
        ),
        default=False
    )

    export_merge_animation: EnumProperty(
        name='Merge Animation',
        items=(('NLA_TRACK', 'NLA Track Names', 'Merge by NLA Track Names'),
               ('ACTION', 'Actions', 'Merge by Actions'),
               ('NONE', 'No Merge', 'Do Not Merge Animations'),
               ),
        description='Merge Animations',
        default='ACTION'
    )

    export_anim_single_armature: BoolProperty(
        name='Export all Armature Actions',
        description=(
            "Export all actions, bound to a single armature. "
            "WARNING: Option does not support exports including multiple armatures"
        ),
        default=True
    )

    export_reset_pose_bones: BoolProperty(
        name='Reset Pose Bones Between Actions',
        description=(
            "Reset pose bones between each action exported. "
            "This is needed when some bones are not keyed on some animations"
        ),
        default=True
    )

    export_current_frame: BoolProperty(
        name='Use Current Frame as Object Rest Transformations',
        description=(
            'Export the scene in the current animation frame. '
            'When off, frame 0 is used as rest transformations for objects'
        ),
        default=False
    )

    export_rest_position_armature: BoolProperty(
        name='Use Rest Position Armature',
        description=(
            "Export armatures using rest position as joints' rest pose. "
            "When off, current frame pose is used as rest pose"
        ),
        default=True
    )

    export_anim_scene_split_object: BoolProperty(
        name='Split Animation by Object',
        description=(
            "Export Scene as seen in Viewport, "
            "But split animation by Object"
        ),
        default=True
    )

    export_skins: BoolProperty(
        name='Skinning',
        description='Export skinning (armature) data',
        default=True
    )

    export_influence_nb: IntProperty(
        name='Bone Influences',
        description='Choose how many Bone influences to export',
        default=4,
        min=1
    )

    export_all_influences: BoolProperty(
        name='Include All Bone Influences',
        description='Allow export of all joint vertex influences. Models may appear incorrectly in many viewers',
        default=False
    )

    export_morph: BoolProperty(
        name='Shape Keys',
        description='Export shape keys (morph targets)',
        default=True
    )

    export_morph_normal: BoolProperty(
        name='Shape Key Normals',
        description='Export vertex normals with shape keys (morph targets)',
        default=True
    )

    export_morph_tangent: BoolProperty(
        name='Shape Key Tangents',
        description='Export vertex tangents with shape keys (morph targets)',
        default=False
    )

    export_morph_animation: BoolProperty(
        name='Shape Key Animations',
        description='Export shape keys animations (morph targets)',
        default=True
    )

    export_morph_reset_sk_data: BoolProperty(
        name='Reset Shape Keys Between Actions',
        description=(
            "Reset shape keys between each action exported. "
            "This is needed when some SK channels are not keyed on some animations"
        ),
        default=True
    )

    export_lights: BoolProperty(
        name='Punctual Lights',
        description='Export directional, point, and spot lights. '
                    'Uses "KHR_lights_punctual" glTF extension',
        default=False
    )

    export_try_sparse_sk: BoolProperty(
        name='Use Sparse Accessor if Better',
        description='Try using Sparse Accessor if it saves space',
        default=True
    )

    export_try_omit_sparse_sk: BoolProperty(
        name='Omitting Sparse Accessor if Data is Empty',
        description='Omitting Sparse Accessor if data is empty',
        default=False
    )

    export_gpu_instances: BoolProperty(
        name='GPU Instances',
        description='Export using EXT_mesh_gpu_instancing. '
                    'Limited to children of a given Empty. '
                    'Multiple materials might be omitted',
        default=False
    )

    export_action_filter: BoolProperty(
        name='Filter Actions',
        description='Filter Actions to be exported',
        default=False,
    )

    export_convert_animation_pointer: BoolProperty(
        name='Convert TRS/Weights to Animation Pointer',
        description='Export TRS and weights as Animation Pointer. '
                    'Using KHR_animation_pointer extension',
        default=False
    )


    will_save_settings: BoolProperty(
        name='Remember Export Settings',
        description='Store glTF export settings in the Blender project',
        default=False)

    export_hierarchy_full_collections: BoolProperty(
        name='Full Collection Hierarchy',
        description='Export full hierarchy, including intermediate collections',
        default=False
    )

    export_extra_animations: BoolProperty(
        name='Prepare Extra Animations',
        description=(
            'Export additional animations.\n'
            'This feature is not standard and needs an external extension to be included in the glTF file'
        ),
        default=False
    )

    export_loglevel: IntProperty(
        name='Log Level',
        description="Log Level",
        default=-1,
    )

    

class TAMT_export_Preset_Properties(bpy.types.PropertyGroup):

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
        items=[('FBX',"FBX Export","Exports the file as Project.fbx"),
                ('OBJ',"OBJ Export","Export the file as Project.obj"),
                ('USD',"USD Export", "Export as file.usdc"),
                ('DAE',"DAE Export","Export as .dae (Collada)"),
                ('GLTF',"GLTF/GLB Export","Export as .gltf/.glb")])
    

    exp_FBXProperties:  bpy.props.PointerProperty(type=TAMT_fbxExportProperties)
    exp_OBJProperties:  bpy.props.PointerProperty(type=TAMT_objExportProperties)
    exp_USDProperties:  bpy.props.PointerProperty(type=TAMT_usdExportProperties)
    exp_DAEProperties:  bpy.props.PointerProperty(type=TAMT_daeExportProperties)
    exp_GLTFProperties: bpy.props.PointerProperty(type=TAMT_gltfExportProperties)


    
    exp_editPresetDetails: bpy.props.BoolProperty(
        name = "Edit Preset",
        description="Edit Properties of Preset.",
        default= False,
    )

    exp_triangulate: bpy.props.BoolProperty(
        name = 'Triangulate',
        description="Explicitly Triangulate the meshes using modifier during export, best for consistent results",
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

    
    inc_collections: bpy.props.CollectionProperty(type= TAMT_CollectionItem)
    inc_collections_index: bpy.props.IntProperty(name = "Collections Index", default= -1)

    exc_collections: bpy.props.CollectionProperty(type= TAMT_CollectionItem)
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

    



class TAMT_exportCollection(bpy.types.PropertyGroup):
    presets: bpy.props.CollectionProperty(type = TAMT_export_Preset_Properties)



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

    export_collection: bpy.props.PointerProperty(type = TAMT_exportCollection)
    export_presets: bpy.props.PointerProperty(type = exportPresetActive)


    



classes = (
    TAMT_CollectionItem,
    exportPresetActive,
    TAMT_fbxExportProperties,
    TAMT_objExportProperties,
    TAMT_usdExportProperties,
    TAMT_daeExportProperties,
    TAMT_gltfExportProperties,
    TAMT_export_Preset_Properties,
    TAMT_exportCollection,
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