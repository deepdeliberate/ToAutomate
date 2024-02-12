import bpy

class ToAutomatePreferences(bpy.types.AddonPreferences):
    """ Addon preferences for ToAutomate"""
    bl_idname = __package__
    bl_label = "To Automate Addon Preferences"

    def draw(self, context):
        pass



def register_classes():
    bpy.utils.register_class(ToAutomatePreferences)

def unregister_classes():
    bpy.utils.unregister_class(ToAutomatePreferences)