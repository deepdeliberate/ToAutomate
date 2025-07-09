# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 





from importlib import reload
import sys
import bpy
from . import *

# Use development button to enable or disable reload functionality

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return 
    reload(sys.modules[__name__])
    reload(props)
    reload(preferences)
    reload(operators)
    reload(panel)
    reload(utils)
    reload(utils_panel)