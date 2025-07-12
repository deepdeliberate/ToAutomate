import bpy

def pre_export_Algo_apply(col, final_objects, initial_state ):
    initial_state["hide_set"] = {obj: obj.hide_get() for obj in final_objects}
    initial_state["hide_viewport"] = {obj: obj.hide_viewport for obj in final_objects}
    initial_state["hide_render"] = {obj: obj.hide_render for obj in final_objects}

    for obj in final_objects:
        if col not in obj.users_collection:
            col.objects.link(obj)
        obj.hide_viewport = False
        obj.hide_set(False)
        obj.select_set(True)

def post_export_Algo_revert(col, final_objects, initial_state ):

    for obj in final_objects:
        col.objects.unlink(obj)
        obj.select_set(False)
        obj.hide_set( initial_state["hide_set"][obj] )
        obj.hide_viewport = initial_state["hide_viewport"][obj]
        obj.hide_render = initial_state["hide_render"][obj]

def export_FBX_Main_Func(final_objects, export_Path, settings):
    with bpy.context.temp_override(active_object = final_objects[0], selected_objects = final_objects):
        bpy.ops.export_scene.fbx(
            filepath = str(export_Path),
            check_existing=False,
            use_selection= True,
            use_visible=False,
            collection='', 

            global_scale=           settings.global_scale,
            apply_unit_scale=       settings.apply_unit_scale,
            apply_scale_options=    settings.apply_scale_options,
            use_space_transform=    settings.use_space_transform,
            bake_space_transform=   settings.bake_space_transform,
            object_types=           settings.object_types,
            
            use_mesh_modifiers=          settings.use_mesh_modifiers,
            mesh_smooth_type=           settings.mesh_smooth_type,
            colors_type=                settings.colors_type,
            prioritize_active_color=    settings.prioritize_active_color,
            use_subsurf=                settings.use_subsurf,
            use_mesh_edges=             settings.use_mesh_edges,
            use_tspace=                 settings.use_tspace,
            use_triangles=              settings.use_triangles,

            add_leaf_bones=             settings.add_leaf_bones,
            primary_bone_axis=          settings.primary_bone_axis,
            secondary_bone_axis=        settings.secondary_bone_axis,
            use_armature_deform_only=   settings.use_armature_deform_only,
            armature_nodetype=          settings.armature_nodetype,

            bake_anim=                  settings.bake_anim,
            bake_anim_use_all_bones=    settings.bake_anim_use_all_bones,
            bake_anim_use_nla_strips=   settings.bake_anim_use_nla_strips,
            bake_anim_use_all_actions = settings.bake_anim_use_all_actions,
            bake_anim_force_startend_keying= settings.bake_anim_force_startend_keying,
            bake_anim_step=             settings.bake_anim_step,
            bake_anim_simplify_factor=  settings.bake_anim_simplify_factor,

            axis_forward= settings.axis_forward,
            axis_up= settings.axis_up,
            )

