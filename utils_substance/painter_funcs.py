def Create_PainterFile(exported_mesh_json, project_settings_json ):
    return f"""
    import substance_painter.project
    import substance_painter.textureset
    import substance_painter.exception
    import substance_painter.logging # Still import the module itself
    import time
    import os
    import json

    # REMOVED: log = substance_painter.logging.get('BlenderPipeline')
    # Direct calls to logging functions now:
    # substance_painter.logging.info()
    # substance_painter.logging.error()
    # substance_painter.logging.warning()

    try:
        mesh_file_path_in_painter = json.loads(r'''{exported_mesh_json}''')
        loaded_settings_dict = json.loads(r'''{project_settings_json}''')

        substance_painter.logging.info(f"Received mesh file path: {{mesh_file_path_in_painter}}")
        substance_painter.logging.info(f"Received project settings: {{loaded_settings_dict}}")

        if not os.path.exists(mesh_file_path_in_painter):
            substance_painter.logging.error(f"Mesh file does not exist in Painter's environment: {{mesh_file_path_in_painter}}")
            raise FileNotFoundError(f"Mesh file not found: {{mesh_file_path_in_painter}}")

        settings = substance_painter.project.Settings()
        settings.default_texture_resolution = loaded_settings_dict['default_texture_resolution']

        normal_map_format_str = loaded_settings_dict['normal_map_format']
        if hasattr(substance_painter.project.NormalMapFormat, normal_map_format_str):
            settings.normal_map_format = getattr(substance_painter.project.NormalMapFormat, normal_map_format_str)
        else:
            substance_painter.logging.warning(f"Unknown normal map format: {{normal_map_format_str}}. Using default (OpenGL).")
            settings.normal_map_format = substance_painter.project.NormalMapFormat.OpenGL

        if loaded_settings_dict['compute_tangent_space_per_fragment']:
            settings.tangent_space_mode = substance_painter.project.TangentSpace.PerFragment
        else:
            settings.tangent_space_mode = substance_painter.project.TangentSpace.PerVertex

        if loaded_settings_dict['use_uv_tile_workflow']:
            settings.project_workflow = substance_painter.project.ProjectWorkflow.UVTile
        else:
            settings.project_workflow = substance_painter.project.ProjectWorkflow.Default

        settings.import_cameras = loaded_settings_dict['import_cameras']


        substance_painter.logging.info("Checking if project is already open...")
        if substance_painter.project.is_open():
            substance_painter.logging.info("Project is open. Attempting to close it before creating a new one.")
            substance_painter.project.close()
            time.sleep(2)
            if substance_painter.project.is_open():
                substance_painter.logging.error("Failed to close existing project. Aborting new project creation.")
                raise Exception("Failed to close existing project.")
            else:
                substance_painter.logging.info("Existing project closed successfully.")

        substance_painter.logging.info(f"Attempting to create new project with mesh: {{mesh_file_path_in_painter}}")
        substance_painter.project.create(
            mesh_file_path = mesh_file_path_in_painter,
            settings = settings
        )

        if substance_painter.project.is_open():
            substance_painter.logging.info("Substance Painter project created successfully!")
        else:
            substance_painter.logging.error("Project creation failed: Project is not open after create call.")
            raise Exception("Project creation failed.")

    except Exception as e_create:
        substance_painter.logging.error(f"An error occurred during project creation in Substance Painter: {{str(e_create)}}")
        raise # Re-raise the exception to be caught by the outer script

    substance_painter.logging.info("Substance Painter script finished.")
    """