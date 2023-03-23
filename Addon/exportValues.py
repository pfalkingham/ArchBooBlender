import bpy

def write_some_data(context, filepath):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    # create a list of custom properties
    props = ["RAV", "RMD", "Pitch", "Roll", "Arch Volume", "Base Area", "Axis Length", "Mid Axis Depth", "Heel Depth", "mpA Depth", "mpB Depth"]
    # write the header row
    f.write("Mesh, ")
    f.write(",".join(props) + "\n")
    # loop through the arch_* objects
    for obj in bpy.data.objects:
        if obj.name.startswith("arch_"):
            #write the object's name:
            f.write(obj.name+", ")
            # create a list of values for each object
            values = [str(obj.get(prop)) for prop in props]
            # write the data row
            f.write(",".join(values) + "\n")
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_data.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_some_data(context, self.filepath)
    

# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportSomeData)



def unregister():
    bpy.utils.unregister_class(ExportSomeData)
  

if __name__ == "__main__":
    register()
    
        # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
