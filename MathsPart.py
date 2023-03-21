#this script is called by ArchBooMaker, and does the boolean-ing, calculations, and application of custom properties.

import bpy 
import math
import bmesh
from mathutils import Vector

def do_the_hard_part (my_track_name, left_or_right, foot_or_track, new_object_name):
    print("Booleaning and calculating variables")
    
#First up, select my_track_name, duplicate it, and rename the duplicate:
    # Select the object by name
    obj = bpy.context.scene.objects.get (my_track_name)
    # Deselect all other objects
    bpy.ops.object.select_all (action='DESELECT')
    # Make the object active and selected
    bpy.context.view_layer.objects.active = obj
    obj.select_set (True)
    # Duplicate the object in place
    bpy.ops.object.duplicate_move ()
    # Get the duplicate object
    dup = bpy.context.active_object
    # Rename the duplicate object
    dup.name = new_object_name
    
#set duplicate colour to red:
    # Get the existing material by name
    mat = bpy.data.materials.get ("Red")

    # If it does not exist, create a new one
    if mat is None:
        mat = bpy.data.materials.new (name="Red")
        mat.diffuse_color = (1, 0, 0, 1)

    # Assign the material to the duplicate object
    dup.active_material = mat
    
#Next, we want to boolean the prism and the object to create our arch:
    # Get the prism object by name
    prism = bpy.context.scene.objects.get ("prism")
    # Add a boolean modifier to the duplicate object
    bool = dup.modifiers.new (name="Boolean", type="BOOLEAN")
    # Set the modifier operation to difference
    bool.operation = "INTERSECT"
    # Set the modifier object to prism
    bool.object = prism
    #turn on self intersection:
    bool.use_self = True
    # Apply the modifier
    bpy.ops.object.modifier_apply ({"object": dup}, modifier=bool.name) #We could comment this out to make things reversible.
    #make prism and original object invisible in the viewport:
    prism.hide_set(True)
    obj.hide_set(True)

####CALCULATION TIME###

#Let's just grab those locators:
    mpa = bpy.context.scene.objects.get ("mpLocatorA")
    mpb = bpy.context.scene.objects.get ("mpLocatorB")
    mph = bpy.context.scene.objects.get ("heelLocator")
    
#I could keyframe the locators here, but I'm going to leave that out for now.


##some variables used in other calculations:
    mpMid = (mpa.location + mpb.location)/2
    axisMid = (mph.location + mpMid)/2


#Orientation Locator
 #I didn't bother with the orientation locator in the setup script, 
 #Do we create a new one here temporarily?
 
##AXIS LENGTH
    axis_length = (mpMid - mph.location).length

##MID AXIS DEPTH
    track_depth = axisMid.z

##HEEL DEPTH
    heel_depth = mph.location.z    

##MPa DEPTH
    mpa_depth = mpa.location.z

##MPB DEPTH
    mpb_depth = mpb.location.z
    
##RELATIVE MID DEPTH
    rel_depth = track_depth/axis_length

##PITCH
    axis = mpMid - mph.location
    pitch = math.degrees(math.asin(axis.z/axis_length))

##ROLL

#~~~TODO~~~


##BASE AREA
    side1 = Vector(mpa.location-mph.location)
    side2 = Vector(mpb.location - mph.location)
    base_area = 0.5*((side1.cross(side2)).length)

##ARCHVOLUME
    #Need to use bmesh apparently
    # create a new bmesh object and fill it with mesh data
    me = dup.data
    bm = bmesh.new()
    bm.from_mesh(me)
    # apply world transformation matrix to bmesh
    bm.transform(dup.matrix_world)
    # triangulate faces for consistency
    bmesh.ops.triangulate(bm, faces=bm.faces)
    # initialize volume to zero
    volume = 0
    # loop through all faces in bmesh
    for f in bm.faces:
        # get the three vertices of the face
        v1 = f.verts[0].co
        v2 = f.verts[1].co
        v3 = f.verts[2].co
        # calculate the signed volume of the tetrahedron formed by the face and the origin
        volume += v1.dot(v2.cross(v3)) / 6

    # print result    
    print("Volume:", volume)

    # free bmesh memory    
    bm.free()
 
 
##RELATIVE ARCH VOLUME  (newest RAV is volume divided by area^1.5
    rav = 100*(volume/(pow(area, 1.5)))



#Assign variables to custom properties panel.    
    print("RAV:" rav)
    print("RMD:"axisMid.z)
    print("pitch: ", pitch)
    print("Roll: ")
    print("Arch Volume: " volume)
    print("Base Area: " base_area)
    print("Axis Length: ", axis_length)
    print("Mid Axis Depth: ", track_depth)
    print("Heel Depth: ", mph.location.z)
    print("mpA depth: ", mpa.location.z)
    print("mpB depth: ", mpb.location.z)
    print("side: ", left_or_right)