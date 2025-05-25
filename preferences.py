import bpy

from . import operators

class ToAutomatePreferences(bpy.types.AddonPreferences):
    """ Addon preferences for ToAutomate"""
    bl_idname = __package__
    bl_label = "To Automate Addon Preferences"

    painter_path: bpy.props.StringProperty(
        name = 'Substance Painter Executable',
        default = operators.substance_painter_path(), 
        subtype= 'FILE_PATH',
        description="Path to your Substance Painter Executable"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'painter_path')


classes = (
    ToAutomatePreferences,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)