def export_USD_Main_Func(col, export_Path, settings):
    result = bpy.ops.wm.usd_export(
        filepath = str(export_Path),
        selected_objects_only=False,
        visible_objects_only= settings.visible_objects_only,
        collection = f"{col.name}",

        export_animation=   settings.export_animation,
        export_hair=        settings.export_hair,
        export_uvmaps=      settings.export_uvmaps,
        rename_uvmaps=      settings.rename_uvmaps,
        export_mesh_colors= settings.export_mesh_colors,
        export_normals=     settings.export_normals,
        export_materials=   settings.export_materials,
        export_subdivision= settings.export_subdivision,
        export_armatures=   settings.export_armatures,
        only_deform_bones=  settings.only_deform_bones,
        export_shapekeys=   settings.export_shapekeys,

        use_instancing=             settings.use_instancing,
        evaluation_mode=            settings.evaluation_mode,
        generate_preview_surface=   settings.generate_preview_surface,
        generate_materialx_network= settings.generate_materialx_network,
        convert_orientation=        settings.convert_orientation,
        export_global_forward_selection= settings.export_global_forward_selection,
        export_global_up_selection= settings.export_global_up_selection,
    
        export_textures=        settings.export_textures,
        export_textures_mode=   settings.export_textures_mode,
        overwrite_textures=     settings.overwrite_textures,
        relative_paths=         settings.relative_paths,
        xform_op_mode=          settings.xform_op_mode,

        export_custom_properties=       settings.export_custom_properties,
        custom_properties_namespace=    settings.custom_properties_namespace,
        author_blender_name=            settings.author_blender_name,
        convert_world_material=         settings.convert_world_material,
        allow_unicode=                  settings.allow_unicode,

        export_meshes=  settings.export_meshes,
        export_lights=  settings.export_lights,
        export_cameras= settings.export_cameras,
        export_curves=  settings.export_curves,
        export_points=  settings.export_points,
        export_volumes= settings.export_volumes,

        triangulate_meshes=         settings.triangulate_meshes,
        quad_method=                settings.quad_method,
        ngon_method=                settings.ngon_method,
        usdz_downscale_size=        settings.usdz_downscale_size,
        usdz_downscale_custom_size= settings.usdz_downscale_custom_size,
        merge_parent_xform=         settings.merge_parent_xform,
        convert_scene_units=        settings.convert_scene_units,
        meters_per_unit=            settings.meters_per_unit,

    )

    return result


def export_OBJ_Main_Func(col, export_Path, settings):
    result = bpy.ops.wm.obj_export(
        filepath= str(export_Path),
        export_animation=   settings.export_animation,
        start_frame=        settings.start_frame,
        end_frame=          settings.end_frame,
        forward_axis=       settings.forward_axis,
        up_axis=            settings.up_axis,
        global_scale=       settings.global_scale,

        export_selected_objects=False,

        export_uv=          settings.export_uv,
        export_normals=     settings.export_normals,
        export_colors=      settings.export_colors,
        export_materials=   settings.export_materials,
        export_pbr_extensions=  settings.export_pbr_extensions,
        path_mode=          settings.path_mode,
        export_triangulated_mesh=   settings.export_triangulated_mesh,

        export_curves_as_nurbs=     settings.export_curves_as_nurbs,
        export_object_groups=       settings.export_object_groups,
        export_material_groups=     settings.export_material_groups,
        export_vertex_groups=       settings.export_vertex_groups,
        export_smooth_groups=       settings.export_smooth_groups,
        smooth_group_bitflags=       settings.smooth_group_bitflags,

        collection=f"{col.name}",
    )

    return result


def export_DAE_Main_Func(final_objects, export_Path, settings):
    result = bpy.ops.wm.collada_export(
        filepath=str(export_Path),

        apply_modifiers=                 settings.apply_modifiers,
        export_mesh_type=               settings.export_mesh_type,
        export_mesh_type_selection=     settings.export_mesh_type_selection,
        export_global_forward_selection=settings.export_global_forward_selection,
        export_global_up_selection=     settings.export_global_up_selection,
        apply_global_orientation=       settings.apply_global_orientation,

        deform_bones_only=              settings.deform_bones_only,
        include_animations=             settings.include_animations,
        include_all_actions=            settings.include_all_actions,
        export_animation_type_selection=settings.export_animation_type_selection,

        sampling_rate=                  settings.sampling_rate,
        keep_smooth_curves=             settings.keep_smooth_curves,
        keep_keyframes=                 settings.keep_keyframes,
        keep_flat_curves=                settings.keep_flat_curves,
        active_uv_only=                 settings.active_uv_only,
        use_texture_copies=             settings.use_texture_copies,

        selected=                       True,
        triangulate=                    settings.triangulate,

        use_object_instantiation=       settings.use_object_instantiation,
        use_blender_profile=             settings.use_blender_profile,

        sort_by_name=                   settings.sort_by_name,
        export_object_transformation_type=      settings.export_object_transformation_type,
        export_object_transformation_type_selection=        settings.export_object_transformation_type_selection,

        export_animation_transformation_type=               settings.export_animation_transformation_type,
        export_animation_transformation_type_selection=     settings.export_animation_transformation_type_selection,

        open_sim=                       settings.open_sim,
        limit_precision=                settings.limit_precision,
        keep_bind_info=                 settings.keep_bind_info,
    )

    return result


