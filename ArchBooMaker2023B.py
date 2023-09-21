import bpy
import sys
import os
    
from . import MathsPart
from . import ArchBooSetup2023B
from . import exportValues

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
        ArchBooSetup2023B.setup_prism()
        return {'FINISHED'}

# Define an operator class that runs the export script
class RunExportOperator (bpy.types.Operator):
    bl_idname = "object.export_values"
    bl_label = "Export to CSV"
    
    def execute (self, context):
        # Put your script for export here
        bpy.ops.export_data.some_data('INVOKE_DEFAULT')
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
        
        #some buttons to ease selecting of locators
        row2 = layout.row ()
        row2.operator('object.select_mpa', text="mpa").name = "mpLocatorA"
        row2.operator('object.select_mpa', text="mpb").name = "mpLocatorB"
        row2.operator('object.select_mpa', text="mph").name = "heelLocator"
        
        # create an object selector
        layout.prop_search(scene, "my_track", scene, "objects", text="Model")
        
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
        
        #add the export button
        layout.operator ("object.export_values", text = "export values")        
        #layout.operator ("object.close_panel")

#three buttons to select locators (I feel this might be useful?)
class OBJECT_OT_selectMpa(bpy.types.Operator): 
    bl_label = "Select locator" 
    bl_idname = "object.select_mpa"

    name: bpy.props.StringProperty(name="Name", default="") # This is the argument for the operator

    def execute (self, context):
        # Get the object by name
        myobject = bpy.data.objects.get(self.name)
        if myobject:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            # Select the object
            myobject.select_set(True)
            # Make it active
            context.view_layer.objects.active = myobject
            self.report({'INFO'}, f"Selected {myobject.name}")
        else:
            self.report({'WARNING'}, f"No object named {self.name}")
        return {'FINISHED'}



# create an operator to cancel the operation and reset the fields
class OBJECT_OT_ResetOperation (bpy.types.Operator):
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
    bpy.utils.register_class (OBJECT_OT_CalculateBoolean)
    bpy.utils.register_class (OBJECT_OT_ResetOperation)
    #bpy.utils.register_class (OBJECT_OT_ClosePanel)
    bpy.utils.register_class (RunScriptOperator)
    bpy.utils.register_class (RunExportOperator)
    bpy.utils.register_class (OBJECT_OT_selectMpa)
    
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
    bpy.utils.unregister_class (OBJECT_OT_CalculateBoolean)
    bpy.utils.unregister_class (OBJECT_OT_ResetOperation)
    #bpy.utils.unregister_class (OBJECT_OT_ClosePanel)
    bpy.utils.unregister_class (RunScriptOperator)
    bpy.utils.unregister_class (RunExportOperator)
    bpy.utils.unregister_class (OBJECT_OT_selectMpa)

    
    
    
    del bpy.types.Scene.selected_object
    del bpy.types.Scene.foot_or_track
    del bpy.types.Scene.left_or_right
    del bpy.types.Scene.new_object_name

if __name__ == "__main__":
   register ()