from importlib import reload
import sys
import bpy
from . import *

# Use development button to enable or disable reload functionality

def reload_modules():
    if not bpy.context.preferences.view.show_developer_ui:
        return 
    reload(sys.modules[__name__])
    reload(preferences)
    reload(props)
    reload(operators)
    reload(panel)