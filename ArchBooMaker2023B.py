import bpy
import sys
import os

# get blend file path
filepath = bpy.data.filepath

# get the directory relative to the blend file path
dir = os.path.dirname(filepath)

# append your module's path to sys.path
if not dir in sys.path:
    sys.path.append(dir)
    
import MathsPart
import importlib
importlib.reload(MathsPart)

# Define a function that updates the new object name field
def update_new_object_name(self, context):
    # Check if the pointer property is None
    if self.my_track is None:
        # Reset the new object name field to an empty string
        self.new_object_name = "arch_"
    else:
        # Get the selected object name from the pointer property
        selected_object_name = self.my_track.name
        # Update the new object name field with the prefix and the selected object name
        self.new_object_name = f"arch_{selected_object_name}"

# Define an operator class that runs the setup script
class RunScriptOperator (bpy.types.Operator):
    bl_idname = "object.run_script"
    bl_label = "Run Script"
    
    def execute (self, context):
        # Put your script for Prism MAKER here

        return {'FINISHED'}

# This class closes the panel !!!MAY WANT TO REMOVE THIS WHEN IT'S AN ADDON
class OBJECT_OT_ClosePanel (bpy.types.Operator):
    bl_label = "Close"
    bl_idname = "object.close_panel"
    
    def execute (self, context):
        # unregister the panel class
        bpy.utils.unregister_class (OBJECT_PT_MayaScript)
        
        return {'FINISHED'}

# Define a pointer property for the tray object
bpy.types.Scene.my_track = bpy.props.PointerProperty(name="track", type=bpy.types.Object, update=update_new_object_name)


# create a panel in the viewport window
class OBJECT_PT_MayaScript (bpy.types.Panel):
    bl_label = "ArchBooMaker"
    bl_idname = "OBJECT_PT_maya_script"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ABM"

    def draw (self, context):
        layout = self.layout
        scene = context.scene
        
        #Adding the run setup script button
        layout.operator("object.run_script", text = "Setup Prism")
        
        # create an object selector
        layout.prop_search(scene, "my_track", scene, "objects", text="Model")
        
        # create an insert button
#        layout.operator ("object.insert_object_name")
        
        # create a dialogue for foot or track
        layout.prop (scene, "foot_or_track", expand=True)
        
        # create a dialogue for left or right
        layout.prop (scene, "left_or_right", expand=True)
        
        # create a name field for a new object
        layout.prop (scene, "new_object_name")
        
        # create a calculate button and a cancel button
        row = layout.row ()
        row.operator ("object.calculate_boolean")
        row.operator ("object.cancel_operation")
        layout.operator ("object.close_panel")

# create an operator to insert the selected object name into the new object name field
class OBJECT_OT_InsertObjectName (bpy.types.Operator):
    bl_label = "Update Arch Name"
    bl_idname = "object.insert_object_name"
    
    def execute (self, context):
        scene = context.scene
        
        # get the selected object name
        selected_object_name = scene.my_track.name
        
        # update the new object name field with the prefix and the selected object name
        scene.new_object_name = f"arch_{selected_object_name}"
        
        return {'FINISHED'}


# create an operator to cancel the operation and reset the fields
class OBJECT_OT_CancelOperation (bpy.types.Operator):
    bl_label = "Reset"
    bl_idname = "object.cancel_operation"
    
    def execute (self, context):
       scene = context.scene
      
       # reset the fields to their default values 
       scene.selected_object = ""
       scene.foot_or_track = 'FOOT'
       scene.left_or_right = 'LEFT'
       scene.new_object_name = "arch_"
       scene.my_track = None
       #make sure prism is visible:
       bpy.context.scene.objects['prism'].hide_set(False)
       
       return {'FINISHED'}



# create an operator to calculate the boolean operation on the new object
class OBJECT_OT_CalculateBoolean (bpy.types.Operator):
    bl_label = "Calculate"
    bl_idname = "object.calculate_boolean"
    
    def execute (self, context):
        scene = context.scene
        #Call the maths Script
        
        ###TEST VARIABLES HERE###
        print(scene.my_track.name)
        print(scene.left_or_right)
        print(scene.foot_or_track)
        print(scene.new_object_name)
        # Get the values of the object selector and the radio buttons from the context
        MathsPart.do_the_hard_part(scene.my_track.name, scene.left_or_right, scene.foot_or_track, scene.new_object_name)
        return {'FINISHED'}

# register the classes and properties
def register ():
    bpy.utils.register_class (OBJECT_PT_MayaScript)
#   bpy.utils.register_class (OBJECT_OT_InsertObjectName)
    bpy.utils.register_class (OBJECT_OT_CalculateBoolean)
    bpy.utils.register_class (OBJECT_OT_CancelOperation)
    bpy.utils.register_class (OBJECT_OT_ClosePanel)
    bpy.utils.register_class(RunScriptOperator)
    
    bpy.types.Scene.selected_object = bpy.props.StringProperty ()
    bpy.types.Scene.foot_or_track = bpy.props.EnumProperty (
        items=[
            ('FOOT', 'Foot', ''),
            ('TRACK', 'Track', '')
        ],
        default='FOOT'
    )
    
    bpy.types.Scene.left_or_right = bpy.props.EnumProperty (
        items=[
            ('LEFT', 'Left', ''),
            ('RIGHT', 'Right', '')
        ],
        default='LEFT'
    )
    
    bpy.types.Scene.new_object_name = bpy.props.StringProperty (
        default="arch_"
    )

# unregister the classes and properties
def unregister ():
    bpy.utils.unregister_class (OBJECT_PT_MayaScript)
    bpy.utils.unregister_class (OBJECT_OT_InsertObjectName)
    bpy.utils.unregister_class (OBJECT_OT_CalculateBoolean)
    bpy.utils.unregister_class (OBJECT_OT_CancelOperation)
    bpy.utils.unregister_class (OBJECT_OT_ClosePanel)
    bpy.utils.unregister_class(RunScriptOperator)
    
    
    del bpy.types.Scene.selected_object
    del bpy.types.Scene.foot_or_track
    del bpy.types.Scene.left_or_right
    del bpy.types.Scene.new_object_name

if __name__ == "__main__":
   register ()