def export_GLTF_Main_Func(col, export_Path, settings ):

    result = bpy.ops.export_scene.gltf(
        filepath= str(export_Path),
        check_existing=False,
        use_selection= True,
        use_visible= False,
        use_active_collection=False, 
        use_active_scene=False, 
        collection= f"{col.name}",
        use_renderable=False, 
        use_active_collection_with_nested=True, 

        export_nla_strips = True,
        export_original_specular = False,
        export_hierarchy_full_collections = False,
        export_extra_animations = False,
        export_loglevel = -1,

        export_import_convert_lighting_mode = settings.export_import_convert_lighting_mode,
        gltf_export_id = settings.gltf_export_id,
        export_use_gltfpack = settings.export_use_gltfpack,
        export_gltfpack_tc = settings.export_gltfpack_tc,
        export_gltfpack_tq = settings.export_gltfpack_tq,
        export_gltfpack_si = settings.export_gltfpack_si,
        export_gltfpack_sa = settings.export_gltfpack_sa,
        export_gltfpack_slb = settings.export_gltfpack_slb,

        export_gltfpack_vp = settings.export_gltfpack_vp,
        export_gltfpack_vt = settings.export_gltfpack_vt,
        export_gltfpack_vn = settings.export_gltfpack_vn,
        export_gltfpack_vc = settings.export_gltfpack_vc,
        export_gltfpack_vpi = settings.export_gltfpack_vpi,
        export_gltfpack_noq = settings.export_gltfpack_noq,
        export_gltfpack_kn = settings.export_gltfpack_kn,
        export_format = settings.export_format,

        ui_tab = settings.ui_tab,
        export_copyright = settings.export_copyright,
        export_image_format = settings.export_image_format,
        export_image_add_webp = settings.export_image_add_webp,
        export_image_webp_fallback = settings.export_image_webp_fallback,
        export_texture_dir = settings.export_texture_dir,
        export_jpeg_quality = settings.export_jpeg_quality,
        export_image_quality = settings.export_image_quality,
        export_keep_originals = settings.export_keep_originals,
        export_texcoords = settings.export_texcoords,
        export_normals = settings.export_normals,
        export_gn_mesh = settings.export_gn_mesh,

        export_draco_mesh_compression_enable = settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level = settings.export_draco_mesh_compression_level,
        export_draco_position_quantization = settings.export_draco_position_quantization,
        export_draco_normal_quantization = settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization = settings.export_draco_texcoord_quantization,
        export_draco_color_quantization = settings.export_draco_color_quantization,
        export_draco_generic_quantization = settings.export_draco_generic_quantization,
        export_tangents = settings.export_tangents,
        export_materials = settings.export_materials,
        export_unused_images = settings.export_unused_images,
        export_unused_textures = settings.export_unused_textures,
        export_vertex_color = settings.export_vertex_color,
        export_all_vertex_colors = settings.export_all_vertex_colors,
        export_active_vertex_color_when_no_material = settings.export_active_vertex_color_when_no_material,

        export_attributes = settings.export_attributes,
        use_mesh_edges = settings.use_mesh_edges,
        use_mesh_vertices = settings.use_mesh_vertices,
        export_cameras = settings.export_cameras,



        at_collection_center = settings.at_collection_center,
        export_extras = settings.export_extras,
        export_yup = settings.export_yup,
        export_apply = settings.export_apply,
        export_shared_accessors = settings.export_shared_accessors,
        export_animations = settings.export_animations,
        export_frame_range = settings.export_frame_range,
        export_frame_step = settings.export_frame_step,
        export_force_sampling = settings.export_force_sampling,
        export_sampling_interpolation_fallback = settings.export_sampling_interpolation_fallback,
        export_pointer_animation = settings.export_pointer_animation,
        export_animation_mode = settings.export_animation_mode,
        export_nla_strips_merged_animation_name = settings.export_nla_strips_merged_animation_name,
        export_def_bones = settings.export_def_bones,
        export_hierarchy_flatten_objs = settings.export_hierarchy_flatten_objs,
        export_armature_object_remove = settings.export_armature_object_remove,
        export_leaf_bone = settings.export_leaf_bone,

        export_optimize_animation_size = settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature = settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object = settings.export_optimize_animation_keep_anim_object,
        export_optimize_disable_viewport = settings.export_optimize_disable_viewport,
        export_negative_frame = settings.export_negative_frame,
        export_anim_slide_to_zero = settings.export_anim_slide_to_zero,
        export_bake_animation = settings.export_bake_animation,
        export_merge_animation = settings.export_merge_animation,
        export_anim_single_armature = settings.export_anim_single_armature,
        export_reset_pose_bones = settings.export_reset_pose_bones,
        export_current_frame = settings.export_current_frame,
        export_rest_position_armature = settings.export_rest_position_armature,
        export_anim_scene_split_object = settings.export_anim_scene_split_object,
        export_skins = settings.export_skins,
        export_influence_nb = settings.export_influence_nb,

        export_all_influences = settings.export_all_influences,
        export_morph = settings.export_morph,
        export_morph_normal = settings.export_morph_normal,
        export_morph_tangent = settings.export_morph_tangent,
        export_morph_animation = settings.export_morph_animation,
        export_morph_reset_sk_data = settings.export_morph_reset_sk_data,
        export_lights = settings.export_lights,
        export_try_sparse_sk = settings.export_try_sparse_sk,
        export_try_omit_sparse_sk = settings.export_try_omit_sparse_sk,
        export_gpu_instances = settings.export_gpu_instances,
        export_action_filter = settings.export_action_filter,
        export_convert_animation_pointer = settings.export_convert_animation_pointer,
    )
    return result

