
import bpy

from . import props

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

        # Rename Order Method Properties
        enum_rnm_method = tamt.rnm_ord_type
        crt_object_col = tamt.rnm_ord_3rd
        prnt_obj_col_name = tamt.rnm_ord_parent

        # rnm_ord_type , rnm_ord_3rd ,rnm_ord_parent

        if enum_rnm_method == 'OP1' or enum_rnm_method == 'OP2':
            if not context.active_object:
                self.report({'ERROR'},"No active object")
                return {'CANCELLED'}
            # Getting the active object name
        name = context.active_object.name

        # Collection Name per object for OP2
        obj_col_name = name

        # Making sure the basename has proper prefix and suffix
        # Can improve algorithm by using string [ : - len(LP)] 
        if LP in name:
            if name.endswith(HP):
                name = name.replace(HP,"")
                obj_col_name = obj_col_name.replace(HP)

            name = name.replace( LP, "" )
            obj_col_name = obj_col_name.replace(LP, "")
        context.active_object.name = name + LP

        if enum_rnm_method == 'OP1':
            if move_LP :
                # low_col = get_col(col_LP_name)
                move_obj(self, context.object, col_LP_name) 
            
            move_obj_LP_HP(self, context, context.active_object , context.selected_objects, name, col_HP_name, move_HP)
            # Add functionality to rename the active object while renaming

        elif enum_rnm_method == 'OP2':
            # move to object collection
            base_obj_col = get_col(obj_col_name )

            # got the collection
            if prnt_obj_col_name != "" :
                prnt_obj_col = get_col(prnt_obj_col_name)
                # move_col(base_obj_col, prnt_obj_col)q
            
            # Move LP and HP both here after renaming
            if move_LP :
                # low_col = get_col(col_LP_name)
                move_obj(self, context.object, obj_col_name) 
            move_obj_LP_HP( self, context, context.active_object, context.selected_objects, name, obj_col_name)
            
        
        else:
            low_objects = []
            high_objects = []

            for obj in context.selected_objects:
                if obj.name.endswith(LP):
                    low_objects.append(obj)

                elif obj.name.endswith(HP):
                    high_objects.append(obj)

            # Parent property option?
                    
            if not crt_object_col:
                move_mult_obj(self, low_objects, col_LP_name)
                move_mult_obj(self, high_objects, col_HP_name)
            else:
                # move to object name collection
                for obj in low_objects:
                    base_obj_col_name = obj.name[ : -1*(len(LP))]  
                    move_obj(self, obj, base_obj_col_name) 

                for obj in high_objects:
                    base_obj_col_name =  obj.name[ : -1*(len(HP))]
                    move_obj(self,obj, base_obj_col_name) 




        
        return {'FINISHED'}   
    

# Function to move and rename the High poly objects to their corresponding LP name and HP col
    
def move_obj_LP_HP( self, context, act_obj , objects, base_name, target_col_name, move_HP = True):
    tamt = context.scene.tamt

    HP = tamt.high_suffix

    # Renaming and Moving active and selected objects to thier Collection
    count = 0
    for obj in objects:
        if not (obj == act_obj) :
            cur_name = base_name + HP  

            if count > 0:
                cur_name += f"_{count}"
            count += 1
            obj.name = cur_name

            if move_HP :
                # high_col = get_col(col_HP_name)
                move_obj(self, obj, target_col_name) 

def move_col(col, parent_col):

    if not (col in parent_col.children):
        parent_col.children.link(col)

    # Check tree traverse for any other parent of collectionq



