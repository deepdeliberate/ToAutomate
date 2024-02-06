import bpy 

class OBJECT_OT_rename_baking_objects(bpy.types.Operator):
    """ Rename the active object and make the selected object counter suffix"""
    bl_idname = "to_automte.rename_object"
    bl_label = "Rename selected objects with desired suffix"

    @classmethod
    def poll(cls, context):
        if not(context.selected_objects):
            return False
        if not(context.object):
            return False
        if context.object.type == 'None':
            return False
        return True
    
    def execute(self, context):
        pass

def register_classes():
    bpy.utils.register_class(OBJECT_OT_rename_baking_objects)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_OT_rename_baking_objects)