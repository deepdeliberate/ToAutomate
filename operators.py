
import bpy
import bmesh
import os
import subprocess

from . import props
from . import utils
from pathlib import Path

class OBJECT_OT_TAMT_rename(bpy.types.Operator):
    """ Rename the active object and make the selected object counter suffix"""
    bl_idname = "to_automate.rename_object"
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
                utils.move_obj(self, context.object, col_LP_name) 
            
            utils.move_obj_LP_HP(self, context, context.active_object , context.selected_objects, name, col_HP_name, move_HP)
            # Add functionality to rename the active object while renaming

        elif enum_rnm_method == 'OP2':
            # move to object collection
            base_obj_col = utils.get_col(obj_col_name )

            # got the collection
            if prnt_obj_col_name != "" :
                prnt_obj_col = utils.get_col(prnt_obj_col_name)
                # move_col(base_obj_col, prnt_obj_col)q
            
            # Move LP and HP both here after renaming
            if move_LP :
                # low_col = get_col(col_LP_name)
                utils.move_obj(self, context.object, obj_col_name) 
            utils.move_obj_LP_HP( self, context, context.active_object, context.selected_objects, name, obj_col_name)
            
        
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
                utils.move_mult_obj(self, low_objects, col_LP_name)
                utils.move_mult_obj(self, high_objects, col_HP_name)
            else:
                # move to object name collection
                for obj in low_objects:
                    base_obj_col_name = obj.name[ : -1*(len(LP))]  
                    utils.move_obj(self, obj, base_obj_col_name) 

                for obj in high_objects:
                    base_obj_col_name =  obj.name[ : -1*(len(HP))]
                    utils.move_obj(self,obj, base_obj_col_name) 




        
        return {'FINISHED'}   
    

# Function to move and rename the High poly objects to their corresponding LP name and HP col
    


def move_col(col, parent_col):

    if not (col in parent_col.children):
        parent_col.children.link(col)

    # Check tree traverse for any other parent of collectionq



class OBJECT_OT_TAMT_select(bpy.types.Operator):
    """ Option 1:  Select the objects' significant other, 
    Option 2:  Select no matching object"""
    bl_idname = "to_automate.select_significant"
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
                        utils.sel_object(obj, LP, HP, H_Col)
                    
                    elif(obj.name.endswith(HP)):
                        utils.sel_object(obj, HP, LP, L_Col)
            
            # Deselecting original if option enabled
            if d_sel:
                for ob in des_obj:
                    ob.select_set(False)

        return {'FINISHED'}
    
    # self layout improvement
    # sel_LP_only, sel_HP_only
    # and bug fixes

class OBJECT_OT_TAMT_COLORGANIZE(bpy.types.Operator):
    bl_idname = "to_automate.col_organize"
    bl_label = "Collection Organizer"
    bl_description = "Make Collection Heirarchy equivalent empty-parent to objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        tamt = context.scene.tamt

        org_name = tamt.ORG_name
        mk_root = tamt.ORG_option

        p_col = tamt.ORG_p_col
        if p_col == None:
            self.report({'ERROR'},"Please select a target Collection to Organize")
            return {'CANCELLED'}
        
        if mk_root:
            if len(org_name.strip()) == 0:
                self.report({'ERROR'},"Master Object Name can't be empty")
                return {'CANCELLED'}
        
        # Makes empties and parent for objects in the entire tree of this collection
        utils.Col_traverse(p_col)

        if not org_name:
            a = p_col.name

        if mk_root:
            if bpy.data.objects.get(org_name):
                root_obj = bpy.data.objects[org_name]
            else:
                root_obj = bpy.data.objects.new(org_name, None)
                context.scene.collection.objects.link(root_obj)
            
            bpy.data.objects[p_col.name].parent = root_obj
            
        return {'FINISHED'}

class OBJECT_OT_TAMT_COL_REORGANIZE(bpy.types.Operator):
    bl_idname = "to_automate.col_reorganize"
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
        src_obj = tamt.DORG_obj

        
        if src_obj == None or src_obj.type != 'EMPTY':
            self.report({'ERROR'}, "Select an Empty object to Construct Collections")
            return {'CANCELLED'}
        
        if mk_root:
            if len(root_name.strip()) == 0:
                self.report({'ERROR'},"Master Collection Name can't be empty")
                return {'CANCELLED'}
        
        col = utils.get_col(src_obj.name)
        src_name = src_obj.name

        utils.Obj_retraverse(src_obj, del_emp)

        if mk_root and root_name != src_name:
            p_col = utils.get_col(root_name)

            old_cols = [c2 for c2 in utils.traverse_tree(context.scene.collection) if c2.user_of_id(col)]
            # print(old_cols)
            if p_col not in old_cols:
                p_col.children.link(col)

            for o in old_cols:
                if (o == p_col):
                    continue
                else:
                    o.children.unlink(col)
        
        return {'FINISHED'}


