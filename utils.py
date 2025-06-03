import bpy
import os

from pathlib import Path

def exp_Col_traverse(Col , Exclude):
    # Call out the childrens
    if Col not in Exclude:
        yield Col
        for c in Col.children:
            yield from exp_Col_traverse(c, Exclude)




def rem_col(col):
    if not col:
        return
    
    bpy.context.scene.collection.children.unlink(col)
    bpy.data.collections.remove(col, do_unlink= True)

def update_mesh_path(self,context):
    if self.exp_meshPath.startswith("//"):
        fullpath_blend = bpy.path.abspath(context.blend_data.filepath)
        base_name = bpy.path.basename(context.blend_data.filepath)
        self.exp_meshPath = fullpath_blend[ : -len(base_name)] + self.exp_meshPath[2:]


def update_spp_path(self,context):
    if self.exp_sppPath.startswith("//"):
        fullpath_blend = bpy.path.abspath(context.blend_data.filepath)
        base_name = bpy.path.basename(context.blend_data.filepath)
        self.exp_sppPath = fullpath_blend[ : -len(base_name)] + self.exp_sppPath[2:]

def update_sppTex_path(self,context):
    if self.exp_sppTexPath.startswith("//"):
        fullpath_blend = bpy.path.abspath(context.blend_data.filepath)
        base_name = bpy.path.basename(context.blend_data.filepath)
        self.exp_sppTexPath = fullpath_blend[ : -len(base_name)] + self.exp_sppTexPath[2:]

def update_presets(self, context):
    items = [(str(i), context.scene.tamt.export_collection.presets[i].name, "") for i in range(len(context.scene.tamt.export_collection.presets))]
    if not items:
        items = [('0', 'No Presets', '')]
    return items

def substance_painter_path():
    paths = []
    
    curr_os = os.name

    # MACOS
    if curr_os == 'posix':
        paths.extend([
            f'/Applications/Adobe Substance 3D Painter.app/Contents/MacOS/Adobe Substance 3D Painter',
            f'/Applications/Adobe Substance 3D Painter/Adobe Substance 3D Painter.app/Contents/MacOS/Adobe Substance 3D Painter',
            f'~/Library/Application Support/Steam/steamsapps/common/Substance 3D Painter/Adobe Substance 3D Painter.app/Contents/ MacOS/Adobe Substance 3D Painter'
        ])
        for year in range(2020,2027):
            paths.extend([
                f'/Applications/Adobe Substance 3D Painter {year}.app/Contents/MacOS/Adobe Substance 3D Painter',
                f'/Applications/Adobe Substance 3D Painter/Adobe Substance 3D Painter {year}.app/Contents/MacOS/Adobe Substance 3D Painter',
                f'~/Library/Application Support/Steam/steamapps/common/Substance 3D Painter {year}/Adobe Substance 3D Painter.app/Contents/MacOS/Adobe Substance 3D Painter'
            ])
    elif curr_os == 'nt':
        # Windows
        for ch in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            paths.extend([
                #CC
                f'{ch}:\\Program Files\\Adobe\\Adobe Substance 3D Painter\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Adobe\\Adobe Substance 3D Painter\\Adobe Substance 3D Painter.exe',
                
                # Steam without 3D
                f'{ch}:\\Program Files\\Steam||steamapps\\common\\Substance Painter\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Steam\\steamapps\\common\\Substance Painter\\Adobe Substance 3D Painter.exe',
                
                # Steam with 3D
                f'{ch}:\\Program Files\\Steam\\steamapps\\common\\Substance 3D Painter\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Steam\\steamapps\\common\\Substance 3D Painter\\Adobe Substance 3D Painter.exe'
            ])
        # Windows with year
        for year in range(2020,2027):
            paths.extend([
                # CC
                f'{ch}:\\Program Files\\Adobe\\Adobe Substance 3D Painter {year}\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Adobe\\Adobe Substance 3D Painter {year}\\Adobe Substance 3D Painter.exe',
                
                # Steam without 3D
                f'{ch}:\\Program Files\\Steam||steamapps\\common\\Substance Painter {year}\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Steam\\steamapps\\common\\Substance Painter {year}\\Adobe Substance 3D Painter.exe',
                
                # Steam with 3D
                f'{ch}:\\Program Files\\Steam\\steamapps\\common\\Substance 3D Painter {year}\\Adobe Substance 3D Painter.exe',
                f'{ch}:\\Program Files (x86)\\Steam\\steamapps\\common\\Substance 3D Painter {year}\\Adobe Substance 3D Painter.exe'
            ])

    # Check each path for the current operating system and return the first one that exists
    for path in paths:
        path = os.path.expanduser(path)
        try:
            if Path(path).exists():
                return path
        except Exception as e:
            pass
    return ''

def sync_batch_presets(context):
    tamt = context.scene.tamt
    if not tamt or not tamt.export_collection:
        tamt.batch_selection_list.clear()
        return
    
    main_presets = tamt.export_collection.presets
    batch_items = tamt.batch_selection_list

    existing_batch_states = {item.name_id: item.is_selected for item in batch_items}

    batch_items.clear()

    for i, preset in enumerate(main_presets):
        item = batch_items.add()
        item.name_id = preset.name

        # Restore selection state based on preset's name
        if preset.name in existing_batch_states:
            item.is_selected = existing_batch_states[preset.name]
        else:
            item.is_selected = False