class OBJECT_OT_TAMT_select(bpy.types.Operator):
    """ Option 1:  Select the objects' significant other, 
    Option 2:  Select no matching object"""
    bl_idname = "to_automte.select_significant"
    bl_label = "Select significant other"
    bl_description = "Select the significant other / or ones that don't"
    bl_options = {'REGISTER', 'UNDO'}

    # for selection
    only_LP: bpy.props.BoolProperty(description= "Select Only Low Poly, When ON, only searches LP no HP",default= True)
    only_HP: bpy.props.BoolProperty(description= "Select Only High Poly, When ON, only searches HP no LP", default=True)

    only_col: bpy.props.BoolProperty(description="Select from Collection if ON, otherwise searches whole scene", default = True)

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align= True)
        # row.alignment = 'CENTER'

        row.label(text = "Find in: ")
        row.prop(self,'only_col', text="Collection Only")
        
        # # Low and High Only props
        # row2 = layout.column(align= True)
        # # row2.alignment = 'CENTER'
        
        # tamt = context.scene.tamt
        # Select_option = tamt.col_sel_enum

        # if Select_option == 'OP1':
        #     row2.prop(self,'only_LP', text = "Low Poly")
        #     row2.prop(self, 'only_HP', text= "High Poly")

    
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

            if not(L_Col):
                self.report({'ERROR'}, "No HP Collection Found")
                return {'CANCELLED'}
            
            if not(H_Col):
                self.report({'ERROR'}, "No LP Collection Found")
                return {'CANCELLED'}
            
            if self.only_LP:
                for obj in L_Col.objects:
                    if not((obj.name[ : -1*(len(LP))] + HP) in H_Col.objects):
                        obj.select_set(True)
            
            if self.only_HP:
                for h_obj in H_Col.objects:
                    if not((h_obj.name[  : -1*(len(HP)) ]   + LP ) in L_Col.objects):
                        obj.select_set(True)
        
        # OP2: Selecting the significant other in the object 

        else:
            if d_sel:
                des_obj = [o for o in context.selected_objects]

            # If needs to check from the scene objects
            if not(self.only_col):
                for obj in context.selected_objects:
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

class OBJECT_OT_TAMT_COLORGANIZE(bpy.types.Operator):
    bl_idname = "to_automte.col_organize"
    bl_label = "Collection Organizer"
    bl_description = "Make Collection Heirarchy equivalent empty-parent to objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        tamt = context.scene.tamt

        org_name = context.scene.tamt.ORG_name
        mk_root = context.scene.tamt.ORG_option
        
        Col_traverse(context.scene.collection)
        if not org_name:
            a = 'ROOT_PARENT'
        if mk_root:
            if not(bpy.data.objects.get(org_name)):
                col_obj = bpy.data.objects.new(org_name, None)
                context.scene.collection.objects.link(col_obj)
            else:
                col_obj = bpy.data.objects[org_name]

            for name in context.scene.collection.children.keys():
                if bpy.data.objects.get(name):
                    if (bpy.data.objects[name] == col_obj):
                        continue
                    else:
                        bpy.data.objects[name].parent = col_obj

            for obj in context.scene.collection.objects:
                if not(obj.type == 'EMPTY'):
                    obj.parent = col_obj
        return {'FINISHED'}

class OBJECT_OT_TAMT_COL_REORGANIZE(bpy.types.Operator):
    bl_idname = "to_automte.col_reorganize"
    bl_label = "Collection Revert"
    bl_description = "Convert the Empty Collection Parenting to Collections"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        tamt = context.scene.tamt

        root_name = tamt.DORG_name
        mk_root = tamt.DORG_option
        del_emp = tamt.del_emp

        all_coll = None
        
        if not root_name:
            root_name = 'MASTER Collection'
        
        if mk_root == 1:
            for obj in context.scene.objects:
                if not(obj.parent):
                    if not(bpy.data.objects.get(root_name)):
                        obj_root = bpy.data.objects.new(root_name, None)
                        context.scene.collection.objects.link(obj_root)
                    else:
                        obj_root = bpy.data.objects[root_name]
                    old = obj_root.users_collection

                    if not(context.scene.collection in old):
                        context.scene.collection.objects.link(obj_root)

                    count = 0
                    for o in old:
                        if not(o == context.scene.collection):
                            count += 1
                    
                    if count >= 1:
                        # Object already exist in other collection

                        pass
                    obj.parent = obj_root
        
        flag = False
        for obj in context.scene.objects:
            if obj and obj.type == 'EMPTY':
                if not(obj.parent):
                    flag = True
                    Col_retraverse(obj)

        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.collection.all_objects:
            if not obj.type == 'EMPTY':
                if obj.parent:
                    if obj.parent.type == 'EMPTY':
                        obj.select_set(True)

                        bpy.ops.object.parent_clear(type = 'CLEAR_KEEP_TRANSFORM')
                        obj.select_set(False)
        
        if del_emp:
            all_coll = [name for name in bpy.data.collections.values()]
            for i in range(len(all_coll)):
                if all_coll:
                    cols = all_coll.pop()
                    if bpy.data.objects.get(cols.name) != None:
                        obj = bpy.data.objects[cols.name]
                        if obj.type == 'EMPTY':
                            bpy.data.objects.remove(obj, do_unlink=True)
        
        return {'FINISHED'}


