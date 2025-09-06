# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 


bl_info = {
    "name": "ToAutomate",
    "author": "Naman Deep",
    "version": (1,0,6),
    "blender": (4, 5, 0),
    "location": "VIEW3D > Properties > To Automate",
    "description": "Addon to Partly Automate 3D Project Development",
    "category": "3D View",
}

import bpy

from bpy.types import Operator
from bpy.props import StringProperty
from bpy.props import BoolProperty
# from bpy.props import Panel

from . import panel
from . import props
from . import preferences
from . import operators
from . import _refresh_
from . import utils
from . import utils_panel
from . import export_utils

_refresh_.reload_modules()

def register():
    props.register_classes()
    preferences.register_classes()
    operators.register_classes()
    panel.register_classes()


def unregister():
    panel.unregister_classes()
    operators.unregister_classes()
    props.unregister_classes()
    preferences.unregister_classes()