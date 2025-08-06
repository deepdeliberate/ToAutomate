# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 




import bpy
import bmesh
import os
import subprocess

from . import export_utils
from . import props
from . import utils
from . import utils_panel
from pathlib import Path

class OBJECT_OT_TAMT_rename(bpy.types.Operator):
    """ Rename the active object and make the selected object counter suffix"""
    bl_idname = "to_automate.rename_object"
    bl_label = "Rename selected object"
    bl_description = "Rename selected objects with desired suffix"
    bl_options = {"REGISTER", "UNDO"}

    new_name: bpy.props.StringProperty(
        name="Name",
        description="Enter the name for the active object"
    )

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
    
    def invoke(self, context, event):
        active_object = context.object
        if active_object:
            self.new_name = active_object.name
        else:
            return {'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)
    
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
        parent_col_name = tamt.rnm_ord_parent

        # rnm_ord_type , rnm_ord_3rd ,rnm_ord_parent

        if enum_rnm_method == 'OP1' or enum_rnm_method == 'OP2':
            if not context.active_object:
                self.report({'ERROR'},"No active object")
                return {'CANCELLED'}
            
        # Getting the active object name
        

        act_object = context.active_object
        hp_objects = [obj for obj in context.selected_objects if obj != act_object] 

        name = ''
        if self.new_name:
            name = self.new_name
        else:
            name = act_object.name
        obj_col_name = name

        # Making sure the basename has proper prefix and suffix
        # Can improve algorithm by using string [ : - len(LP)] 
        if LP in name:
            name = name.replace( LP, "")

        if HP in name:
            name = name.replace(HP, "")

        obj_col_name = name

        if bpy.data.objects.get(name + LP) != None :
            # Named object already exists
            print("I Tried")
            bpy.data.objects[name + LP].name = name + '_1' + LP 

        print("I Tried2")
        

        act_object.name = name + LP

        for i,obj in enumerate(hp_objects):
            if i == 0:
                obj.name = name + HP 
            else:
                obj.name = name + HP + '_' + str( i )


        if enum_rnm_method == 'OP1':
            if move_LP :
                # low_col = get_col(col_LP_name)
                utils.move_object( [context.object], col_LP_name )

            my_objs = [obj for obj in context.selected_objects if obj != context.object]
            if move_HP:
                utils.move_object( my_objs, col_HP_name )

            
        elif enum_rnm_method == 'OP2':
            # move to object collection
            col = utils.get_col(obj_col_name)
            utils.move_object( context.selected_objects, obj_col_name)

            # got the collection
            if len(parent_col_name.strip()) > 0 :
                parent_col = utils.get_col(parent_col_name)
                utils.move_col(col , parent_col)
            
            
        
        return {'FINISHED'}   
    

# Function to move and rename the High poly objects to their corresponding LP name and HP col
    






class OBJECT_OT_TAMT_select(bpy.types.Operator):
    """ Option 1:  Select the objects' significant other, 
    Option 2:  Select no matching object"""
    bl_idname = "to_automate.select_significant"
    bl_label = "Select significant other"
    bl_description = "Select the significant other / or ones that don't"
    bl_options = {'REGISTER', 'UNDO'}

    # for selection

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) >= 0

    
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
        final_selection = []

        all_objs = [o for o in context.selected_objects]
        if not(L_Col):
                self.report({'ERROR'}, "No HP Collection Found")
                return {'CANCELLED'}
        
        if not(H_Col):
            self.report({'ERROR'}, "No LP Collection Found")
            return {'CANCELLED'}

        if Select_option == 'OP1':
            bpy.ops.object.select_all(action='DESELECT')
            
            for col in {L_Col, H_Col}:
                for obj in col.objects:
                    if obj.name.endswith(LP):
                        if bpy.data.objects.get(obj.name.replace(LP, HP)):
                            pair_obj = bpy.data.objects.get(obj.name.replace(LP, HP))
                            for col in pair_obj.users_collection:
                                if col != H_Col:
                                    final_selection.append(pair_obj)
                                    self.report({'INFO'},f"{pair_obj.name} isn't in {col_HP_name} collection, found in {col.name}")
                        else:
                            self.report({'INFO'},f"{obj.name}'s pair object doesn't exist")
                            final_selection.append(obj)

                    elif obj.name.endswith(HP):
                        print(f"name {obj.name}")
                        if bpy.data.objects.get(obj.name.replace(HP, LP)):
                            pair_obj = bpy.data.objects.get(obj.name.replace(HP, LP))
                            for col in pair_obj.users_collection:
                                if col != L_Col:
                                    final_selection.append(pair_obj)
                                    self.report({'INFO'},f"{pair_obj.name} isn't in {col_HP_name} collection, found in {col.name}")
                        else:
                            self.report({'INFO'},f"{obj.name}'s pair object doesn't exist")
                            final_selection.append(obj)

                    else:
                        self.report({'INFO'},f"{obj.name} isn't named properly")
                        final_selection.append(obj)

            for obj in final_selection:
                obj.select_set(True)

            if final_selection:
                context.view_layer.objects.active = final_selection[0]
                

        
        # OP2: Selecting the significant other in the object 

        else:
            if len(context.selected_objects) == 0:
                self.report({'WARNING'},"NO Objects Selected to check")
                return {'CANCELLED'}


            if d_sel:
                bpy.ops.object.select_all(action='DESELECT')

            for obj in all_objs:
                if (obj.name.endswith(LP)):
                    pair_obj = bpy.data.objects.get( obj.name.replace(LP, HP))
                    if pair_obj:
                        if H_Col not in pair_obj.users_collection:
                            self.report({'INFO'},f"{pair_obj.name} found, but in non-LP_HP collection {pair_obj.users_collection[0].name}")
                        else:
                            final_selection.append(pair_obj)
                    else:
                        self.report({'INFO'},f"{obj.name}'s pair not found, expected {obj.name.replace(LP, HP)}")
                        


                elif (obj.name.endswith(HP)):
                    pair_obj = bpy.data.objects.get( obj.name.replace(HP, LP))
                    if pair_obj:
                        if L_Col not in pair_obj.users_collection:
                            self.report({'INFO'},f"{pair_obj.name} found, but in non-LP_HP collection {pair_obj.users_collection[0].name}")
                        else:
                            final_selection.append(pair_obj)

                    else:
                        self.report({'INFO'},f"{obj.name}'s pair not found, expected {obj.name.replace(HP, LP)}")
                        final_selection.append(obj)
                else:
                    self.report({'INFO'},f"{obj.name} isn't named properly")
                    final_selection.append(obj)

            if d_sel:
                for obj in all_objs:
                    obj.select_set(False)

            for obj in final_selection:
                obj.select_set(True)

            if final_selection:
                context.view_layer.objects.active = final_selection[0]
        

        return {'FINISHED'}

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
        return context.mode == 'OBJECT' and len(context.selected_objects) == 2
    
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

        if not(context.active_object.type == 'MESH' or context.active_object.type == 'CURVE') :
            self.report({'ERROR'}, "Incompatible Object")
            return {'CANCELLED'}
        
        s_obj = bpy.context.active_object
        mod = None
        if s_obj.modifiers:
            for m in s_obj.modifiers:
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
                            mod.offset_v = 1.0
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

        for obj in bpy.context.selected_objects:
            exist = False
            if obj.type=='MESH':
                target_uv = None
                if obj.data.uv_layers.get(uv_name) == None:
                    test = obj.data.uv_layers.new(name = uv_name)
                    if mk_active:
                        obj.data.uv_layers.active = obj.data.uv_layers[ len(obj.data.uv_layers)-1]
                        obj.data.uv_layers[len(obj.data.uv_layers)-1].active_render = True
                    
                else:
                    if mk_active:
                        for i,uv in enumerate(obj.data.uv_layers):
                            if uv.name == uv_name:
                                obj.data.uv_layers.active =  obj.data.uv_layers[i]
                                obj.data.uv_layers[i].active_render = True

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

        create = tamt.uvmap_ren_create

        if option =='OP1':
            for obj in context.selected_objects:
                exist=0
                if obj.type=='MESH':
                    for uv_tex in obj.data.uv_layers:   
                        if uv_tex==obj.data.uv_layers.active:
                            exist=1
                            uv_tex.name=uv_name
                    if not(exist) and create:
                        obj.data.uv_layers.new(name=uv_name)
        if option =='OP2':
            for obj in context.selected_objects:
                f_exist= False
                r_exist = False
                if obj.type=='MESH':
                    for uv_tex in obj.data.uv_layers:
                        if uv_tex.name==f_name:
                            f_exist=1
                            uv_tex.name=uv_name
                            if active:
                                obj.data.uv_layers.active=uv_tex

                        if uv_tex.name == uv_name:
                            r_exist = True
                        
                                
                    if (not(f_exist) and not(r_exist) and create):
                        new_uv = obj.data.uv_layers.new(name=uv_name)
                        if active:
                            obj.data.uv_layers.active=new_uv
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
                                break
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

        preset_by_name = {p.name: p for p in tamt.export_collection.presets}
        all_count = 0
        for i,preset in enumerate(tamt.export_collection.presets):
            if preset.exp_for_batch:
                tamt.export_presets.selected_preset = str(i)
                all_count += 1
                if preset:
                    try: 
                        bpy.ops.to_automate.atm_exportcol('INVOKE_DEFAULT')
                        selected_count += 1
                        self.report({'INFO'},f"Exported: '{preset.name}'")

                    except Exception as e:
                        self.report({'WARNING'}, f"Failed to export Preset '{preset.name}': {e}")
                else:
                    self.report({'WARNING'}, f"Selected preset '{preset.name}' not found in current presets. Skipping")
            
            
        tamt.export_presets.selected_preset = current_preset

        if selected_count > 0:
            add_message = ""
            if all_count - selected_count > 0:
                add_message = f"{all_count - selected_count} Preset(s) Cancelled"
            self.report({'INFO'}, f"Batch export finished: {selected_count} preset(s) exported. {add_message}")
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

        do_triangulate = preset.exp_triangulate

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
            if len(exp_name.strip()) > 0:
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
            self.report({'INFO'}, "Final Export Object count is 0")
            return {'CANCELLED'}
        
        if do_triangulate:
            for obj in final_objects:
                utils.add_triangulate(obj, "TAMT_Triangulate_T")

        # Export File Format
        if exp_format == 'FBX':
            export_ext = '.fbx'
        elif exp_format == 'OBJ':
            export_ext = '.obj'
        elif exp_format == 'USD':
            export_ext = '.usdc'
        elif exp_format == 'DAE':
            export_ext = '.dae'
        elif exp_format == 'GLTF':
            export_ext = '.glb'

        exp_mesh = ''

        abc = ""
        if mesh_export_path.startswith('//'):
            mesh_export_path = str(bpy.path.abspath(mesh_export_path+"{}.{}".format(export_final_name,export_ext)))

        # Updating the keyframe to desired Keyframe for the preset
        bpy.context.scene.frame_current = exp_targetKeyframe

        export_External_Col_name = 'TAMTEXP_'

        # ------------------------------- FBX ------------------------------


        if exp_format == 'FBX' :
            export_ext = '.fbx'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            exp_mesh = export_Path
            settings = preset.exp_FBXProperties

            export_utils.export_FBX_Main_Func(final_objects, export_Path, settings)



        # ------------------------------- USD ------------------------------


        elif exp_format == 'USD':  #USDz
            export_ext = '.usdc'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            settings = preset.exp_USDProperties

            exp_mesh = export_Path

            export_External_Col_name += export_final_name
            col = utils.get_col(export_External_Col_name)
            
            # Link all objects to an additional temp collection
            for obj in final_objects:
                col.objects.link(obj)

            export_utils.export_USD_Main_Func(col, export_Path, settings)

            # unlink objects from temp collection
            for obj in final_objects:
                col.objects.unlink(obj)

            utils.rem_col(col)

        # ------------------------------- OBJ ------------------------------


        elif exp_format == 'OBJ' :
            export_ext = '.obj'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            settings = preset.exp_OBJProperties

            exp_mesh = export_Path

            bpy.ops.object.select_all(action='DESELECT')
            
            initial_state = {
                "hide_set": None,
                "hide_viewport": None,
                "hide_render": None
            }

            export_External_Col_name += export_final_name
            col = utils.get_col(export_External_Col_name)

            export_utils.pre_export_Algo_apply(col, final_objects, initial_state)

            # Export here ----------------
            result = export_utils.export_OBJ_Main_Func(col, export_Path, settings)

            # unlink objects from temp collection
            export_utils.post_export_Algo_revert(col, final_objects, initial_state)

            utils.rem_col(col)

        # ------------------------------- DAE ------------------------------

        
        elif exp_format == 'DAE':
            export_ext = '.dae'
            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            settings = preset.exp_DAEProperties

            exp_mesh = export_Path

            bpy.ops.object.select_all(action='DESELECT')

            initial_state = {
                "hide_set": None,
                "hide_viewport": None,
                "hide_render": None
            }

            export_External_Col_name += export_final_name
            col = utils.get_col(export_External_Col_name)

            export_utils.pre_export_Algo_apply(col, final_objects, initial_state)

            # Export here ----------------
            result = export_utils.export_DAE_Main_Func(final_objects, export_Path, settings)

            export_utils.post_export_Algo_revert(col, final_objects, initial_state )

            utils.rem_col(col)
        
        # ------------------------------- GLTF ------------------------------
        elif exp_format == 'GLTF':
            export_ext = '.glb' 

            settings = preset.exp_GLTFProperties
            export_ext = '.glb' if settings.export_format == 'GLB' else '.gltf'

            export_Path = Path(mesh_export_path).joinpath(str(export_final_name + export_ext) )

            initial_state = {
                "hide_set": None,
                "hide_viewport": None,
                "hide_render": None
            }

            export_External_Col_name += export_final_name
            col = utils.get_col(export_External_Col_name)

            export_utils.pre_export_Algo_apply(col, final_objects, initial_state)

            # Export here ----------------
            result = export_utils.export_GLTF_Main_Func(col, export_Path, settings)

            export_utils.post_export_Algo_revert(col, final_objects, initial_state )

            utils.rem_col(col)


        
        if do_triangulate:
            for obj in final_objects:
                utils.rem_triangulate(obj, "TAMT_Triangulate_T")

        

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

        prefs = utils.get_addon_prefs()
        preset_type = prefs.exp_Preset_Type

        preset_map = {
            'FBX': (prefs.exp_Presets_FBX, 'default_FBX_preset'),
            'OBJ': (prefs.exp_Presets_OBJ, 'default_OBJ_preset'),
            'USD': (prefs.exp_Presets_USD, 'default_USD_preset'),
            'DAE': (prefs.exp_Presets_DAE, 'default_DAE_preset'),
            'GLTF': (prefs.exp_Presets_GLTF, 'default_GLTF_preset'),
        }

        # presets, index_prop_name = preset_map.get(preset_type, (None, None))


        new_preset.name = f"Preset {len(collection.presets)}"
        new_preset.exp_nameMethod = 'OP1'
        new_preset.exp_name = "My_mesh"
        new_preset.exp_conf_path = ""
        new_preset.exp_f_path = False
        new_preset.exp_meshSource = 'OP1'
        new_preset.exp_openSubstance = False
        new_preset.exp_triangulate = True

        new_preset.exp_format = prefs.exp_Preset_Type

        new_settings_map = {
            'FBX':new_preset.exp_FBXProperties,
            'OBJ':new_preset.exp_OBJProperties,
            'USD':new_preset.exp_USDProperties,
            'DAE':new_preset.exp_DAEProperties,
            'GLTF': new_preset.exp_GLTFProperties,
        }

        # if presets and len(presets) > 0:
        #     active_index = int(getattr(prefs, index_prop_name))
        #     if active_index >= 0  :
        #         utils.copy_expFormat_presets(presets[active_index], new_settings_map[preset_type] )
        
        # Make other formats have default settings too
        for key in preset_map.keys():
            cur_presets, cur_index_prop_name = preset_map.get(key, (None, None))
            if cur_presets and len(cur_presets) > 0:
                print(cur_index_prop_name)
                print((getattr(prefs, cur_index_prop_name)))

                active_index = int(getattr(prefs, cur_index_prop_name))

                if active_index >= 0 :
                    utils.copy_expFormat_presets(cur_presets[active_index], new_settings_map[key] )
                    

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
    bl_description = "Add Active Collection in Outliner to Include/Exclude it's object and children collection for Export"

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
    

