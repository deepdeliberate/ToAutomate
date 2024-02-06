bl_info = {
    "name": "To Automate",
    "author": "Naman Deep",
    "version": (1,0),
    "blender": (4, 0, 0),
    "location": "VIEW3D > Properties > To Automate",
    "description": "Addon to Partly Automate 3D Project Development",
    "category": "Learning",
}

import bpy
from . import panel
from . import preferences
from . import operators
from . import _refresh_

_refresh_.reload_modules()

def register():
    operators.register_classes()
    preferences.register_classes()
    panel.register_classes()

def unregister():
    panel.unregister_classes()
    operators.unregister_classes()
    preferences.unregsiter_classes()