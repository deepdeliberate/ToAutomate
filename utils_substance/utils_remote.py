import bpy
import sys
import subprocess
import json
import time
import textwrap

from . import remotePainter
from . import painter_funcs
from .. import utils


def remoteStart( code_list ,exported_mesh_path, project_settings, painter_path):
    exported_mesh_json = json.dumps(exported_mesh_path)
    project_settings_json = json.dumps(project_settings)

    painter_client = remotePainter.RemotePainter()
    
    painter_process = subprocess.Popen([painter_path, "--enable-remote-scripting"])

    # Changeable parameters for efficiency
    max_retries = 20
    retry_delay = 3
    connected = False

    for i in range(max_retries):
        try:
            print(f"Attempting to connect to Substance Painter (Attempt {i+1}/{max_retries})...")
            painter_client.checkConnection()
            print("Successfully connected to Substance 3D Painter!")
            connected = True
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    if not connected:
        print("Failed to connect to Substance Painter after multiple retries. Terminating Painter process.")
        painter_process.terminate()
        sys.exit(1)

    # useful for modular code execution list
    
    code_to_execute = painter_funcs.Create_PainterFile(exported_mesh_json, project_settings_json)


    try:
        print("Sending project creation script to Substance Painter...")
        response = painter_client.execScript(code_to_execute, "python")
        print("Project creation script response (if any):", response)
    except remotePainter.ExecuteScriptError as e:
        print(f"Error executing project creation script in Painter: {e}")
    except Exception as e:
        print(f"An unexpected error occurred when sending script to Painter: {e}")

    