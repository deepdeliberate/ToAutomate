import bpy

def TAMT_fbx_export_panel_transform(layout, operator):
    header, body = layout.panel("TAMT_FBX_export_transform", default_closed=False)
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
    header, body = layout.panel("TAMT_FBX_export_properties", default_closed=True)
    header.label(text="FBX Settings")
    if body:
        TAMT_fbx_export_panel_transform(layout, operator)
        TAMT_fbx_export_panel_geometry(layout, operator)
        TAMT_fbx_export_panel_armature(layout, operator)
        TAMT_fbx_export_panel_animation(layout, operator)
