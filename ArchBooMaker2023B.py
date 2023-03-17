#Blender version of ArchBooMaker2023.  
#Based on Steve Gatesy's Mel script for Maya
#This version for blender is written by Peter Falkingham, March 2023, with help from Bing/ChatGPT
#first need to run ArchBooSetupBlender.py - this creates a prism driven by three locators
#align locators with metatarsal heads and heel.  
#Run this script, select if it's a foot or track you're generating an arch for
#Select if it's a left or right
#Select the object to boolean (the track or the foot)
#Prism height is controlled by a custom property on the prism itself.


import bpy

class ArchBooMakerOperator(bpy.types.Operator):
    """Create an arch from a prism and a boolean object"""
    bl_idname = "object.arch_boo_maker"
    bl_label = "Arch Boo Maker"
    bl_options = {'REGISTER', 'UNDO'}

    model: bpy.props.StringProperty(name="Model",default="")
    mode: bpy.props.EnumProperty(name="Mode",items=[("TRACK", "Track", "Use track mode"),("FOOT", "Foot", "Use foot mode")])
    side: bpy.props.EnumProperty(name="Side",items=[("LEFT", "Left", "Use left side"),("RIGHT", "Right", "Use right side")])

    boolean_name: bpy.props.StringProperty(
        name="Boolean Name",
        default="arch_"
    )

    def execute(self, context):
        # Get the prism object
        prism = bpy.data.objects.get(self.model)
        
        # Check if it exists
        if not prism:
            self.report({'ERROR'}, f"No object named {self.model} found")
            return {'CANCELLED'}
        
        # Scale the prism along the z-axis
        prism.scale.z = self.prism_height
        
         # Get the boolean object
        boo = bpy.data.objects.get(self.boolean_name)

         # Check if it exists
        if not boo:
             self.report({'ERROR'}, f"No object named {self.boolean_name} found")
             return {'CANCELLED'}

         # Set the boolean modifier on the prism
        mod = prism.modifiers.new("Arch Boo", 'BOOLEAN')
        mod.object = boo
        mod.operation = 'DIFFERENCE'

         # Apply the modifier
        bpy.ops.object.modifier_apply(modifier=mod.name)

         # Delete the boolean object
        bpy.data.objects.remove(boo)

         # Return success message
        self.report({'INFO'}, f"Arch created from {self.model} and {self.boolean_name}")
         
        return {'FINISHED'}

    def invoke(self, context, event):
        # Use invoke_props_dialog to create a dialog window
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        # Draw the dialog layout
        layout = self.layout
        layout.prop(self, "model")
        row = layout.row()
        row.prop(self, "mode")
        row = layout.row()
        row.prop(self, "side")
        layout.prop(self, "boolean_name")


def register():
    bpy.utils.register_class(ArchBooMakerOperator)


def unregister():
    bpy.utils.unregister_class(ArchBooMakerOperator)


if __name__ == "__main__":
    register()

    # Call the operator
    bpy.ops.object.arch_boo_maker('INVOKE_DEFAULT')