# function to select the object if found in a collection


class OBJECT_OT_TAMT_MOD_MIRROR(bpy.types.Operator):
    bl_idname = "to_automte.atm_mirror"
    bl_label = "Add Mirror"
    bl_description = "Add Mirror Modifier to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    mirror_axis: bpy.props.BoolVectorProperty(name = "Mirror Axis",
                                                default=(True, False, False),
                                                subtype= 'XYZ',
                                                )
    
    all_sym: bpy.props.BoolProperty(name="Global Sym", default= True                                
                                    )
    
    create_new : bpy.props.BoolProperty(name="Create New", default= False,
                                        description="Create New modifier even if existed"                                
                                    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)

        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        tamt = context.scene.tamt

        shift_uv = tamt.shift_uv
        newmod = tamt.NewMod
        shift_u = tamt.shift_uvu
        shift_v = tamt.shift_uvv

        for obj in context.selected_objects:
            exist = False
            if obj.modifiers:
                for mod in obj.modifiers:
                    if mod.type == 'MIRROR':
                        exist = True
                
            if exist and not newmod :
                continue
            else:
                # Create new modifier
                mod = obj.modifiers.new(name = 'My_Mirror', type = 'MIRROR')
                if self.all_sym:
                    sym_obj = Global_Sym()
                    mod.mirror_object = sym_obj

                mod.use_axis[0] = self.mirror_axis[0]
                mod.use_axis[1] = self.mirror_axis[1]
                mod.use_axis[2] = self.mirror_axis[2]

                if shift_uv:
                    if shift_u:
                        mod.offset_u = 1.0
                    if shift_v:
                        mod.offset_v = 1.0
                            
        return {'FINISHED'}
    

class OBJECT_OT_TAMT_MOD_TRIANGULATE(bpy.types.Operator):
    bl_idname = "to_automte.atm_triangulate"
    bl_label = "Add Triangulate"
    bl_description = "Add Triangulate Modifier to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        tamt = context.scene.tamt

        newmod = tamt.NewMod

        for obj in context.selected_objects:
            n=0
            exist=False
            if obj.modifiers:
                for i,modifier in enumerate(obj.modifiers):
                    n+=1
                    if modifier.type=="TRIANGULATE":
                        exist=True
                        modifier.keep_custom_normals = True
                        m_name=modifier.name
                        obj.modifiers.remove(modifier)
                        
                        add_triangulate(obj,"Triangulate" )
                        break
                            #modify=obj.modifiers.new(name=m_name,type='TRIANGULATE')
                            
                        if enum=='OP2':
                            pass       
                if not exist:
                    if newmod:
                        add_triangulate(obj, "Triangulate")
            else:
                if newmod:
                    add_triangulate(obj, "Triangulate")
        return {'FINISHED'}