# function to select the object if found in a collection


class OBJECT_OT_TAMT_MOD_MIRROR(bpy.types.Operator):
    bl_idname = "to_automate.atm_mirror"
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
                    sym_obj = utils.Global_Sym()
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
    bl_idname = "to_automate.atm_triangulate"
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
                        
                        utils.add_triangulate(obj,"Triangulate" )
                        break
                            #modify=obj.modifiers.new(name=m_name,type='TRIANGULATE')
                            
                        if enum=='OP2':
                            pass       
                if not exist:
                    if newmod:
                        utils.add_triangulate(obj, "Triangulate")
            else:
                if newmod:
                    utils.add_triangulate(obj, "Triangulate")
        return {'FINISHED'}

class OBJECT_OT_TAMT_MOD_ARRAY(bpy.types.Operator):
    bl_idname = "to_automate.atm_array"
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
    bl_idname = "to_automate.atm_wght_normal"
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

     

class OBJECT_OT_TAMT_MESH_ADDMAT(bpy.types.Operator):
    bl_idname = "to_automate.atm_addmat"
    bl_label = "Add Material"
    bl_description = "Add Material to selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    mat_name: bpy.props.StringProperty(name = "Material Name",default= "NewMat")

    @classmethod
    def poll(cls, context):
        obj = context.object
        if len(bpy.context.selected_objects) < 1:
            return False
        if obj.type != 'MESH' and obj.type != 'CURVE':
            return False
        if context.mode not in {'OBJECT', 'EDIT_MESH'}:
            return False 
        return True
        
    
    def execute(self, context):
        tamt = context.scene.tamt
        
        mat = tamt.base_mat
        apply_mat = tamt.apply_mat
        remove_old = tamt.rem_old_mat

        is_in_edit_mode = (context.object.mode == 'EDIT' ) 

        all_objs = [obj for obj in context.selected_objects]

        if mat:
            mat_name = mat.name
        elif len(self.mat_name.strip()) > 1:
            mat_name = self.mat_name
        else:
            self.report({'ERROR'}, "Empty Name won't work")
            return {'CANCELLED'}
        
        if not mat:
            mat = utils.get_mat(self.mat_name)
            tamt.base_mat = mat

        if is_in_edit_mode:
            for obj in all_objs:
                if obj.type != 'MESH':
                    continue

                mat_index = -1
                for i, slot in enumerate(obj.data.materials):
                    if slot == mat:
                        mat_index = i
                        break
                
                if mat_index == -1:
                    # Add material to the object
                    obj.data.materials.append(mat)
                    mat_index = len(obj.data.materials) - 1
                

                
                mesh = obj.data
                bm = bmesh.from_edit_mesh(mesh)
                bm.verts.ensure_lookup_table()
                bm.edges.ensure_lookup_table()
                bm.faces.ensure_lookup_table()

                face_indices = []
                for face in bm.faces:
                    if face.select:
                        for loop in face.loops:
                            face_indices.append(face.index)

                bm.free()
                bpy.ops.object.mode_set(mode = 'OBJECT')

                for id in face_indices:
                    if id >= 0 and id < len(obj.data.polygons):
                        obj.data.polygons[id].material_index = mat_index
                bpy.ops.object.mode_set(mode = 'EDIT')
                

        else:
            for obj in all_objs:
                if remove_old:
                    utils.rem_mat(obj)
                if obj.type == 'MESH' or obj.type == 'CURVE':
                    utils.add_mat(obj, mat, apply_mat, mat_name)

            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # Show Pop up only if the mat is not selected
        if (context.scene.tamt.base_mat == None):
            return context.window_manager.invoke_props_dialog(self) 
        
        else:
            # Material already selected
            return self.execute(context)
    


    
class OBJECT_OT_TAMT_MESH_REMMATS(bpy.types.Operator):
    bl_idname = "to_automate.atm_remmat"
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
            utils.rem_mat(obj)

        
        return {'FINISHED'}
            

## Clean unused mats from the selected objects

class OBJECT_OT_TAMT_MESH_CLEANMATS(bpy.types.Operator):
    bl_idname = "to_automate.atm_cleanmat"
    bl_label = "Remove Empty Materials"
    bl_description = "Remove all unused materials from object"
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
            mats_to_remove = []

            for i, slot in enumerate(obj.data.materials):

                faces_using_mat = False
                for face in obj.data.polygons:
                    if face.material_index == i:
                        faces_using_mat = True
                        break
                    
                if not faces_using_mat:
                    mats_to_remove.append(i)
        
            mats_to_remove.sort(reverse=True)

            count = 0
            if mats_to_remove:
                for i in mats_to_remove:
                    obj.data.materials.pop(index = i)
                    count += 1

                self.report({'INFO'}, f"{obj.name} got Removed {count} unused materials")


        
        return {'FINISHED'}


