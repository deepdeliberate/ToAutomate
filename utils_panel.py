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