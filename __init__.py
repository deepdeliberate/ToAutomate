bl_info = {
    "name": "To Automate",
    "author": "Naman Deep",
    "version": (1,0,1),
    "blender": (4, 2, 0),
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
from . import preferences
from . import operators
from . import _refresh_
from . import props
from . import utils

_refresh_.reload_modules()

def register():
    props.register_classes()
    operators.register_classes()
    preferences.register_classes()
    panel.register_classes()
    

def unregister():
    panel.unregister_classes()
    operators.unregister_classes()
    props.unregister_classes()
    preferences.unregister_classes()