# UV Check Offset for Array and mirror

class OBJECT_OT_TAMT_UV_OFFCHECK(bpy.types.Operator):
    bl_idname = "to_automate.atm_uvchkoffset"
    bl_label = "Check UV Offset"
    bl_description = "Select Objects which has no UV offset in their modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        all_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']

        for obj in all_objs:
            flag = False
            if obj.modifiers:
                for mod in obj.modifiers:
                    u, v = 0,0
                    if mod.type == 'MIRROR' or mod.type == 'ARRAY':
                        if mod.offset_u == 0 and mod.offset_v == 0:
                            flag = True
                            break

            if flag:
                obj.select_set(True)
            else:
                obj.select_set(False)

        
        return {'FINISHED'}


class OBJECT_OT_TAMT_UV_OFFSET(bpy.types.Operator):
    bl_idname = "to_automate.atm_uv_addoffset"
    bl_label = "Add UV Offset"
    bl_description = "Add UV offset to Mirror and Array modifiers in object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        objects = [obj for obj in context.selected_objects if obj.type == 'MESH']

        flag = True

        for obj in objects:
            if obj.modifiers:
                for mod in obj.modifiers:
                    if mod.type == 'MIRROR' or mod.type == 'ARRAY':
                        # Alternate U V offset, so that multiple mod stack has alternate u v offset
                        if flag : 
                            mod.offset_u = 1.0 
                            flag = False
                        else : 
                            modd_offset_v = 1.0
                            flag = True
        
        return {'FINISHED'}
    
class OBJECT_OT_TAMT_UV_SplitCheck(bpy.types.Operator):
    bl_idname = "to_automate.atm_uv_islandcheck"
    bl_label = "Check UV Split island"
    bl_description = "Checks the UV islands if they are splitted"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls,context):
        return context.mode=='EDIT_MESH'
    
    def execute(self,context):
        bpy.ops.object.mode_set(mode='EDIT')
        tolerance=0
        bpy.ops.mesh.select_all(action='DESELECT')
        for obj in bpy.context.selected_objects:
            me=obj.data
            bm=bmesh.from_edit_mesh(me)
            uvl=bm.loops.layers.uv[me.uv_layers.active.name]
            for face in bm.faces:
                for loop in face.loops:
                    neighbour_loop=loop.link_loop_radial_next
                    if loop is neighbour_loop or loop.edge.seam:
                        continue
                    loop1_start_uv=loop[uvl].uv
                    loop1_end_uv=loop.link_loop_next[uvl].uv
                    loop2_start_uv=neighbour_loop[uvl].uv
                    loop2_end_uv=neighbour_loop.link_loop_next[uvl].uv
                    vert1_uv_distance=(loop1_start_uv-loop2_end_uv).length
                    vert2_uv_distance=(loop1_end_uv-loop2_start_uv).length
                    if vert1_uv_distance>tolerance or vert2_uv_distance>tolerance:
                        loop.edge.select=True
        
        return{'FINISHED'}
    