def pre_export_Algo_apply(col, final_objects, initial_state ):
    initial_state["hide_set"] = {obj: obj.hide_get() for obj in final_objects}
    initial_state["hide_viewport"] = {obj: obj.hide_viewport for obj in final_objects}
    initial_state["hide_render"] = {obj: obj.hide_render for obj in final_objects}

    for obj in final_objects:
        if col not in obj.users_collection:
            col.objects.link(obj)
        obj.hide_viewport = False
        obj.hide_set(False)
        obj.select_set(True)

def post_export_Algo_revert(col, final_objects, initial_state ):

    for obj in final_objects:
        col.objects.unlink(obj)
        obj.select_set(False)
        obj.hide_set( initial_state["hide_set"][obj] )
        obj.hide_viewport = initial_state["hide_viewport"][obj]
        obj.hide_render = initial_state["hide_render"][obj]

def export_FBX_Main_Func(final_objects, export_Path, settings):
    with bpy.context.temp_override(active_object = final_objects[0], selected_objects = final_objects):
        bpy.ops.export_scene.fbx(
            filepath = str(export_Path),
            check_existing=False,
            use_selection= True,
            use_visible=False,
            collection='', 

            global_scale=           settings.global_scale,
            apply_unit_scale=       settings.apply_unit_scale,
            apply_scale_options=    settings.apply_scale_options,
            use_space_transform=    settings.use_space_transform,
            bake_space_transform=   settings.bake_space_transform,
            object_types=           settings.object_types,
            
            use_mesh_modifiers=          settings.use_mesh_modifiers,
            mesh_smooth_type=           settings.mesh_smooth_type,
            colors_type=                settings.colors_type,
            prioritize_active_color=    settings.prioritize_active_color,
            use_subsurf=                settings.use_subsurf,
            use_mesh_edges=             settings.use_mesh_edges,
            use_tspace=                 settings.use_tspace,
            use_triangles=              settings.use_triangles,

            add_leaf_bones=             settings.add_leaf_bones,
            primary_bone_axis=          settings.primary_bone_axis,
            secondary_bone_axis=        settings.secondary_bone_axis,
            use_armature_deform_only=   settings.use_armature_deform_only,
            armature_nodetype=          settings.armature_nodetype,

            bake_anim=                  settings.bake_anim,
            bake_anim_use_all_bones=    settings.bake_anim_use_all_bones,
            bake_anim_use_nla_strips=   settings.bake_anim_use_nla_strips,
            bake_anim_use_all_actions = settings.bake_anim_use_all_actions,
            bake_anim_force_startend_keying= settings.bake_anim_force_startend_keying,
            bake_anim_step=             settings.bake_anim_step,
            bake_anim_simplify_factor=  settings.bake_anim_simplify_factor,

            axis_forward= settings.axis_forward,
            axis_up= settings.axis_up,
            )