class OBJECT_OT_TAMT_EXPORT_TYPE_SETTINGS(bpy.types.Operator):
    """Export Collections With Presets"""
    bl_idname="to_automate.atm_preset_exp_settings"
    bl_label="Export Settings"
    bl_description="Edit Export File Settings for selected"  
    bl_options={"REGISTER","UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        tamt = context.scene.tamt
        collection = tamt.export_collection

        preset_index = int(tamt.export_presets.selected_preset)
        preset = collection.presets[preset_index]

        layout.operator(TAMT_OT_PREFS_LoadPresetFromPrefs.bl_idname, text= "Load Presets")
        if preset.exp_format == 'FBX': # FBX
            utils_panel.fbx_properties(layout, preset.exp_FBXProperties)
        elif preset.exp_format == 'OBJ': # OBJ
            utils_panel.obj_properties(layout, preset.exp_OBJProperties)
        elif preset.exp_format == 'USD': # USD
            utils_panel.usd_properties(layout, preset.exp_USDProperties)
        elif preset.exp_format == 'DAE': # DAE
            utils_panel.dae_properties(layout, preset.exp_DAEProperties)
        elif preset.exp_format == 'GLTF': # GLTF
            utils_panel.gltf_properties(layout, preset.exp_GLTFProperties)

    def execute(self, context):
        
        return {'FINISHED'}


class TAMT_OT_PREFS_LoadPresetFromPrefs(bpy.types.Operator):
    bl_idname="to_automate.atm_load_preset_prefs"
    bl_label = "Load Preset from Preferences"
    bl_description = "Import Settings from Preferences Presets"
    bl_options={"REGISTER","UNDO"}

    selected_prefs_preset: bpy.props.EnumProperty(
        name= "Load Preset list",
        description= "Choose a preset from preferences",
        items= utils.update_panel_expFormat_presets,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        tamt = context.scene.tamt
        preset_collection = tamt.export_collection
        current_preset_index = int(tamt.export_presets.selected_preset)

        # this is current Preset's setting so accessing internal presets
        cur_preset = preset_collection.presets[current_preset_index]
        current_preset_type = cur_preset.exp_format

        prefs = utils.get_addon_prefs()

        prefs_preset_map = {
            'FBX': prefs.exp_Presets_FBX,
            'OBJ': prefs.exp_Presets_OBJ,
            'USD': prefs.exp_Presets_USD,
            'DAE': prefs.exp_Presets_DAE,
            'GLTF': prefs.exp_Presets_GLTF,

        }

        pref_presets = prefs_preset_map.get(current_preset_type, None)
        selected = None

        if len(pref_presets) == 0:
            self.report({'INFO'}, "No Presets to Load from")
            return {'CANCELLED'}

        try:
            index = int(self.selected_prefs_preset)
            print(index)
            if len(pref_presets) > 0:
                selected = pref_presets[index]
        except Exception as e:
            self.report({'WARNING'}, f"Invalid preset selected {e}")
            return {'CANCELLED'}
        
        current_preset_settings_map = {
            'FBX':cur_preset.exp_FBXProperties,
            'OBJ':cur_preset.exp_OBJProperties,
            'USD':cur_preset.exp_USDProperties,
            'DAE':cur_preset.exp_DAEProperties,
            'GLTF': cur_preset.exp_GLTFProperties,
        }
        
        if selected and len(pref_presets) > 0 :
            utils.copy_expFormat_presets( selected, current_preset_settings_map[current_preset_type] )

        self.report({'INFO'}, f"Successfully Imported {current_preset_type} Export Settings from {selected.preset_name}")
        return {'FINISHED'}
        

#   ---------------------------- Export Preference Operators ------------------------------



class OBJECT_OT_TAMT_PREFS_ADD_EXPPRESET(bpy.types.Operator):
    """Export Format Presets"""
    bl_idname="to_automate.atm_prefs_create_preset"
    bl_label="Add Export Format Preset"
    bl_description="Create a Preset for the selected Export Format"  
    bl_options={"REGISTER","UNDO"}

    def execute(self, context):
        prefs = utils.get_addon_prefs()
        preset_type = prefs.exp_Preset_Type

        preset_map = utils.get_expFormat_utils_map(prefs)

        presets, index_prop_name = preset_map.get(preset_type, (None, None))
            
        new_preset = presets.add()
        new_preset.preset_name = f"Preset {len(presets)}"

        current_index = str(len(presets)-1)

        setattr(prefs, index_prop_name, current_index)

        return  {'FINISHED'}


class OBJECT_OT_TAMT_PREFS_REM_EXPPRESET(bpy.types.Operator):
    bl_idname="to_automate.atm_prefs_remove_preset"
    bl_label = "Remove Current Export Preset"
    bl_description = "Remove current Preset of the selected Export Format"

    confirmed: bpy.props.BoolProperty(default = True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Delete the Active Preset?")

    def execute(self, context):

        if not self.confirmed:
            self.report({'INFO'}, "Operator Cancelled")
            return {'CANCELLED'}

        prefs = utils.get_addon_prefs()
        preset_type = prefs.exp_Preset_Type

        preset_map = utils.get_expFormat_utils_map(prefs)

        presets, index_prop_name = preset_map.get(preset_type, (None, None))
        
        if len(presets) == 0:
            self.report({'INFO'}, "No Presets to Delete")
            return {'CANCELLED'}
        
        active_index = int(getattr(prefs, index_prop_name))
        presets.remove(active_index)

        new_index = str(min(active_index, len(presets) - 1) if presets else '-1')
        setattr(prefs, index_prop_name, new_index)

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

    OBJECT_OT_TAMT_BatchSelectDeselectAll,
    OBJECT_OT_TAMT_BATCHEXPORT,
    OBJECT_OT_TAMT_EXPORTCOLL,
    OBJECT_OT_TAMT_EXPORTCOL_CREATEPRESET,
    OBJECT_OT_TAMT_EXPORTCOL_REMPRESET,
    OBJECT_OT_TAMT_EXPORTCOL_ADDCOL,
    OBJECT_OT_TAMT_EXPORTCOL_REMCOL,
    OBJECT_OT_TAMT_EXPORT_TYPE_SETTINGS,

    OBJECT_OT_TAMT_PREFS_ADD_EXPPRESET,
    OBJECT_OT_TAMT_PREFS_REM_EXPPRESET,
    TAMT_OT_PREFS_LoadPresetFromPrefs,
    

]

def register_classes():
    for c in classes:
        bpy.utils.register_class(c)


def unregister_classes():
    for c in classes:
        bpy.utils.unregister_class(c)