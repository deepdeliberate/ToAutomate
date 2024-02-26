
import bpy

class OBJECT_OT_TAMT_rename(bpy.types.Operator):
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
        context.active_object.name = name + LP

        if move_LP :
            # low_col = get_col(col_LP_name)
            move_obj(self, context.object, col_LP_name) 

        # Add functionality to rename the active object while renaming

        count = 0
        # Renaming and Moving active and selected objects to thier Collection
        for obj in context.selected_objects:
            if not (obj == context.active_object) :
                cur_name = name + HP  
                if count > 0:
                    cur_name += f"_{count}"
                count += 1
                obj.name = cur_name


                if move_HP :
                    # high_col = get_col(col_HP_name)
                    move_obj(self, obj, col_HP_name) 
        
        return {'FINISHED'}      

class OBJECT_OT_TAMT_select(bpy.types.Operator):
    """ Option 1:  Select the objects' significant other, 
    Option 2:  Select no matching object"""
    bl_idname = "to_automte.select_significant"
    bl_label = "Select significant other"
    bl_description = "Select the significant other / or ones that don't"
    bl_options = {'REGISTER', 'UNDO'}

    # for selection
    only_LP: bpy.props.BoolProperty(default= True)
    only_HP: bpy.props.BoolProperty(default=True)

    only_col: bpy.props.BoolProperty(default = True)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
    def execute(self, context):
        tamt = context.scene.tamt

        LP = tamt.low_suffix
        HP = tamt.high_suffix
        move_LP = tamt.move_LP
        move_HP = tamt.move_HP

        d_sel = tamt.opt_col_sel

        Select_option = tamt.col_sel_enum

        col_LP_name = tamt.col_LP
        col_HP_name = tamt.col_HP

        L_Col = bpy.data.collections.get(col_LP_name)
        H_Col = bpy.data.collections.get(col_HP_name)

        # OP1: Selecting the objects with no significant others

        if Select_option == 'OP1':
            for obj in context.scene.objects: obj.select_set(False)

            if not(bpy.data.collections.get(col_HP_name)):
                self.report({'ERROR'}, "No HP Collection Found")
                return {'CANCELLED'}
            
            if self.only_LP:
                for obj in L_Col.objects:
                    if ((obj.name[ : -1*(len(LP))] + HP) in H_Col.objects):
                        obj.select_set(True)
            
            if self.only_HP:
                for h_obj in H_Col.objects:
                    if ((h_obj.name[  : -1*(len(HP)) ]   + LP ) in L_Col.objects):
                        obj.select_set(True)
        
        # OP2: Selecting the significant other in the object 

        else:
            if d_sel:
                des_obj = [o for o in context.selected_objects]

            if not(self.only_col):
                for obj in context.selectable_objects:
                    if(obj.name.endswith(LP )):
                        ob = bpy.data.objects.get( obj.name[  : -1*(len(LP))] + HP)
                        if ob:
                            # Set object to visible collection
                            ob.select_set(True)

                    elif(obj.name.endswith(HP)):
                        ob = bpy.data.objects.get( obj.name[  : -1*(len(HP))] + LP)
                        if ob:
                            ob.select_set(True)
            else:

                # if object is LP check in HP Collection
                # If it's significant other is there?

                for obj in context.selected_objects:
                    if (obj.name.endswith(LP)):
                        sel_object(obj, LP, HP, H_Col)
                    
                    elif(obj.name.endswith(HP)):
                        sel_object(obj, HP, LP, L_Col)
            
            # Deselecting original if option enabled
            if d_sel:
                for ob in des_obj:
                    ob.select_set(False)

        return {'FINISHED'}
    
    # self layout improvement
    # sel_LP_only, sel_HP_only
    # and bug fixes

            

# function to select the object if found in a collection
                            
def sel_object(obj, suffix, s_suffix, target_col):

    c_obj = bpy.data.objects.get(( obj.name[  : -1*(len(suffix))] + s_suffix))

    if c_obj:
        if( target_col in c_obj.users_collection):
            # Present in the High poly collection
            c_obj.select_set(True)




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
    for o in old_colls:
        if not( o == my_col):
            o.objects.unlink(obj)
        self.report({'INFO'}, f"{o.name} Object already in LP Collection")


classes = [
    OBJECT_OT_TAMT_rename,
    OBJECT_OT_TAMT_select,
]

def register_classes():
    for c in classes:
        bpy.utils.register_class(c)


def unregister_classes():
    for c in classes:
        bpy.utils.unregister_class(c)