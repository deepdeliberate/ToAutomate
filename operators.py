import bpy 

class OBJECT_OT_rename_baking_objects(bpy.types.Operator):
    """ Rename the active object and make the selected object counter suffix"""
    bl_idname = "to_automte.rename_object"
    bl_label = "Rename selected object"
    bl_description = "Rename selected objects with desired suffix"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not(context.selected_objects):
            return False
        if not(context.object):
            return False
        if context.object.type == 'None':
            return False
        if context.mode != "OBJECT":
            return False
        return True
    
    def execute(self, context):
        tamt = context.scene.tamt

        LP = tamt.low_suffix
        HP = tamt.high_suffix
        move_LP = tamt.move_LP
        move_HP = tamt.move_HP

        col_LP_name = tamt.col_LP
        col_HP_name = tamt.col_HP

        if not context.active_object:
            self.report({'ERROR'},"No active object")
            return {'CANCELLED'}
        
        # Getting the active object name
        name = context.active_object.name

        if LP in name:
            if name.endswith(HP):
                name = name.replace(HP,"")
            name = name.replace( LP, "" )
        context.object.name = name + LP

        if move_LP :
            low_col = get_col(col_LP_name)
            move_obj(self, context.object, col_LP_name) 

        # Renaming and Moving active and selected objects to thier Collection
        for i , obj in enumerate(context.selected_objects):
            if not (obj == context.object) :
                obj.name = name + HP
                if i > 0:
                    obj.name += f"_{i}"
                
                if move_HP :
                    high_col = get_col(col_HP_name)
                    move_obj(self, context.object, col_LP_name) 
                


                    


#  Function to get a Collection of given name
        
def get_col(col_name):
    if not(bpy.data.collections.get(col_name)):
        my_col = bpy.data.collections.new(name = col_name)
        bpy.context.scene.collection.children.link(my_col)
    else:
        my_col = bpy.data.collections.get(col_name)

    return my_col


#  Function to move object to given collection
def move_obj(self, obj, Col):
    my_col = get_col(Col)

    old_colls = obj.users_collection

    if not(my_col in old_colls):
        my_col.objects.link(obj)
    else:
        for o in old_colls:
            if not( o == my_col):
                o.objects.unlink(obj)
        self.report({'INFO'}, "LOW Poly Object already in LP Collection")

def register_classes():
    bpy.utils.register_class(OBJECT_OT_rename_baking_objects)



def unregister_classes():
    bpy.utils.unregister_class(OBJECT_OT_rename_baking_objects)