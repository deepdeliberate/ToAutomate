import bpy

from bpy.props import PointerProperty

class TAMT_Addon_Props(bpy.types.PropertyGroup):
    """ Class to define all the properties of the addon"""

    #   --------------  Renamer Menu  ------------------
    
    low_suffix: bpy.props.StringProperty(
        name= "Low Suffix",
        description="Low Poly Object Suffix",
        default = "_LP",
    )
    high_suffix: bpy.props.StringProperty(
        name = "High Suffix",
        description="High Poly Suffix",
        default = "_HP",
    )

    move_HP: bpy.props.BoolProperty(
        name = "Move HPs to HP Collection",
        description = "Move the HP object into high poly collection",
        default = True,
    )
    move_LP: bpy.props.BoolProperty(
        name = "Move LPs to LP Collection",
        description = "Move the LP object into low poly collection",
        default = True,
    )

    col_HP: bpy.props.StringProperty(
        name = "High Poly Collection",
        default = "HP_Named"
    )
    col_LP: bpy.props.StringProperty(
        name = "Low Poly Collection",
        default = "LP_Named"
    )

    # Select significant other
    opt_col_sel: bpy.props.BoolProperty(
        name = "Select the Original Object",
        default = False
    )

    col_sel_enum: bpy.props.EnumProperty(
        name="",
        description= "Menu to Select Objects",
        items= [('OP1', "Non-matching objects", "Select Objects having no matching low or high objects from the collections"),
                ('OP2', "Significant Other","Select the counter high / low object for the selected objects")]
    )




classes = (
    TAMT_Addon_Props,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.tamt = PointerProperty(type = TAMT_Addon_Props)

def unregister_classes():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.tamt