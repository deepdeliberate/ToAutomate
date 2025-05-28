import bpy
import os

from pathlib import Path

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