class OBJECT_OT_TAMT_MOD_ARRAY(bpy.types.Operator):
    bl_idname = "to_automte.atm_array"
    bl_label = "Add Dynamic Array"
    bl_description = "Dynamic Array makes active object have it's array as difference of position compared to second object"
    bl_options = {'REGISTER', 'UNDO'}

    Mod_Mir_Axes: bpy.props.BoolVectorProperty(name = "Array Axis",
                                            default=(True, False, False),
                                            subtype='XYZ',
                                            )
    
    create_new : bpy.props.BoolProperty(name="Create New", default= False,
                                        description="Create New modifier even if existed"                                
                                    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self)

        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        tamt = context.scene.tamt

        shift_uv = tamt.shift_uv
        shift_u = tamt.shift_uvu
        shift_v = tamt.shift_uvv

        Mod_loc_X = self.Mod_Mir_Axes[0]
        Mod_loc_Y = self.Mod_Mir_Axes[1]
        Mod_loc_Z = self.Mod_Mir_Axes[2]

        val_UV_X = 1.0
        val_UV_Y = 1.0

        if not shift_u :
            val_UV_X = 0.0
        if not shift_v :
            val_UV_Y = 0.0

        if not context.active_object:
           self.report({'ERROR'}, "No active object")
           return {'CANCELLED'}
        if len(context.selected_objects) != 2:
           self.report({'ERROR'}, "You must select two objects")
           return {'CANCELLED'}
        
        s_obj = bpy.context.active_object
        mod = None
        if s_obj.modifiers:
            for m in obj.modifiers:
                if m.type == 'ARRAY' and m.name == 'D_Array':
                    mod = m
                    break
        if not mod or self.create_new:        
            mod = s_obj.modifiers.new(name="D_Array",type='ARRAY')

        mod.use_relative_offset = False

        mod.use_constant_offset = True
        C_Loc = [ Mod_loc_X, Mod_loc_Y , Mod_loc_Z ]

        for obj in bpy.context.selected_objects:
            if (obj != s_obj ):
                for i in range(0,3):
                    if C_Loc[i]:
                        mod.constant_offset_displace[i] = obj.location[i] - s_obj.location[i]
                if shift_uv:
                    mod.offset_u = val_UV_X
                    mod.offset_v = val_UV_Y
        
        return {'FINISHED'}
    

class OBJECT_OT_TAMT_MOD_WGHTNRM(bpy.types.Operator):
    bl_idname = "to_automte.atm_wght_normal"
    bl_label = "Add Weighted Normal"
    bl_description = "Add Weighted Normal Modifier to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        if len (context.selected_objects) < 1:
            self.report({'WARNING'}, "Please select at least one object")
            return {'CANCELLED'}
        
        for obj in context.selected_objects:
            a = False
            for mod in obj.modifiers:
                if mod.type == 'WEIGHTED_NORMAL':
                    a = True
                    mod.keep_sharp = True
            if not a:
                #Means we need to add the modifier 
                mod = obj.modifiers.new(name = 'WeightedNormal', type = 'WEIGHTED_NORMAL')    
                mod.keep_sharp = True
        
        return {'FINISHED'}     

class OBJECT_OT_TAMT_MOD_ADDMAT(bpy.types.Operator):
    bl_idname = "to_automte.atm_addmat"
    bl_label = "Add Material"
    bl_description = "Add Material to selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    mat_name: bpy.props.StringProperty(name = "Material Name",default= "MarkUV")

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        tamt = context.scene.tamt
        
        mat = tamt.base_mat
        apply_mat = tamt.apply_mat
        remove_old = tamt.rem_old_mat
        
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Please select some objects")
            return {'CANCELLED'}
        
        if mat:
            mat_name = mat.name
        elif len(self.mat_name) > 0 :
            mat_name = self.mat_name
        else:
            self.report({'ERROR'}, "Please select some objects")
            return {'CANCELLED'}

        all_objs = context.selected_objects
        for obj in all_objs:
            if remove_old:
                rem_mat(obj)
            if obj.type == 'MESH':
                add_mat(obj, mat_name, mat)

        if not mat:
            mat = get_mat(mat_name)
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Show Pop up only if the mat is not selected
        if (context.scene.tamt.base_mat == None):
            return context.window_manager.invoke_props_dialog(self) 
        
        else:
            # Material already selected
            return self.execute(context)
    


    