def export_USD_Main_Func(col, export_Path, settings):
    result = bpy.ops.wm.usd_export(
        filepath = str(export_Path),
        selected_objects_only=False,
        visible_objects_only= settings.visible_objects_only,
        collection = f"{col.name}",

        export_animation=   settings.export_animation,
        export_hair=        settings.export_hair,
        export_uvmaps=      settings.export_uvmaps,
        rename_uvmaps=      settings.rename_uvmaps,
        export_mesh_colors= settings.export_mesh_colors,
        export_normals=     settings.export_normals,
        export_materials=   settings.export_materials,
        export_subdivision= settings.export_subdivision,
        export_armatures=   settings.export_armatures,
        only_deform_bones=  settings.only_deform_bones,
        export_shapekeys=   settings.export_shapekeys,

        use_instancing=             settings.use_instancing,
        evaluation_mode=            settings.evaluation_mode,
        generate_preview_surface=   settings.generate_preview_surface,
        generate_materialx_network= settings.generate_materialx_network,
        convert_orientation=        settings.convert_orientation,
        export_global_forward_selection= settings.export_global_forward_selection,
        export_global_up_selection= settings.export_global_up_selection,
    
        export_textures=        settings.export_textures,
        export_textures_mode=   settings.export_textures_mode,
        overwrite_textures=     settings.overwrite_textures,
        relative_paths=         settings.relative_paths,
        xform_op_mode=          settings.xform_op_mode,

        export_custom_properties=       settings.export_custom_properties,
        custom_properties_namespace=    settings.custom_properties_namespace,
        author_blender_name=            settings.author_blender_name,
        convert_world_material=         settings.convert_world_material,
        allow_unicode=                  settings.allow_unicode,

        export_meshes=  settings.export_meshes,
        export_lights=  settings.export_lights,
        export_cameras= settings.export_cameras,
        export_curves=  settings.export_curves,
        export_points=  settings.export_points,
        export_volumes= settings.export_volumes,

        triangulate_meshes=         settings.triangulate_meshes,
        quad_method=                settings.quad_method,
        ngon_method=                settings.ngon_method,
        usdz_downscale_size=        settings.usdz_downscale_size,
        usdz_downscale_custom_size= settings.usdz_downscale_custom_size,
        merge_parent_xform=         settings.merge_parent_xform,
        convert_scene_units=        settings.convert_scene_units,
        meters_per_unit=            settings.meters_per_unit,

    )

    return result


def export_OBJ_Main_Func(col, export_Path, settings):
    result = bpy.ops.wm.obj_export(
        filepath= str(export_Path),
        export_animation=   settings.export_animation,
        start_frame=        settings.start_frame,
        end_frame=          settings.end_frame,
        forward_axis=       settings.forward_axis,
        up_axis=            settings.up_axis,
        global_scale=       settings.global_scale,

        export_selected_objects=False,

        export_uv=          settings.export_uv,
        export_normals=     settings.export_normals,
        export_colors=      settings.export_colors,
        export_materials=   settings.export_materials,
        export_pbr_extensions=  settings.export_pbr_extensions,
        path_mode=          settings.path_mode,
        export_triangulated_mesh=   settings.export_triangulated_mesh,

        export_curves_as_nurbs=     settings.export_curves_as_nurbs,
        export_object_groups=       settings.export_object_groups,
        export_material_groups=     settings.export_material_groups,
        export_vertex_groups=       settings.export_vertex_groups,
        export_smooth_groups=       settings.export_smooth_groups,
        smooth_group_bitflags=       settings.smooth_group_bitflags,

        collection=f"{col.name}",
    )

    return result