def batch_select_all_presets(context, select: bool):
    tamt = context.scene.tamt
    if tamt and tamt.batch_selection_list:
        for item in tamt.batch_selection_list:
            item.is_selected = select

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


def remove_obj(obj):
    obj = bpy.data.objects.get(obj.name)
    if obj:
        for cols in obj.users_collection:
            cols.objects.unlink(obj)
        bpy.data.objects.remove(obj, do_unlink=True)
    else:
        return
    

def sel_object(obj, suffix, s_suffix, target_col):
    c_obj = bpy.data.objects.get(( obj.name[  : -1*(len(suffix))] + s_suffix))

    if c_obj:
        if( target_col in c_obj.users_collection):
            # Present in the High poly collection
            c_obj.select_set(True)

testing = {
    'painter_path' : substance_painter_path()
}

def get_preferences(context):
    if __name__ == '__main__':
        return testing
    else:
        prefs = context.preferences.addons[__package__].preferences

        return {
            'painter_path': prefs.painter_path
        }
    
# Materials Functions

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
    if mat_name not in [m.name for m in obj.data.materials if m ]:
        obj.data.materials.append(mat)
        # print(f"Assigned material: {mat.name}")

    
    mat_index = obj.data.materials.find(mat.name)

    if mat_index != -1 and apply:
        for poly in obj.data.polygons:
            poly.material_index = mat_index
    
    return {"FINISHED"}

def rem_mat(obj):
    if obj.data.materials:
        obj.data.materials.clear()

def add_triangulate(obj , tri_name = "Export_Triangulate_T" ):
    # print('I triangulate')
    
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
    col_obj = None

    # Create empty object of Col too?
    if bpy.data.objects.get(col.name):
        # current col objec extis
        col_obj = bpy.data.objects[col.name]
    else:
        col_obj = get_empty_obj(col.name)

    for c_col in col.children:
        
        #Object named after the current Collection
        if not(bpy.data.objects.get(c_col.name)):
            new_obj= bpy.data.objects.new(c_col.name,None)
            c_col.objects.link(new_obj)
        elif bpy.data.objects[c_col.name].type == 'EMPTY' and bpy.data.objects[c_col.name].instance_type == 'COLLECTION' and bpy.data.objects[c_col.name].instance_collection:
            # Check whether empty object named col_name, and maybe it's an instance too lol
            #rename this object
            new_obj = bpy.data.objects[c_col.name] 
            new_obj.name += '_instance'
            

        else: 
            # Object with collection name exists
            new_obj=bpy.data.objects[c_col.name]
            old_cols=new_obj.users_collection
            if not c_col in old_cols:
                c_col.objects.link(new_obj)
            for o in old_cols:
                o.objects.unlink(new_obj)
        
        new_obj.parent = col_obj

        if col != bpy.context.scene.collection :
            new_obj.parent=bpy.data.objects[col.name]
        else:
            pass


        # Make collection named object first 
        # Traverse children collection
        Col_traverse(c_col)
        
    # Traverse all collection so far
    for obj in col.objects:
        if not(obj.name == col.name ):
            if not(obj.parent):
                obj.parent = get_empty_obj(col.name)



def get_empty_obj(name):
    my_col = (name)
    
    if not bpy.data.objects.get(name):
        obj = bpy.data.objects.new(name,None)
        my_col.objects.link(obj)
    else:
        # Exists
        obj = bpy.data.objects[name]
        old_cols = obj.users_collection
        if my_col not in old_cols:
            my_col.objects.link(obj)

    return obj

def Obj_retraverse(obj, rem_parent = False):

    if obj.type=='EMPTY':
        if not(bpy.data.collections.get(obj.name)):
            new_col=bpy.data.collections.new(name=obj.name)
            if not(obj.parent):
                bpy.context.scene.collection.children.link(new_col)
            else:
                # Could be error prone, if obj_parent col doesn't exist :P
                bpy.data.collections[obj.parent.name].children.link(new_col)

        else:
            new_col=bpy.data.collections.get(obj.name)
            if obj.parent:
                parent = get_col(obj.parent.name)
                if not new_col in parent.children.values():
                    # Making collection sit under correct parent_col
                    col_parents = [c2 for c2 in traverse_tree(bpy.context.scene.collection) if c2.user_of_id(new_col)]
                    
                    if not(bpy.data.collections[obj.parent.name] in col_parents ):
                        bpy.data.collections[obj.parent.name].children.link(new_col)
                    for col in col_parents:
                        if (col == bpy.data.collections[obj.parent.name]):
                            continue
                        else:
                            col.children.unlink(new_col)

        # moving to new collection and removing object from prev collection
        old_col=obj.users_collection
        if not(new_col in old_col):
            new_col.objects.link(obj)
        for o in old_col:
            if not(o.name==new_col.name):
                o.objects.unlink(obj)

        # Traver childrent of current Empty object
        for ob in obj.children:
            Obj_retraverse(ob, rem_parent)

        if rem_parent:
            obj.parent = None
            remove_obj(obj)

    else:
        #zprint(obj.name)

        # only After Traversing all parent, we un-parent child too
        if obj.parent and obj.parent.type == 'EMPTY':
            old=obj.users_collection
            new_col=get_col(obj.parent.name)
            if not(new_col in old):
                new_col.objects.link(obj)
            for o in old:
                if not(o == new_col):
                    o.objects.unlink(obj)
        if rem_parent and obj.parent.type == 'EMPTY':
            obj.parent = None
            
