import bpy

from . import operators
from bpy.props import IntProperty, BoolProperty, StringProperty

class OBJECT_PT_3DView_panel(bpy.types.Panel):
    """ 3D View Panel"""
    bl_label = "To Automate"
    bl_idname = "to_automate_3D_panel"
    bl_space_type = 'VIEW3D'
    bl_context = 'object'

    def draw(self, context):
        layout = self.layout
        pass


def register_classes():
    bpy.utils.register_class(OBJECT_PT_3DView_panel)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_3DView_panel)