def export_DAE_Main_Func(final_objects, export_Path, settings):
    result = bpy.ops.wm.collada_export(
        filepath=str(export_Path),

        apply_modifiers=                 settings.apply_modifiers,
        export_mesh_type=               settings.export_mesh_type,
        export_mesh_type_selection=     settings.export_mesh_type_selection,
        export_global_forward_selection=settings.export_global_forward_selection,
        export_global_up_selection=     settings.export_global_up_selection,
        apply_global_orientation=       settings.apply_global_orientation,

        deform_bones_only=              settings.deform_bones_only,
        include_animations=             settings.include_animations,
        include_all_actions=            settings.include_all_actions,
        export_animation_type_selection=settings.export_animation_type_selection,

        sampling_rate=                  settings.sampling_rate,
        keep_smooth_curves=             settings.keep_smooth_curves,
        keep_keyframes=                 settings.keep_keyframes,
        keep_flat_curves=                settings.keep_flat_curves,
        active_uv_only=                 settings.active_uv_only,
        use_texture_copies=             settings.use_texture_copies,

        selected=                       True,
        triangulate=                    settings.triangulate,

        use_object_instantiation=       settings.use_object_instantiation,
        use_blender_profile=             settings.use_blender_profile,

        sort_by_name=                   settings.sort_by_name,
        export_object_transformation_type=      settings.export_object_transformation_type,
        export_object_transformation_type_selection=        settings.export_object_transformation_type_selection,

        export_animation_transformation_type=               settings.export_animation_transformation_type,
        export_animation_transformation_type_selection=     settings.export_animation_transformation_type_selection,

        open_sim=                       settings.open_sim,
        limit_precision=                settings.limit_precision,
        keep_bind_info=                 settings.keep_bind_info,
    )

    return result


