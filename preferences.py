# 
# Developed by Naman Deep
# 
# You may use this addon in personal or commercial Blender projects.
# Redistribution or resale without explicit permission is strictly prohibited.
#
# This file is part of the "ToAutomate" Blender Addon
# For support or inquiries, contact @ https://github.com/deepdesperate 




import bpy

from . import props
from . import utils
from . import utils_panel

class ToAutomatePreferences(bpy.types.AddonPreferences):
    """ Addon preferences for ToAutomate"""
    bl_idname = __package__
    bl_label = "To Automate Addon Preferences"

    first_run_complete: bpy.props.BoolProperty(default= False, options= {'HIDDEN'})

    painter_path: bpy.props.StringProperty(
        name = 'Substance Painter Executable',
        default = utils.substance_painter_path(), 
        subtype= 'FILE_PATH',
        description="Path to your Substance Painter Executable"
    )


    exp_Preset_Type: bpy.props.EnumProperty(
        name= "Select Preset Type",
        description="Select Preset type to create/choose the default preset for it",
        items=[
            ('FBX', "FBX_Presets", "FBX Export presets"),
            ('OBJ', "OBJ Presets", "OBJ Export presets"),
            ('USD', "USD_Presets", "USD Export presets"),
            ('DAE', "DAE_Presets", "Dae Collada Export presets"),
        ],
        default= 'FBX',
    )

    # Make enum for selection and filling it with values using a function
    # Calling a class with presetPointerProperty
    exp_Presets_FBX:            bpy.props.CollectionProperty(type = props.TAMT_fbxExportProperties)
    default_FBX_preset:            bpy.props.EnumProperty(name = "FBX Preset", items =  utils.update_prefs_presets )
    
    exp_Presets_OBJ:            bpy.props.CollectionProperty(type = props.TAMT_objExportProperties)
    default_OBJ_preset:            bpy.props.EnumProperty(name = "OBJ Preset", items =  utils.update_prefs_presets )
    
    exp_Presets_USD:            bpy.props.CollectionProperty(type = props.TAMT_usdExportProperties)
    default_USD_preset:            bpy.props.EnumProperty(name = "USD Preset", items =  utils.update_prefs_presets )
    
    exp_Presets_DAE:            bpy.props.CollectionProperty(type = props.TAMT_daeExportProperties)
    default_DAE_preset:            bpy.props.EnumProperty(name = "DAE Preset", items =  utils.update_prefs_presets )
    


    def draw(self, context):
        layout = self.layout

        r1 = layout.row()
        r1.label(text="Substance Painter Executable")
        r1.prop(self, 'painter_path', text="")

        r2 = layout.row()
        r2.label(text="Export Format Preset")
        
        r2.prop(self, 'exp_Preset_Type', text="")

        layout_row = layout.row(align=True)

        preset_map = {
            'FBX': (self.exp_Presets_FBX, 'default_FBX_preset'),
            'OBJ': (self.exp_Presets_OBJ, 'default_OBJ_preset'),
            'USD': (self.exp_Presets_USD, 'default_USD_preset'),
            'DAE': (self.exp_Presets_DAE, 'default_DAE_preset'),
        }

        presets, index_prop_name = preset_map.get(self.exp_Preset_Type, (None, None))

        # row.prop(self, index_prop_name)
        # if len(presets) > 0:
        #     index = int(getattr(self, index_prop_name))
        #     row.prop(presets[index], "preset_name", text = "")

        layout_row.label(text = "Preset", icon= 'PRESET')

        right_side = layout_row.row(align= True)
        right_side.alignment = 'RIGHT'

        right_side.prop(self, index_prop_name, text = "", icon='PRESET',icon_only=True)
        if len(presets) > 0:
            index = int(getattr(self, index_prop_name))
            right_side.prop(presets[index], "preset_name", text = "")


        right_side.operator("to_automate.atm_prefs_create_preset", text= "", icon= 'ADD')
        right_side.operator("to_automate.atm_prefs_remove_preset", text= "", icon= 'REMOVE')


        panel_map = {
            'FBX': utils_panel.fbx_properties,
            'OBJ': utils_panel.obj_properties,
            'USD': utils_panel.usd_properties,
            'DAE': utils_panel.dae_properties,
        }

        if len(presets) > 0:
            setting_row = layout.box()

            current_preset_panel = panel_map.get(self.exp_Preset_Type, None)
            index = int(getattr(self, index_prop_name))
            current_preset_panel(setting_row, presets[index])



classes = (
    ToAutomatePreferences,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

    # prefs = bpy.context.preferences.addons["ToAutomate"].preferences
    # if not prefs.first_run_complete:
    #     print("Initial Setup for ToAutomate...")
    #     utils.preFill_Export_list(prefs)
    #     prefs.first_run_complete = True


def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)