class OBJECT_OT_TAMT_UV_MARKSHARPSEAM(bpy.types.Operator):
    bl_idname="to_automate.atm_uv_marksharpseam"
    bl_label="Mark Sharp as seams"
    bl_description="Marks sharp edges as seams of selected mesh"  
    bl_options={"REGISTER","UNDO"}
    
    @classmethod
    def poll(cls,context):
        if context.mode != 'EDIT_MESH':
            return False
        return True
    
    def execute(self,context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bm = bmesh.from_edit_mesh(obj.data)
                bm.edges.ensure_lookup_table()

                mark_count = 0
                for edge in bm.edges:
                    if not edge.smooth:
                        edge.seam = True
                        mark_count += 1
                bmesh.update_edit_mesh(obj.data)
                bm.free()
        
        return {'FINISHED'}
    
class OBJECT_OT_TAMT_UV_MARKOUTERSEAM(bpy.types.Operator):
    bl_idname="to_automate.atm_uv_markboundseam"
    bl_label="Mark Boundary seams"
    bl_description="Marks seams of the boundary of selected faces of mesh"  
    bl_options={"REGISTER","UNDO"}
    
    @classmethod
    def poll(cls,context):
        return context.mode=='EDIT_MESH'
    def execute(self,context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}
    


# UV CREATE, RENAME, DELETE
class OBJECT_OT_TAMT_UV_Create(bpy.types.Operator):
    """ UV Create Menu"""
    bl_idname="to_automate.atm_uv_create"
    bl_label="Create UVMap"
    bl_description="Create UVMap for selected objects, if exists no Change"  
    bl_options={"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH' or context.mode == 'OBJECT')
    
    def execute(self, context):
        tamt = context.scene.tamt

        uv_name=tamt.uvmap_name
        mk_active=tamt.uvmap_mk_active
        # mk_activeRender=tamt.uvmap_mk_activerender

        for obj in context.selected_objects:
            exist = False
            if obj.type=='MESH':
                for uv_tex in obj.data.uv_layers:
                    if uv_tex.name==uv_name:
                        exist = True
                if not(exist):
                    obj.data.uv_layers.new(name=uv_name)
                if mk_active:
                    obj.data.uv_layers.active=obj.data.uv_layers[uv_name]
                    obj.data.uv_layers[uv_name].active_render=True
                # if mk_activeRender: 
                #     obj.data.uv_layers[uv_name].active_render=True
        return {'FINISHED'}    

class OBJECT_OT_TAMT_UV_Rename(bpy.types.Operator):
    """ UV Rename Menu"""
    bl_idname="to_automate.atm_uv_rename"
    bl_label="Rename UVMap"
    bl_description="Rename UVMap for selected objects"  
    bl_options={"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH' or context.mode == 'OBJECT')
    
    def execute(self, context):
        tamt = context.scene.tamt
        uv_name = tamt.uvmap_ren_name
        option = tamt.uvmap_ren_enum

        active = tamt.uvmap_ren_active
        f_name = tamt.uvmap_f_name
        create = tamt.uvmap_rep_name

        if option =='OP1':
            for obj in context.selected_objects:
                exist=0
                if obj.type=='MESH':
                    for uv_tex in obj.data.uv_layers:   
                        if uv_tex==obj.data.uv_layers.active:
                            exist=1
                            uv_tex.name=uv_name
                    if not(exist):
                        obj.data.uv_layers.new(name=uv_name)
        if option =='OP2':
            for obj in context.selected_objects:
                exist=0
                if obj.type=='MESH':
                    for uv_tex in obj.data.uv_layers:
                        if uv_tex.name==f_name:
                            exist=1
                            uv_tex.name=uv_name
                            if active:
                                obj.data.uv_layers.active=uv_tex
                                
                    if (not(exist) and create):
                        obj.data.uv_layers.new(name=uv_name)
                        if active:
                            obj.data.uv_layers.active=uv_tex
                            obj.data.uv_layers[uv_name].active_render=True
        return {'FINISHED'}



class OBJECT_OT_TAMT_UV_Remove(bpy.types.Operator):
    """ UV Delete Menu"""
    bl_idname="to_automate.atm_uv_delete"
    bl_label="Delete UVMap"
    bl_description="Delete UVMap for selected objects"  
    bl_options={"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' or context.mode == 'OBJECT'
    
    def execute(self, context):
        tamt = context.scene.tamt
        uv_name = tamt.uvmap_del_name
        uvr_enum = tamt.uvmap_del_enum

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if len(obj.data.uv_layers) == 0:
                    continue
                if obj.data.uv_layers:
                    for i in range(len(obj.data.uv_layers) -1, -1, -1):
                        uv_tex = obj.data.uv_layers[i]
                        if uvr_enum=='OP1':
                            if uv_tex==obj.data.uv_layers.active:
                                obj.data.uv_layers.remove(uv_tex)
                        elif uvr_enum=='OP2':
                            if uv_tex.name==uv_name:
                                obj.data.uv_layers.remove(uv_tex)
                        else:
                            # Remove except this
                            if uv_tex.name != uv_name:
                                obj.data.uv_layers.remove(uv_tex)
                else:
                    self.report({'INFO'},"Some Object has no UVs at all")
        return {'FINISHED'}
    

# Batch Export Operator

class OBJECT_OT_TAMT_BatchSycnList(bpy.types.Operator):
    bl_idname="to_automate.batch_sync_presets"
    bl_label="Sync Batch Presets"
    bl_description="Synchroize Batch Presets"  
    bl_options={"REGISTER","UNDO"}
    
    def execute(self, context):
        utils.sync_batch_presets(context)
        context.scene.tamt.batch_sync = False

        return {'FINISHED'}

class OBJECT_OT_TAMT_BatchSelectDeselectAll(bpy.types.Operator):
    bl_idname="to_automate.batch_select_deselect_all"
    bl_label="Select/Deselect All"
    bl_description="Select or Deselect all Presets"  
    bl_options={"REGISTER","UNDO"}

    select_all: bpy.props.BoolProperty(
        name="Select All",
        description="True for select all, False for deselect all",
        default=False
    )

    def execute(self, context):
        utils.batch_select_all_presets(context, self.select_all)
        return {'FINISHED'}

class OBJECT_OT_TAMT_BATCHEXPORT(bpy.types.Operator):
    """Batch Export Presets"""
    bl_idname="to_automate.atm_batchexport"
    bl_label="Batch Export"
    bl_description="Batch Export selected Presets"  
    bl_options={"REGISTER","UNDO"}

    def execute(self, context):
        tamt = context.scene.tamt
        if not tamt or not tamt.export_collection:
            self.report({'ERROR'}, "No export Presets Found")
            return {'CANCELLED'}

        selected_count = 0

        current_preset = tamt.export_presets.selected_preset

        utils.sync_batch_presets(context)

        preset_by_name = {p.name: p for p in tamt.export_collection.presets}
        
        for batch_item in tamt.batch_selection_list:
            if batch_item.is_selected :
                actual_preset = preset_by_name.get(batch_item.name_id)

                if actual_preset:
                    try:
                        active_id = list(tamt.export_collection.presets).index(actual_preset)
                    except ValueError:
                        self.report({'WARNING'}, f"Selected preset '{actual_preset.name}' not found in main collection. Skipping.")
                        continue
                    
                    tamt.export_presets.selected_preset = str(active_id)
                    context.view_layer.update()

                    try: 
                        bpy.ops.to_automate.atm_exportcol('INVOKE_DEFAULT')
                        selected_count += 1
                        self.report({'INFO'},f"Exported: '{actual_preset.name}'")

                    except Exception as e:
                        self.report({'WARNING'}, f"Failed to export Preset '{actual_preset.name}': {e}")
                else:
                    self.report({'WARNING'}, f"Selected preset '{batch_item.name_id}' not found in current presets. Skipping")
            elif batch_item.is_selected:
                self.report({'WARNING'}, f"Selected preset item has no valid link. Skipping.")
            
        tamt.export_presets.selected_preset = current_preset

        if selected_count > 0:
            self.report({'INFO'}, f"Batch export finished: {selected_count} preset(s) exported.")
            return{'FINISHED'}
        else:
            self.report({'INFO'}, "No Valid presets selected for batch export.")
            return {'CANCELLED'}
    

# Export Presets Operator ----------------------------------

class OBJECT_OT_TAMT_EXPORTCOLL(bpy.types.Operator):
    """Export Collections With Presets"""
    bl_idname="to_automate.atm_exportcol"
    bl_label="Export Collections"
    bl_description="Export Collections"  
    bl_options={"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def execute(self, context):
        tamt = context.scene.tamt
        suffix_LP = tamt.low_suffix
        suffix_HP = tamt.high_suffix

        if len(tamt.export_collection.presets) == 0:
            self.report({'INFO'}, "Please add a Preset in order to Setup Export Settings")
            return {'CANCELLED'}
    
        preset_index = int( tamt.export_presets.selected_preset)
        preset = tamt.export_collection.presets[preset_index]

        exp_saveInMain = preset.exp_inDirectory #Bool
        exp_name = preset.exp_name
        exp_nameMethod = preset.exp_nameMethod
        exp_meshSource = preset.exp_meshSource
        exp_format = preset.exp_format
        exp_meshPath = preset.exp_meshPath

        exp_openSubstance = preset.exp_openSubstance

        exp_sepSppName = preset.exp_separateSppName
        exp_sppName = preset.exp_sppName
        exp_sppPath = preset.exp_sppPath
        exp_sppTexPath = preset.exp_sppTexPath

        exp_targetKeyframe = preset.exp_targetKeyframe
        save_keyFrame = bpy.context.scene.frame_current

        preferences = utils.get_preferences(context)
        painter_path = preferences["painter_path"]

        sppFileName = "My_substance"

        avoid_suffix_check = False

        final_objects = []



        if exp_meshSource == 'OP1':
            inc_collections = preset.inc_collections
            exc_collections = preset.exc_collections

            Inc_Coll = [ c.collection for c in inc_collections ]
            Exc_Coll = [ c.collection for c in exc_collections]
                
            if len(Inc_Coll) == 0:
                self.report({'ERROR'}, "No Collection selected for export")
                return {'CANCELLED'}

            # Set for checking duplicates

            # Only exclude if they are found in the traversal of Inc_Coll:
            # Exclude fully, so don't traverse Exc_coll's childrens either

            final_cols = []
            for col in Inc_Coll:
                cur_cols = []
                cur_cols = [c for c in (utils.exp_Col_traverse( col , Exc_Coll)) ]
                final_cols += cur_cols

            
            #  Final Collections contains all needed collections

            if len(final_cols) == 0:
                self.report({'ERROR'}, "Object Count from Collections is 0")
                return {'CANCELLED'}
            
            for col in final_cols:
                for obj in col.objects:
                    final_objects.append(obj)

        elif exp_meshSource == 'OP2':
            # Selected Objects
            for obj in bpy.context.selected_objects:
                final_objects.append(obj)

        else:
            # Write Code for LP and HP Objects
            all_low_cols = [col for col in utils.exp_Col_traverse(col, []) ]
            all_high_cols = [col for col in utils.exp_Col_traverse(col, []) ]

            low_objects = []
            for obj in low_objects:
                if obj.name.endswith(suffix_LP) or avoid_suffix_check :
                    low_objects.append(obj)
            
            high_objects = []
            for obj in low_objects:
                if obj.name.endswith(suffix_HP) or avoid_suffix_check:
                    high_objects.append(obj)

            final_objects = low_objects + high_objects

        # final_objects contains all desired mesh so far

        export_final_name = 'ABC'
        # Name Algorithm ----------------------------

        if exp_nameMethod == 'OP1':
            # Project File Name
            # Project File save check
            if not(bpy.path.basename(bpy.context.blend_data.filepath)):
                self.report({'ERROR'}, "Please Save your project file first")
                return {'CANCELLED'}
            
            #Blend File name
            export_final_name = bpy.path.basename(bpy.context.blend_data.filepath).replace(".blend","")

        elif exp_nameMethod == 'OP2':
            # Custom name
            # make sure it ain't empty
            if len(exp_name.replace(" ","")) > 0:
                export_final_name = exp_name
            else:
                self.report({'ERROR'}, "Please create non-empty name")
                return {'CANCELLED'}
        
        
        
        
        # Export location path

        mesh_export_path = bpy.path.abspath('//')

        if exp_saveInMain:
            # save in base directory
            if not(bpy.path.basename(bpy.context.blend_data.filepath)):
                self.report({'ERROR'}, "Please Save your project file first")
                return {'CANCELLED'}
            
            mesh_export_path = bpy.path.abspath('//')
        
        else:
            # Save in the desired location
            if len(exp_meshPath.replace(" ", "")) == 0:
                self.report({'ERROR'}, "Please make sure the save path isn't empty")
                return {'CANCELLED'}

            mesh_export_path = exp_meshPath


        if len(final_objects) == 0:
            self.report({'ERROR'}, "Final Export Object count is 0")
            return {'CANCELLED'}

        # Export File Format
        if exp_format == 'OP1':
            export_ext = '.fbx'
        elif exp_format == 'OP2':
            export_ext = '.obj'
        else:
            export_ext = '.usdc'

        exp_mesh = ''

        abc = ""
        if mesh_export_path.startswith('//'):
            mesh_export_path = str(bpy.path.abspath(mesh_export_path+"{}.{}".format(export_final_name,export_ext)))

        # Updating the keyframe to desired Keyframe for the preset
        bpy.context.scene.frame_current = exp_targetKeyframe

        export_External_Col_name = 'TAMTEXP_'

        if exp_format == 'OP1' :
            export_ext = '.fbx'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            exp_mesh = export_Path

            with bpy.context.temp_override(active_object = final_objects[0], selected_objects = final_objects):
                bpy.ops.export_scene.fbx(
                use_selection= True,
                mesh_smooth_type='EDGE',
                use_mesh_modifiers= True,
                add_leaf_bones= False,
                use_triangles= True,
                apply_scale_options= 'FBX_SCALE_ALL',
                bake_anim= False,
                bake_anim_use_nla_strips= False,
                bake_space_transform= True,
                axis_forward='-Z',
                axis_up='Y',
                filepath = str(export_Path),
                )

        elif exp_format == 'OP2':
            export_ext = '.obj'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            exp_mesh = export_Path

            # bpy.ops.object.select_all(action='DESELECT')

            # for obj in final_objects:
            #     obj.select_set(True)
            export_External_Col_name += export_final_name
            col = utils.get_col(export_External_Col_name)
            
            # Link all objects to an additional temp collection
            for obj in final_objects:
                col.objects.link(obj)

            bpy.ops.wm.obj_export(
                filepath= str(export_Path),
                export_selected_objects=False,
                export_triangulated_mesh=True,
                forward_axis='NEGATIVE_Z',
                up_axis='Y',
                collection=f"{col.name}",
            )

            # unlink objects from temp collection
            for obj in final_objects:
                col.objects.unlink(obj)

            utils.rem_col(col)




        elif exp_format == 'OP3':
            export_ext = '.usdc'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            exp_mesh = export_Path

            # bpy.ops.object.select_all(action='DESELECT')

            # for obj in final_objects:
            #     obj.select_set(True)

            export_External_Col_name += export_final_name
            col = (export_External_Col_name)

            # Could use a key-map for {obj: obj.hide_viewport for obj in final_objs}
            # To store hide info
            # Temporary hide operator isn't available
            
            # Link all objects to an additional temp collection
            for obj in final_objects:
                col.objects.link(obj)
            
            bpy.ops.wm.usd_export(
                filepath = str(export_Path),
                selected_objects_only=False,
                visible_objects_only=False,
                use_instancing=False,
                export_textures=False,
                export_textures_mode='NEW',
                triangulate_meshes=True,
                quad_method='SHORTEST_DIAGONAL',
                ngon_method='BEAUTY',
                export_normals=True,
                export_materials=True,
                export_uvmaps=True,
                export_animation=False,
                export_curves=True,
                export_global_forward_selection='NEGATIVE_Z',
                export_global_up_selection='Y',
                collection = f"{col.name}",
            )

            # unlink objects from temp collection
            for obj in final_objects:
                col.objects.unlink(obj)

            utils.rem_col(col)
        

        # Updating the current frame to original location
        bpy.context.scene.frame_current = save_keyFrame

        # Open Substance Algorithm

        #  Accurate name for the Substance file
        if exp_sepSppName :
            if len(exp_sppName.replace(" ","")) > 0:
                sppFileNameWithExt = exp_sppName + '.spp'
            else:
                self.report({'ERROR'}, "Please create non-empty name")
                return {'CANCELLED'}
            # sppFileNameWithExt = exp_sppName + '.spp'

        else:
            sppFileNameWithExt = export_final_name + '.spp'


        exp_sppPath = Path(exp_sppPath).joinpath(sppFileNameWithExt)
        exp_sppTexPath = Path(exp_sppTexPath)

        if exp_openSubstance:
            if painter_path == '':
                self.report({'ERROR'}, 'Please specify Substance Painter path in addon preferences')
                return {'CANCELLED'}

            if not Path(painter_path).exists:
                self.report({'ERROR'}, "Substance Painter path is not valid. Please set the correct path to Substance Painter in addon Preferences")
                return {'CANCELLED'}
            
            if os.name == 'posix' and painter_path.endswith('.app'):
                painter_path = painter_path + '/Contents/MacOS/Adobe Substance 3D Painter'
            
            if os.path.isdir(painter_path):
                self.report({'ERROR'}, 'Substance Painter is set to a directory. Please set it to the executable file')
                return {'CANCELLED'}
            
            if exp_sppTexPath == '':
                self.report({'INFO'}, f'Substance textures did not have correct path set, using same path as {export_final_name}.spp')
                exp_sppTexPath = exp_sppPath
            
            
            open_substance_only = False

            try: 
                if not open_substance_only:
                    if os.name == 'nt':
                        subprocess.Popen([painter_path, '--mesh',exp_mesh , '--export-path', exp_sppTexPath , exp_sppPath] )
                    else:
                        subprocess.Popen(f'"{painter_path}" --mesh "{exp_mesh}" --export-path "{exp_sppTexPath}" "{exp_sppPath}"', shell= True)
                else:
                    if os.name == 'nt':
                        subprocess.Popen([painter_path, '--export-path', exp_sppTexPath, exp_sppPath])
                    else :
                        subprocess.Popen(f'"{painter_path}" --export-path "{exp_sppTexPath}" "{exp_sppPath}"', shell= True)
            except Exception as e:
                self.report({'ERROR'}, f'Error opening Substance Painter: {e}')
                return {'FINISHED'}
        
        self.report({'INFO'}, f"FINISHED EXPORTING")
        return {'FINISHED'}


class OBJECT_OT_TAMT_EXPORTCOL_CREATEPRESET(bpy.types.Operator):
    """Create Collection Export Preset"""
    bl_idname="to_automate.atmt_exportcol_crtpreset"
    bl_label="Create New Preset"
    bl_description="Add a new Preset for Specific Export System"  
    bl_options={"REGISTER","UNDO"}

    def execute(self, context):
        tamt = context.scene.tamt
        collection = tamt.export_collection
        new_preset = collection.presets.add()

        new_preset.name = f"Preset {len(collection.presets)}"
        new_preset.exp_nameMethod = 'OP1'
        new_preset.exp_name = "My_mesh"
        new_preset.exp_conf_path = ""
        new_preset.exp_f_path = False
        new_preset.exp_meshSource = 'OP1'
        new_preset.exp_format = 'OP1'
        new_preset.exp_openSubstance = False

        #Update the enum property items
        tamt.export_presets.selected_preset = str(len(tamt.export_collection.presets) - 1)
        return  {'FINISHED'}
    

class OBJECT_OT_TAMT_EXPORTCOL_REMPRESET(bpy.types.Operator):
    bl_idname="to_automate.atmt_exportcol_rempreset"
    bl_label = "Delete Current Preset"
    bl_description = "Delete the current Preset"

    confirmed: bpy.props.BoolProperty(default = True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Delete the Active Preset?")

    def execute(self, context):

        if self.confirmed:
            tamt = context.scene.tamt
            preset_collection = tamt.export_collection

            if len(preset_collection.presets) == 0:
                self.report({'INFO'}, "No Presets to Delete")
                return {'CANCELLED'}  
            
            preset_index = int(tamt.export_presets.selected_preset)

            name = preset_collection.presets[preset_index].name
            preset_collection.presets.remove(preset_index)

            # Update the selected preset index
            if len(preset_collection.presets) > 0:
                tamt.export_presets.selected_preset = str(min( preset_index, len(preset_collection.presets) - 1))
            else :
                tamt.export_presets.selected_preset = '0'

            self.report({'INFO'}, f"Deleted Preset: {name}")
            return {'FINISHED'}
        
        self.report({'INFO'}, "Operator Cancelled")
        return {'CANCELLED'}

    
class OBJECT_OT_TAMT_EXPORTCOL_ADDCOL(bpy.types.Operator):
    bl_idname="to_automate.atmt_exportcol_addcol"
    bl_label = "Add Collection"
    bl_description = "Add Collection to Include/Exclude it's object and children collection for Export"

    def execute(self, context):
        tamt = context.scene.tamt
        preset_index = int(tamt.export_presets.selected_preset)
        preset = tamt.export_collection.presets[preset_index]

        active_collection = context.collection
        collection_group = preset.inc_collections if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections
        if not active_collection:
            self.report({'ERROR'}, "No Active Collectioin")
            return {'CANCELLED'}
        
        # Check if the collection is already in th preset's collections

        already_present = False
        for item in collection_group:
            if item.collection == active_collection:
                already_present = True
                break
        
        if already_present:
            self.report({'WARNING'}, "Collection is already added")
            return {'CANCELLED'}
                    
            
        if preset.collection_type == 'INC_COLLECTIONS':
            item = preset.inc_collections.add()
        else:
            item = preset.exc_collections.add()

        item.collection = active_collection
        
        return {'FINISHED'}
    
class OBJECT_OT_TAMT_EXPORTCOL_REMCOL(bpy.types.Operator):
    bl_idname = "renamer.export_remove_collection"
    bl_label = "Remove Collection"
    bl_description = "Remove this collection from the group"

    index: bpy.props.IntProperty()

    def execute(self, context):
        tamt = context.scene.tamt

        preset_index = int(tamt.export_presets.selected_preset)
        preset = tamt.export_collection.presets[preset_index]

        collection_group = preset.inc_collections if preset.collection_type == 'INC_COLLECTIONS' else preset.exc_collections
        collection_group.remove(self.index)
        return {'FINISHED'}















classes = [
    OBJECT_OT_TAMT_rename,
    OBJECT_OT_TAMT_select,
    OBJECT_OT_TAMT_COLORGANIZE,
    OBJECT_OT_TAMT_COL_REORGANIZE,

    OBJECT_OT_TAMT_MOD_MIRROR,
    OBJECT_OT_TAMT_MOD_TRIANGULATE,
    OBJECT_OT_TAMT_MOD_ARRAY,
    OBJECT_OT_TAMT_MOD_WGHTNRM,
    OBJECT_OT_TAMT_MESH_ADDMAT,
    OBJECT_OT_TAMT_MESH_REMMATS,
    OBJECT_OT_TAMT_MESH_CLEANMATS,

    OBJECT_OT_TAMT_UV_OFFCHECK,
    OBJECT_OT_TAMT_UV_OFFSET,
    OBJECT_OT_TAMT_UV_SplitCheck,
    OBJECT_OT_TAMT_UV_MARKSHARPSEAM,
    OBJECT_OT_TAMT_UV_MARKOUTERSEAM,
    OBJECT_OT_TAMT_UV_Create,
    OBJECT_OT_TAMT_UV_Rename,
    OBJECT_OT_TAMT_UV_Remove,

    OBJECT_OT_TAMT_BatchSycnList,
    OBJECT_OT_TAMT_BatchSelectDeselectAll,
    OBJECT_OT_TAMT_BATCHEXPORT,
    OBJECT_OT_TAMT_EXPORTCOLL,
    OBJECT_OT_TAMT_EXPORTCOL_CREATEPRESET,
    OBJECT_OT_TAMT_EXPORTCOL_REMPRESET,
    OBJECT_OT_TAMT_EXPORTCOL_ADDCOL,
    OBJECT_OT_TAMT_EXPORTCOL_REMCOL,

]

def register_classes():
    for c in classes:
        bpy.utils.register_class(c)


def unregister_classes():
    for c in classes:
        bpy.utils.unregister_class(c)