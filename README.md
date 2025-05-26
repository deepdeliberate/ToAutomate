# ToAutomate

## Overview
ToAuotmate has a simple goal, to streamline and automate the repeating process of 3D production work.

1. **ToAutomate** is a Blender addon aimed to optimize the **3D-Art** workflows in real production workflow.
2. It is an ever-evolving addon which tackles various stages of production that could be optimized to simplify repetetive tasks and give artist freedom to focus more on creative work.
3. Tools like: <br>
    a. **Renaming objects for LP/HP Baking stages.<br>
    b. Pre-bake mesh Check, Collection Organizer.<br>
    c. Add Modifier for group objects.<br>
    d. UV/UVMap tools.<br>
    e. Export Collection with Different Presets**
5. Developed by me, I work as a freelance Vehicle Artist, trying to adapt to my different clients, I always strive to improve my workflows to set a modular workflow that fits everyone and hope to impprove the 3D workflow with each encounter.

## Getting Started
### Download and Installation
Install from our github or gumroad, gumroad is helpful just in case you wanna be notified of new releases. 

* [Github](https://github.com/deepdesperate/ToAutomate)
* [Gumroad](https://namandeep.gumroad.com/)

<!-- Add Information about installing in Blender 4.2+ -->

After downloading, the addon can be installed with following steps: <br>
1. Open **Blender** and go to **Edit > Preferences > addons.** 
2. Click at Install from FIle and locate the pacakge [ToAutomate.zip](https://github.com/deepdesperate/ToAutomate) file in the newly opened window. <br>
3. The addon should now appear in your addons list and can be activated. 
Please contact me in case you run into any issues.

## Feature Overview
1. 3D Object Operators: <br>
    <!-- <img src="/assets/images/3DMenu.png" width=200> -->
    1. `Renamer` Operator to convert to rename two objects as Low and High, with suffix
        1. Active object gets renamed to `obj_LP`, and selected object gest `obj_HP`.
        2. Suffix are changeable for both.
    2. `Organize Menu`: It moves the Low-poly and High-poly objects into their respective collection.
    3. `Selection Menu`: Helps Checking if `Low and High objects have their respective counter-part.
    4. `Collection Organizer`: Organizes the Blender Collection Heirarchy and creates respective empty-parent heirarchy useful when exporting to softwares like max and game engines.
    5. `Collection DeOrganizer`: Deorganizes the Empty-parent Heirarchy and Converts it to Blender Collection System.
2. Mesh Operators:
    1. `Modifiers` List: Applies given modifiers to the all selected-objects. Helpful to apply modifiers to group/multiple objects.
    2. `Settings` Some Modifier has additional pop-up setting upon applying, for adjustments.
    3. `Materials` Simply Add, Delete, or Remove Unused Materials to selected objects
        1. Works in `Edit-Mode` too, selected faces get applied the materials selected.
3. UV Operators:
    1. `UV Offset`: Checks whether selected objects has Mirror/Array UV-Offset on or not.
        1. Helpful so during baking, we don't weird artifacts cuz of Overlap-UV
        2. `Add UV Offset`: Adds UV offset to selected objects' modifiers: Array and Mirror
        3. `Split Island Check`: Not perfect, But checks if there are any islands that are split.
        4. `Seams Menu`: Mark Boundary of selected faces as seam, or mark sharp edges as seam
    2. `UVMap Menu`: `Create`, `Rename` or `Delete` UV Maps
        1. Check UV Operators Page for all functionality
4. Export System:
    1. `Export Menu`: Start by Pressing: `Add Preset` and change settings for your first export preset.
    

## Why Object Renamer Tools?
The tool is oriented towards production stages where efficiency/speed is appreciated. I can't force any of my workflows or tools to anyone. 
But I am pretty sure, trying out these features for yourself can save a minute or two during each iteration of workflow and when iterating multiple times, it is a considerable amount of time.

- Like finding which Low poly object doesn't have it's High Poly created or named wrongly in collection of `100` of objects or checking for multiple mesh of same `LP/HP` relationship.
- Exporting Specific Collections for **Normal-Baking**, and different final mesh for **Exporting**.<br>
    - Option to exclude any child Collection from it's Parent Collection Export, 
    - just define a quick preset in Export Manager for the workflow and it will export the collection tree without you manually selecting each collection each time.
- **UV-Tools** UV Tools to help check whether every Baking objects has their Mirror/Array modifiers have offset, so they don't bake artifacts by mistake due to inverted mesh overlapping.
- At the end of the day, we want to work on our projects/task, with minimum bugs
    - less friction in export and baking mesh just to find out that some random mesh wasn't named properly or somehow that one didn't have UV offset leading to Artifacts, that cycle can go repeatedly and in a game-dev environment can be frustrating.
- Test the addon and find it for yourself, If you have more ideas, Suggest them and we'll do best to implement them.