class OBJECT_OT_TAMT_MOD_REMMATS(bpy.types.Operator):
    bl_idname = "to_automte.atm_remmat"
    bl_label = "Remove Materials"
    bl_description = "Remove all materials of selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        if len(bpy.context.selected_objects) < 1:
            return False
        if obj.type != 'MESH' and obj.type != 'CURVE':
            return False
        return True

    def execute(self, context):
        tamt = context.scene.tamt

        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Please select some objects")
            return {'CANCELLED'}

        all_objs = [obj for obj in context.selected_objects if obj.type == 'MESH' or obj.type == 'CURVE']
        for obj in all_objs:
            rem_mat(obj)

        
        return {'FINISHED'}
            
def get_mat(mat_name = 'Base_Mat'):
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
    
    return mat


def add_mat (obj ,mat, apply , mat_name = 'New_Mat') :
    exist_mat = False

    if ( mat is None) :
        if mat_name in bpy.data.materials:
            mat = bpy.data.materials[mat_name]
        
        else:
            mat = bpy.data.materials.new(mat_name)
            mat.use_nodes = True
    
    assign = True
    # Checking if the material already exists in the object mats
    if mat_name not in [m.name for m in obj.data.materials]:
        obj.data.materials.append(mat)
        print(f"Assigned material: {mat.name}")

    
    mat_index = obj.data.materials.find(mat.name)

    if mat_index != -1 and apply:
        for poly in obj.data.polygons:
            poly.material_index = mat_index
    
    return {"FINISHED"}

def rem_mat(obj):
    if obj.data.materials:
        obj.data.materials.clear()

def add_triangulate(obj , tri_name = "Export_Triangulate_T" ):
    print('I triangulate')
    
    if obj.type=='MESH':
        if obj.modifiers:
            index_tri = -1
            index_wt = -1
            for i,mod in enumerate(obj.modifiers):
#                if mod.type == 'WEIGHTED_NORMAL':
#                    index_wt = i
                if mod.type == 'TRIANGULATE':
                    index_tri = i
                    mod.keep_custom_normals = True
            
            if index_tri != -1 and index_wt != -1:
                # Triangle exists
                if index_wt > index_tri :
                    # Trianle is at right location, no need to move
                    pass
                else:
                    #move_above( obj , index_tri, index_wt)
                    bpy.ops.object.modifier_move_to_index({'object':obj},modifier=obj.modifiers[index_tri].name, index=index_wt)
                    modify.keep_custom_normals = True
            elif index_wt != -1:
                # add triangle above the index_wt
                modify=obj.modifiers.new(name=tri_name,type='TRIANGULATE')
                
                bpy.ops.object.modifier_move_to_index({'object':obj}, modifier=modify.name, index=index_wt)
                modify.keep_custom_normals = True
            
            elif index_tri == -1:
                # just add triangulate
                modify=obj.modifiers.new(name=tri_name,type='TRIANGULATE')
                modify.keep_custom_normals = True
        else:
            modify=obj.modifiers.new(name=tri_name,type='TRIANGULATE')
            modify.keep_custom_normals = True
    return obj


def rem_triangulate(obj , tri_name = "Export_Triangulate_T"):
    if obj.type=='MESH':
        i = 0
        for modify in obj.modifiers:
            if modify.name==tri_name:
                if i != len(obj.modifiers)-1:
                    if obj.modifiers[i+1].type == 'WEIGHTED_NORMAL':
                        # Triangulate for Weighted normal
                        modify.name = "Triangulate"
                    else:
                        obj.modifiers.remove(modify)
                else:
                    obj.modifiers.remove(modify)
                    
            i += 1
    return obj

def Global_Sym():
    name = bpy.context.scene.sym_obj_name  
    if not(bpy.data.objects.get(name)):
        o=bpy.data.objects.new(name,None)
        bpy.context.scene.collection.objects.link(o)
    else:
        o=bpy.data.objects[name]
    
    o.empty_display_size=1
    o.empty_display_type='PLAIN_AXES'
    return o

def traverse_tree(col):
    yield col
    for col2 in col.children:
        yield from traverse_tree(col2)    
        