def export_GLTF_Main_Func(col, export_Path, settings ):

    result = bpy.ops.export_scene.gltf(
        filepath= str(export_Path),
        check_existing=False,
        use_selection= True,
        use_visible= False,
        use_active_collection=False, 
        use_active_scene=False, 
        collection= f"{col.name}",
        use_renderable=False, 
        use_active_collection_with_nested=True, 

        export_nla_strips = True,
        export_original_specular = False,
        export_hierarchy_full_collections = False,
        export_extra_animations = False,
        export_loglevel = -1,

        export_import_convert_lighting_mode = settings.export_import_convert_lighting_mode,
        gltf_export_id = settings.gltf_export_id,
        export_use_gltfpack = settings.export_use_gltfpack,
        export_gltfpack_tc = settings.export_gltfpack_tc,
        export_gltfpack_tq = settings.export_gltfpack_tq,
        export_gltfpack_si = settings.export_gltfpack_si,
        export_gltfpack_sa = settings.export_gltfpack_sa,
        export_gltfpack_slb = settings.export_gltfpack_slb,

        export_gltfpack_vp = settings.export_gltfpack_vp,
        export_gltfpack_vt = settings.export_gltfpack_vt,
        export_gltfpack_vn = settings.export_gltfpack_vn,
        export_gltfpack_vc = settings.export_gltfpack_vc,
        export_gltfpack_vpi = settings.export_gltfpack_vpi,
        export_gltfpack_noq = settings.export_gltfpack_noq,
        export_gltfpack_kn = settings.export_gltfpack_kn,
        export_format = settings.export_format,

        ui_tab = settings.ui_tab,
        export_copyright = settings.export_copyright,
        export_image_format = settings.export_image_format,
        export_image_add_webp = settings.export_image_add_webp,
        export_image_webp_fallback = settings.export_image_webp_fallback,
        export_texture_dir = settings.export_texture_dir,
        export_jpeg_quality = settings.export_jpeg_quality,
        export_image_quality = settings.export_image_quality,
        export_keep_originals = settings.export_keep_originals,
        export_texcoords = settings.export_texcoords,
        export_normals = settings.export_normals,
        export_gn_mesh = settings.export_gn_mesh,

        export_draco_mesh_compression_enable = settings.export_draco_mesh_compression_enable,
        export_draco_mesh_compression_level = settings.export_draco_mesh_compression_level,
        export_draco_position_quantization = settings.export_draco_position_quantization,
        export_draco_normal_quantization = settings.export_draco_normal_quantization,
        export_draco_texcoord_quantization = settings.export_draco_texcoord_quantization,
        export_draco_color_quantization = settings.export_draco_color_quantization,
        export_draco_generic_quantization = settings.export_draco_generic_quantization,
        export_tangents = settings.export_tangents,
        export_materials = settings.export_materials,
        export_unused_images = settings.export_unused_images,
        export_unused_textures = settings.export_unused_textures,
        export_vertex_color = settings.export_vertex_color,
        export_all_vertex_colors = settings.export_all_vertex_colors,
        export_active_vertex_color_when_no_material = settings.export_active_vertex_color_when_no_material,

        export_attributes = settings.export_attributes,
        use_mesh_edges = settings.use_mesh_edges,
        use_mesh_vertices = settings.use_mesh_vertices,
        export_cameras = settings.export_cameras,



        at_collection_center = settings.at_collection_center,
        export_extras = settings.export_extras,
        export_yup = settings.export_yup,
        export_apply = settings.export_apply,
        export_shared_accessors = settings.export_shared_accessors,
        export_animations = settings.export_animations,
        export_frame_range = settings.export_frame_range,
        export_frame_step = settings.export_frame_step,
        export_force_sampling = settings.export_force_sampling,
        export_sampling_interpolation_fallback = settings.export_sampling_interpolation_fallback,
        export_pointer_animation = settings.export_pointer_animation,
        export_animation_mode = settings.export_animation_mode,
        export_nla_strips_merged_animation_name = settings.export_nla_strips_merged_animation_name,
        export_def_bones = settings.export_def_bones,
        export_hierarchy_flatten_objs = settings.export_hierarchy_flatten_objs,
        export_armature_object_remove = settings.export_armature_object_remove,
        export_leaf_bone = settings.export_leaf_bone,

        export_optimize_animation_size = settings.export_optimize_animation_size,
        export_optimize_animation_keep_anim_armature = settings.export_optimize_animation_keep_anim_armature,
        export_optimize_animation_keep_anim_object = settings.export_optimize_animation_keep_anim_object,
        export_optimize_disable_viewport = settings.export_optimize_disable_viewport,
        export_negative_frame = settings.export_negative_frame,
        export_anim_slide_to_zero = settings.export_anim_slide_to_zero,
        export_bake_animation = settings.export_bake_animation,
        export_merge_animation = settings.export_merge_animation,
        export_anim_single_armature = settings.export_anim_single_armature,
        export_reset_pose_bones = settings.export_reset_pose_bones,
        export_current_frame = settings.export_current_frame,
        export_rest_position_armature = settings.export_rest_position_armature,
        export_anim_scene_split_object = settings.export_anim_scene_split_object,
        export_skins = settings.export_skins,
        export_influence_nb = settings.export_influence_nb,

        export_all_influences = settings.export_all_influences,
        export_morph = settings.export_morph,
        export_morph_normal = settings.export_morph_normal,
        export_morph_tangent = settings.export_morph_tangent,
        export_morph_animation = settings.export_morph_animation,
        export_morph_reset_sk_data = settings.export_morph_reset_sk_data,
        export_lights = settings.export_lights,
        export_try_sparse_sk = settings.export_try_sparse_sk,
        export_try_omit_sparse_sk = settings.export_try_omit_sparse_sk,
        export_gpu_instances = settings.export_gpu_instances,
        export_action_filter = settings.export_action_filter,
        export_convert_animation_pointer = settings.export_convert_animation_pointer,
    )
    return result