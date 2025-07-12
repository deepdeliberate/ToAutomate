# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 





import bpy

#------------------------ FBX Panel ----------------------------


def TAMT_fbx_export_panel_Include(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_include", default_closed=True)
    header.label(text="Include")
    if body:
        body.prop(operator, "object_types")
        body.prop(operator, "use_custom_props")

def TAMT_fbx_export_panel_transform(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_transform", default_closed=True)
    header.label(text="Transform")
    if body:
        body.prop(operator, "global_scale")
        body.prop(operator, "apply_scale_options")

        body.prop(operator, "axis_forward")
        body.prop(operator, "axis_up")

        body.prop(operator, "apply_unit_scale")
        body.prop(operator, "use_space_transform")
        e_row = body.row()
        e_row.prop(operator, "bake_space_transform")

def TAMT_fbx_export_panel_geometry(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_geometry", default_closed=True)
    header.label(text="Geometry")
    if body:
        body.prop(operator, "mesh_smooth_type")
        body.prop(operator, "use_subsurf")
        body.prop(operator, "use_mesh_modifiers")

        body.prop(operator, "use_mesh_edges")
        body.prop(operator, "use_triangles")
        sub = body.row()

        sub.prop(operator, "use_tspace")
        body.prop(operator, "colors_type")
        body.prop(operator, "prioritize_active_color")

def TAMT_fbx_export_panel_armature(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_armature", default_closed=True)
    header.label(text="Armature")
    if body:
        body.prop(operator, "primary_bone_axis")
        body.prop(operator, "secondary_bone_axis")
        body.prop(operator, "armature_nodetype")
        body.prop(operator, "use_armature_deform_only")
        body.prop(operator, "add_leaf_bones")


def TAMT_fbx_export_panel_animation(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_bake_animation", default_closed=True)
    header.use_property_split = False
    header.prop(operator, "bake_anim", text="")
    header.label(text="Animation")
    if body:
        body.enabled = operator.bake_anim
        body.prop(operator, "bake_anim_use_all_bones")
        body.prop(operator, "bake_anim_use_nla_strips")
        body.prop(operator, "bake_anim_use_all_actions")
        body.prop(operator, "bake_anim_force_startend_keying")
        body.prop(operator, "bake_anim_step")
        body.prop(operator, "bake_anim_simplify_factor")


def fbx_properties(layout, operator):
    layout.label(text = "FBX Preset Setting")

    TAMT_fbx_export_panel_Include(layout, operator)
    TAMT_fbx_export_panel_transform(layout, operator)
    TAMT_fbx_export_panel_geometry(layout, operator)
    TAMT_fbx_export_panel_armature(layout, operator)
    TAMT_fbx_export_panel_animation(layout, operator)



#------------------------ OBJ Panel ----------------------------


def TAMT_obj_General_panel(layout, operator):
    header, body = layout.panel("TAMT_OBJ_export_general", default_closed = True)
    header.label(text = "General")
    if body:
        body.prop(operator, "global_scale")
        body.prop(operator, "forward_axis")
        body.prop(operator, "up_axis")

def TAMT_obj_Geometry_panel(layout, operator):
    header, body = layout.panel("TAMT_OBJ_export_geometry", default_closed = True)
    header.label(text = "Geometry")

    if body:
        body.prop(operator, "export_uv")
        body.prop(operator, "export_normals")
        body.prop(operator, "export_colors")
        body.prop(operator, "export_curves_as_nurbs", text = "Curves as NURBS")
        body.prop(operator, "export_triangulated_mesh", text = "Triangulated Mesh")
        body.prop(operator, "apply_modifiers")
        body.prop(operator, "export_eval_mode")

        
def TAMT_obj_Grouping_panel(layout, operator):
    header, body = layout.panel("TAMT_OBJ_export_grouping", default_closed = True)
    header.label(text = "Grouping")

    if body:
        body.prop(operator, "export_object_groups")
        body.prop(operator, "export_material_groups")
        body.prop(operator, "export_vertex_groups")
        body.prop(operator, "export_smooth_groups")
        body.prop(operator, "smooth_group_bitflags")

        
def TAMT_obj_Material_panel(layout, operator):
    header, body = layout.panel("TAMT_OBJ_export_material", default_closed = True)
    header.label(text = "Materials")

    if body:
        body.prop(operator, "export_materials")
        body.prop(operator, "export_pbr_extensions", text = "PBR Extensions")
        body.prop(operator, "path_mode")


def TAMT_obj_Animation_panel(layout, operator):
    header, body = layout.panel("TAMT_OBJ_export_animation", default_closed = True)
    header.label(text = "Animation")

    if body:
        body.prop(operator, "export_animation")
        body.prop(operator, "start_frame")
        body.prop(operator, "end_frame")



def obj_properties(layout, operator):
    layout.label(text = "OBJ Preset Setting")

    TAMT_obj_General_panel(layout, operator)
    TAMT_obj_Geometry_panel(layout, operator)
    TAMT_obj_Material_panel(layout, operator)
    TAMT_obj_Animation_panel(layout, operator)


#------------------------ USD Panel ----------------------------



def TAMT_usd_General_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_general", default_closed = True)
    header.label(text = "General")
    if body:
        body.prop(operator,"visible_objects_only")
        body.prop(operator,"export_animation")
        body.prop(operator,"export_custom_properties")
        body.prop(operator,"custom_properties_namespace")
        body.prop(operator,"author_blender_name")
        body.prop(operator,"allow_unicode")
        body.prop(operator,"relative_paths")
        body.prop(operator,"convert_orientation")
        if operator.convert_orientation:
            body.prop(operator,"export_global_forward_selection")
            body.prop(operator,"export_global_up_selection")
        body.prop(operator,"convert_scene_units")
        if operator.convert_scene_units == 'CUSTOM':
            body.prop(operator,"meters_per_unit")
        body.prop(operator,"xform_op_mode")
        body.prop(operator,"evaluation_mode")

def TAMT_usd_OBJECTYPE_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_ObjectType", default_closed = True)
    header.label(text = "Object Types")
    if body:
        body.prop(operator,"export_meshes")
        body.prop(operator,"export_lights")
        body.prop(operator,"convert_world_material")
        body.prop(operator,"export_cameras")
        body.prop(operator,"export_curves")
        body.prop(operator,"export_points")
        body.prop(operator,"export_volumes")
        body.prop(operator,"export_hair")

def TAMT_usd_GEOMETRY_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_Geometry", default_closed = True)
    header.label(text = "Geometry")
    if body:
        body.prop(operator, "export_uvmaps")
        body.prop(operator, "rename_uvmaps")
        body.prop(operator, "export_normals")
        body.prop(operator, "merge_parent_xform")
        body.prop(operator, "triangulate_meshes")
        body.prop(operator, "quad_method")
        body.prop(operator, "ngon_method")
        body.prop(operator, "export_subdivision")

def TAMT_usd_RIGGING_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_Rigging", default_closed = True)
    header.label(text = "Rigging")
    if body:
        body.prop(operator,"export_shapekeys")
        body.prop(operator,"export_armatures")
        body.prop(operator,"only_deform_bones")

def TAMT_usd_MATERIALS_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_Materials", default_closed = True)
    header.label(text = "Materials")
    if body:
        body.prop(operator,"generate_preview_surface")
        body.prop(operator,"generate_materialx_network")
        body.prop(operator,"export_textures_mode")
        body.prop(operator,"overwrite_textures")
        body.prop(operator,"usdz_downscale_size")
        if operator.usdz_downscale_size == 'CUSTOM':
            body.prop(operator, "usdz_downscale_custom_size")

def TAMT_usd_EXPERIMENTAL_panel(layout, operator):
    header, body = layout.panel("TAMT_USD_export_Experimental", default_closed = True)
    header.label(text = "Experimental")

    if body:
        body.prop(operator,"use_instancing")


def usd_properties(layout, operator):
    layout.label(text = "USD Preset Setting")

    TAMT_usd_General_panel(layout, operator)
    TAMT_usd_OBJECTYPE_panel(layout, operator)
    TAMT_usd_GEOMETRY_panel(layout, operator)
    TAMT_usd_RIGGING_panel(layout, operator)
    TAMT_usd_MATERIALS_panel(layout, operator)
    TAMT_usd_EXPERIMENTAL_panel(layout, operator)



#------------------------ DAE COLLADA Panel ----------------------------



def TAMT_COLLADA_Main_panel(layout, operator):
    header, body = layout.panel("TAMT_COLLADA_export_Main", default_closed = True)
    header.label(text = "Main")

    if body:
        box1=body.box()
        box1.label(text = "Global Orientation")
        box1.prop(operator, "apply_global_orientation", text="Apply Orientation")
        box1.prop(operator, "export_global_forward_selection"),
        box1.prop(operator, "export_global_up_selection"),


def TAMT_COLLADA_Geo_panel(layout, operator):
    header, body = layout.panel("TAMT_COLLADA_export_Geo", default_closed = True)
    header.label(text = "Geometry")

    if body:
        body.prop(operator, "triangulate"),
        body.prop(operator,"apply_modifiers")
        body.prop(operator,"export_mesh_type_selection", text = "Modifier Settings")
        body.prop(operator, "export_object_transformation_type_selection")

def TAMT_COLLADA_ARM_panel(layout, operator):
    header, body = layout.panel("TAMT_COLLADA_export_ARM", default_closed = True)
    header.label(text = "Armature")

    if body:
        body.prop(operator, "deform_bones_only")
        body.prop(operator, "open_sim")


def TAMT_COLLADA_ANIMATION_panel(layout, operator):
    header, body = layout.panel("TAMT_COLLADA_export_ANIMATION", default_closed = True)
    header.label(text = "Animation")
    if body:
        body.prop(operator, "include_animations")
        enable_anim = operator.include_animations

        curve_key = True
        if operator.export_animation_type_selection == 'sample':
            curve_key = False,
        else:
            curve_key = True

        body.prop(operator, "export_animation_type_selection",expand = True )
        body.prop(operator, "keep_smooth_curves")

        enabled_samples = enable_anim and not curve_key
        row = body.column()
        row.prop(operator, "sampling_rate" )
        row.prop(operator, "keep_keyframes" )
        row.prop(operator, "keep_flat_curves")
        row.prop(operator, "include_all_actions" )
        row.prop(operator, "export_animation_transformation_type_selection"  )
        

def TAMT_COLLADA_EXTRA_panel(layout, operator):
    header, body = layout.panel("TAMT_COLLADA_export_EXTRA", default_closed = True)
    header.label(text = "Extra")
    if body:
        body.prop(operator, "use_object_instantiation")
        body.prop(operator, "use_blender_profile")
        body.prop(operator, "sort_by_name")
        body.prop(operator, "keep_bind_info")
        body.prop(operator, "limit_precision")



def dae_properties(layout, operator):
    layout.label(text = "DAE Preset Setting")
    TAMT_COLLADA_Main_panel(layout, operator)
    TAMT_COLLADA_Geo_panel(layout, operator)
    TAMT_COLLADA_ANIMATION_panel(layout, operator)
    TAMT_COLLADA_EXTRA_panel(layout, operator)


# --------------------------- GLTF Panel ------------------------------

def TAMT_GLTF_Include_panel(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_INCLUDE", default_closed = True)
    header.label(text = "Include")
    if body:
        body.prop(operator, "export_extras")
        body.prop(operator, "export_cameras")
        body.prop(operator, "export_lights")

def TAMT_GLTF_Transform_panel(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Transform", default_closed = True)
    header.label(text = "Include")
    if body:
        body.prop(operator, "export_yup")

def TAMT_GLTF_Data_scenegraph(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_data_scenegraph", default_closed = True)
    header.label(text="Scene Graph")

    if body:
        body.prop(operator, "export_gn_mesh")
        body.prop(operator, "export_gpu_instances")
        body.prop(operator, "export_hierarchy_flatten_objs")
        body.prop(operator, "export_hierarchy_full_collections")

def TAMT_GLTF_Data_mesh(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_data_mesh", default_closed = True)
    header.label(text="Mesh")

    if body:
        body.prop(operator, 'export_apply')
        body.prop(operator, 'export_texcoords')
        body.prop(operator, 'export_normals')
        col = body.column()
        col.active = operator.export_normals
        col.prop(operator, 'export_tangents')
        body.prop(operator, 'export_attributes')

        col = body.column()
        col.prop(operator, 'use_mesh_edges')
        col.prop(operator, 'use_mesh_vertices')

        col = body.column()
        col.prop(operator, 'export_shared_accessors')

        header, sub_body = body.panel("GLTF_export_data_material_vertex_color", default_closed=True)
        header.label(text="Vertex Colors")
        if sub_body:
            row = sub_body.row()
            row.prop(operator, 'export_vertex_color')
            row = sub_body.row()
            if operator.export_vertex_color == "NAME":
                row.prop(operator, 'export_vertex_color_name')
            if operator.export_vertex_color in ["ACTIVE", "NAME"]:
                row = sub_body.row()
                row.label(
                    text="Note that fully compliant glTF 2.0 engine/viewer will use it as multiplicative factor for base color.",
                    icon='ERROR')
                row = sub_body.row()
                row.label(text="If you want to use VC for any other purpose than vertex color, you should use custom attributes.")
            row = sub_body.row()
            row.active = operator.export_vertex_color != "NONE"
            row.prop(operator, 'export_all_vertex_colors')
            row = sub_body.row()
            row.active = operator.export_vertex_color != "NONE"
            row.prop(operator, 'export_active_vertex_color_when_no_material')


def TAMT_GLTF_Data_material(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_data_material", default_closed = True)
    header.label(text="Material")

    if body:
        body.prop(operator, 'export_materials')
        col = body.column()
        col.active = operator.export_materials == "EXPORT"
        col.prop(operator, 'export_image_format')
        if operator.export_image_format in ["AUTO", "JPEG", "WEBP"]:
            col.prop(operator, 'export_image_quality')
        col = body.column()
        col.active = operator.export_image_format != "WEBP" and not operator.export_materials in ['PLACEHOLDER', 'NONE', 'VIEWPORT']
        col.prop(operator, "export_image_add_webp")
        col = body.column()
        col.active = operator.export_image_format != "WEBP" and not operator.export_materials in ['PLACEHOLDER', 'NONE', 'VIEWPORT']
        col.prop(operator, "export_image_webp_fallback")

        header, sub_body = body.panel("GLTF_export_data_material_unused", default_closed=True)
        header.label(text="Unused Textures & Images")
        header.active = operator.export_materials == "EXPORT"
        if sub_body:
            sub_body.active = operator.export_materials == "EXPORT"
            row = sub_body.row()
            row.prop(operator, 'export_unused_images')
            row = sub_body.row()
            row.prop(operator, 'export_unused_textures')

        
def TAMT_GLTF_Data_shapekeys(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data_shapekeys", default_closed = True)
    header.use_property_split = False
    header.prop(operator, "export_morph", text="")
    header.label(text = "Shape Keys")
    if body:
        body.active = operator.export_morph

        body.prop(operator, 'export_morph_normal')
        col = body.column()
        col.active = operator.export_morph_normal
        col.prop(operator, 'export_morph_tangent')

        # Data-Shape Keys-Optimize
        header, sub_body = body.panel("GLTF_export_data_shapekeys_optimize", default_closed=True)
        header.label(text="Optimize Shape Keys")
        if sub_body:
            row = sub_body.row()
            row.prop(operator, 'export_try_sparse_sk')

            row = sub_body.row()
            row.active = operator.export_try_sparse_sk
            row.prop(operator, 'export_try_omit_sparse_sk')


def TAMT_GLTF_Data_armature(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data_armature", default_closed = True)
    header.label(text = "Armature")
    if body:
        body.active = operator.export_skins

        body.prop(operator, 'export_rest_position_armature')

        row = body.row()
        row.active = operator.export_force_sampling
        row.prop(operator, 'export_def_bones')
        if operator.export_force_sampling is False and operator.export_def_bones is True:
            body.label(text="Export only deformation bones is not possible when not sampling animation")
        row = body.row()
        row.prop(operator, 'export_armature_object_remove')
        row = body.row()
        row.prop(operator, 'export_hierarchy_flatten_bones')
        row = body.row()
        row.prop(operator, 'export_leaf_bone')

def TAMT_GLTF_Data_skinning(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data_skinning", default_closed = True)
    header.use_property_split = False
    header.prop(operator, "export_skins", text="")
    header.label(text = "Skinning")
    if body:
        body.active = operator.export_skins

        row = body.row()
        row.prop(operator, 'export_influence_nb')
        row.active = not operator.export_all_influences
        body.prop(operator, 'export_all_influences')

def TAMT_GLTF_Data_lighting(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data_lighting", default_closed = True)
    header.label(text = "Lighting")
    if body:
        body.prop(operator, "export_import_convert_lighting_mode")

def TAMT_GLTF_Data_compression(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data_compression", default_closed = True)
    header.label(text = "Compressions")
    if body:
        body.active = operator.export_draco_mesh_compression_enable

        body.prop(operator, 'export_draco_mesh_compression_level')

        col = body.column(align=True)
        col.prop(operator, 'export_draco_position_quantization', text="Quantize Position")
        col.prop(operator, 'export_draco_normal_quantization', text="Normal")
        col.prop(operator, 'export_draco_texcoord_quantization', text="Tex Coord")
        col.prop(operator, 'export_draco_color_quantization', text="Color")
        col.prop(operator, 'export_draco_generic_quantization', text="Generic")


        
def TAMT_GLTF_Data_panel(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Data", default_closed = True)
    header.label(text = "Data")
    if body:
        TAMT_GLTF_Data_scenegraph(body, operator)
        TAMT_GLTF_Data_mesh(body, operator)
        TAMT_GLTF_Data_material(body, operator)
        TAMT_GLTF_Data_shapekeys(body, operator)
        TAMT_GLTF_Data_armature(body, operator)
        TAMT_GLTF_Data_skinning(body, operator)
        TAMT_GLTF_Data_lighting(body, operator)
        TAMT_GLTF_Data_compression(body, operator)



def TAMT_GLTF_Animation_notes(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_", default_closed = True)
    header.label(text = "Notes")
    if body:
        if operator.export_animation_mode == "SCENE":
            body.label(text="Scene mode uses full bake mode:")
            body.label(text="- sampling is active")
            body.label(text="- baking all objects is active")
            body.label(text="- Using scene frame range")
        elif operator.export_animation_mode == "NLA_TRACKS":
            body.label(text="Track mode uses full bake mode:")
            body.label(text="- sampling is active")
            body.label(text="- baking all objects is active")


def TAMT_GLTF_Animation_bakeAndMerge(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_bakeAndMerge", default_closed = True)
    header.label(text = "Bake & Merge")
    if body:
        body.active = operator.export_animations

        row = body.row()
        row.active = operator.export_force_sampling and operator.export_animation_mode in [
            'ACTIONS', 'ACTIVE_ACTIONS', 'BROACAST']
        row.prop(operator, 'export_bake_animation')

        if operator.export_animation_mode == "SCENE":
            row = body.row()
            row.prop(operator, 'export_anim_scene_split_object')

        row = body.row()
        row.active = operator.export_force_sampling and operator.export_animation_mode in ['ACTIONS']
        row.prop(operator, 'export_merge_animation')

        row = body.row()

def TAMT_GLTF_Animation_ranges(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_ranges", default_closed = True)
    header.label(text = "Rest & Ranges")
    if body:
        body.active = operator.export_animations

        body.prop(operator, 'export_current_frame')
        row = body.row()
        row.active = operator.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'BROADCAST', 'NLA_TRACKS']
        row.prop(operator, 'export_frame_range')
        body.prop(operator, 'export_anim_slide_to_zero')
        row = body.row()
        row.active = operator.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS', 'BROADCAST', 'NLA_TRACKS']
        body.prop(operator, 'export_negative_frame')

def TAMT_GLTF_Animation_armature(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_armature", default_closed = True)
    header.label(text = "Armature")
    if body:
        body.active = operator.export_animations

        row = body.row()
        row.active = operator.export_animation_mode == "ACTIONS"
        row.prop(operator, 'export_anim_single_armature')
        row = body.row()
        row.prop(operator, 'export_reset_pose_bones')


def TAMT_GLTF_Animation_shapekeys(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_shapekeys", default_closed = True)
    header.active = operator.export_animations and operator.export_morph
    header.use_property_split = False
    header.prop(operator, "export_morph_animation", text="")
    header.label(text = "Shape Keys Animation")
    if body:
        body.active = operator.export_animations and operator.export_morph

        row = body.row()
        row.active = operator.export_morph_animation
        row.prop(operator, 'export_morph_reset_sk_data')


def TAMT_GLTF_Animation_sampling(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_sampling", default_closed = True)
    header.use_property_split = False
    header.prop(operator, "export_force_sampling", text="")
    header.label(text = "Sampling Animations")
    if body:
        body.active = operator.export_animations and operator.export_force_sampling

        body.prop(operator, 'export_frame_step')
        body.prop(operator, 'export_sampling_interpolation_fallback')
    

def TAMT_GLTF_Animation_pointer(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_pointer", default_closed = True)
    header.use_property_split = False
    header.active = operator.export_animations and operator.export_animation_mode in ['NLA_TRACKS', 'SCENE']
    header.prop(operator, "export_pointer_animation", text="")
    header.label(text = "Sampling Animations")
    if body:
        row = body.row()
        row.active = header.active and operator.export_pointer_animation
        row.prop(operator, 'export_convert_animation_pointer')

def TAMT_GLTF_Animation_optimize(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_optimize", default_closed = True)
    header.label(text = "Optimize Animations")
    if body:
        body.active = operator.export_animations

        body.prop(operator, 'export_optimize_animation_size')

        row = body.row()
        row.prop(operator, 'export_optimize_animation_keep_anim_armature')

        row = body.row()
        row.prop(operator, 'export_optimize_animation_keep_anim_object')

        row = body.row()
        row.prop(operator, 'export_optimize_disable_viewport')


def TAMT_GLTF_Animation_extra(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation_extra", default_closed = True)
    header.label(text = "Extra Animations")
    if body:
        body.active = operator.export_animations

        body.prop(operator, 'export_extra_animations')

def TAMT_GLTF_Animation_action_filter(layout, operator):
    if operator.export_animation_mode not in ["ACTIONS", "ACTIVE_ACTIONS", "BROADCAST"]:
        return

    header, body = layout.panel("GLTF_export_action_filter", default_closed=True)
    header.use_property_split = False
    header.prop(operator, "export_action_filter", text="")
    header.label(text="Action Filter")
    if body and operator.export_action_filter:
        body.active = operator.export_animations and operator.export_action_filter

        row = body.row()

        # Collection Export does not handle correctly property declaration
        # So use this tweak to avoid spaming the console, waiting for a better solution
        if not is_file_browser and not hasattr(bpy.data.scenes[0], "gltf_action_filter"):
            row.label(text="Please disable/enable 'action filter' to refresh the list")
            return

        if len(bpy.data.actions) > 0:
            row.template_list(
                "SCENE_UL_gltf2_filter_action",
                "",
                bpy.data.scenes[0],
                "gltf_action_filter",
                bpy.data.scenes[0],
                "gltf_action_filter_active")
            col = row.column()
            row = col.column(align=True)
            row.operator("scene.gltf2_action_filter_refresh", icon="FILE_REFRESH", text="")
        else:
            row.label(text="No Actions in .blend file")

def TAMT_GLTF_Animation_panel(layout, operator):
    header, body = layout.panel("TAMT_GLTF_export_Animation", default_closed = True)
    header.use_property_split = False
    header.prop(operator, "export_animations", text = "")
    header.label(text = "Animation")
    if body:
        body.active = operator.export_animations

        body.prop(operator, 'export_animation_mode')
        if operator.export_animation_mode == "ACTIVE_ACTIONS":
            layout.prop(operator, 'export_nla_strips_merged_animation_name')

        if operator.export_animation_mode in ["NLA_TRACKS", "SCENE"]:
            TAMT_GLTF_Animation_notes(body, operator)
        TAMT_GLTF_Animation_bakeAndMerge(body, operator)
        TAMT_GLTF_Animation_ranges(body, operator)
        TAMT_GLTF_Animation_armature(body, operator)
        TAMT_GLTF_Animation_shapekeys(body, operator)
        TAMT_GLTF_Animation_sampling(body, operator)
        TAMT_GLTF_Animation_pointer(body, operator)
        TAMT_GLTF_Animation_optimize(body, operator)
        if operator.export_animation_mode in ['ACTIONS', 'ACTIVE_ACTIONS']:
            TAMT_GLTF_Animation_extra(body, operator)
        
        # Test first
        # TAMT_GLTF_Animation_action_filter(body, operator)



def gltf_properties(layout, operator):
    layout.label(text = "GLTF Preset Setting")
    TAMT_GLTF_Include_panel(layout, operator)
    TAMT_GLTF_Transform_panel(layout, operator)
    TAMT_GLTF_Data_panel(layout, operator)
    TAMT_GLTF_Animation_panel(layout, operator)