def Col_traverse(col):
    for c_col in col.children:
        
        #Object named after the current Collection
        if not(bpy.data.objects.get(c_col.name)):
            new_obj= bpy.data.objects.new(c_col.name,None)
            c_col.objects.link(new_obj)
        else:   #handling if obj already present.(second method Can be also used as either rename existing object having a $ or any sign to differentiate)
            new_obj=bpy.data.objects[c_col.name]
            old=new_obj.users_collection
            if not c_col in old:
                c_col.objects.link(new_obj)
            for o in old:
                o.objects.unlink(new_obj)
        if col==bpy.context.scene.collection :
            pass
        elif col== bpy.context.scene.collection:
            pass
        else:
            new_obj.parent=bpy.data.objects[col.name]
        #Make collection named object first 
        
        Col_traverse(c_col)
    for obj in col.objects:
        if not(obj.name==col.name) and not(col.name=='Master Collection'):
            if not(obj.parent):
                obj.parent = get_empty_obj(col.name)
                obj.parent=bpy.data.objects[col.name]    
        if(obj.name==col.name):
            obj.parent=bpy.data.objects[col.name].parent


def get_empty_obj(name):
    cols = get_col(name)
    obj = bpy.data.objects.new(name,None)
    cols.objects.link(obj)

    return obj

def Col_retraverse(obj):
    if obj.type=='EMPTY':
        if not(bpy.data.collections.get(obj.name)):
            new_col=bpy.data.collections.new(name=obj.name)
            if not(obj.parent):
                bpy.context.scene.collection.children.link(new_col)
            else:
                bpy.data.collections[obj.parent.name].children.link(new_col)
        else:
            new_col=bpy.data.collections.get(obj.name)
            if obj.parent:
                sub=[c2 for c2 in traverse_tree(bpy.context.scene.collection) if c2.user_of_id(new_col)]
                if not(bpy.data.collections[obj.parent.name] in sub):
                    bpy.data.collections[obj.parent.name].children.link(new_col)
                for co in sub:
                    if not(co==bpy.data.collections[obj.parent.name]):
                        co.children.unlink(new_col)
        old_col=obj.users_collection
        if not(new_col in old_col):
            new_col.objects.link(obj)
        for o in old_col:
            if not(o.name==new_col.name):
                o.objects.unlink(obj)
        for ob in obj.children:
            Col_retraverse(ob)
    else:
        #zprint(obj.name)
        if obj.parent:
            old=obj.users_collection
            new_col=bpy.data.collections[obj.parent.name]
            if not(new_col in old):
                new_col.objects.link(obj)
            for o in old:
                if not(o == new_col):
                    o.objects.unlink(obj)

                            
def sel_object(obj, suffix, s_suffix, target_col):

    c_obj = bpy.data.objects.get(( obj.name[  : -1*(len(suffix))] + s_suffix))

    if c_obj:
        if( target_col in c_obj.users_collection):
            # Present in the High poly collection
            c_obj.select_set(True)




#  Function to get a Collection of given name

def get_col(col_name ):

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
        self.report({'INFO'}, f"{o.name} Object already in {Col} Collection")

def move_mult_obj(self, all_obj, Col):
    my_col = get_col(Col)

    for obj in all_obj:
        old_colls = obj.users_collection

        if not(my_col in old_colls):
            my_col.objects.link(obj)
        for o in old_colls:
            if not( o == my_col):
                o.objects.unlink(obj)
            self.report({'INFO'}, f"{o.name} Object already in {Col} Collection")


classes = [
    OBJECT_OT_TAMT_rename,
    OBJECT_OT_TAMT_select,
    OBJECT_OT_TAMT_COLORGANIZE,
    OBJECT_OT_TAMT_COL_REORGANIZE,

    OBJECT_OT_TAMT_MOD_MIRROR,
    OBJECT_OT_TAMT_MOD_TRIANGULATE,
    OBJECT_OT_TAMT_MOD_ARRAY,
    OBJECT_OT_TAMT_MOD_WGHTNRM,
    OBJECT_OT_TAMT_MOD_ADDMAT,
    OBJECT_OT_TAMT_MOD_REMMATS,

]

def register_classes():
    for c in classes:
        bpy.utils.register_class(c)


def unregister_classes():
    for c in classes:
        bpy.utils.unregister_class(c)