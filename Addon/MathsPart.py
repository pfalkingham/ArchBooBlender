#this script is called by ArchBooMaker, and does the boolean-ing, calculations, and application of custom properties.

import bpy 
import math
import bmesh
from mathutils import Vector

def do_the_hard_part (my_track_name, left_or_right, foot_or_track, new_object_name):
    print("Booleaning and calculating variables")
    
#First up, select my_track_name, duplicate it, and rename the duplicate:

#oldCODE
#    # Select the object by name
#    obj = bpy.context.scene.objects.get (my_track_name)
#    # Deselect all other objects
#    bpy.ops.object.select_all (action='DESELECT')
#    # Make the object active and selected
#    bpy.context.view_layer.objects.active = obj
#    obj.select_set (True)
#    # Duplicate the object in place
#    bpy.ops.object.duplicate_move ()
#    # Get the duplicate object
#    dup = bpy.context.active_object
#    # Rename the duplicate object
#    dup.name = new_object_name
#    

##Next, we want to boolean the prism and the object to create our arch:  #this may need an if statement for foot or track
#    # Get the prism object by name
#    prism = bpy.context.scene.objects.get ("prism")
#    # Add a boolean modifier to the duplicate object
#    bool = dup.modifiers.new (name="Boolean", type="BOOLEAN")
#    # Set the modifier operation to difference
#    bool.operation = "INTERSECT"
#    # Set the modifier object to prism
#    bool.object = prism
#    #turn on self intersection:
#    bool.use_self = True
#    # Apply the modifier
#    bpy.ops.object.modifier_apply ({"object": dup}, modifier=bool.name) #We could comment this out to make things reversible.
#    #make prism and original object invisible in the viewport:
#    prism.hide_set(True)
#    obj.hide_set(True)


    #Set object and prism:
    obj = bpy.context.scene.objects.get (my_track_name)
    pris = bpy.context.scene.objects.get("prism")    
        
        
    #make prism selectable (temporarily):
    bpy.ops.object.select_all(action='DESELECT')
    pris.hide_select = False
    pris.hide_set(False)
    pris.select_set(True)
    bpy.context.view_layer.objects.active = pris

    #duplicate the prism
    bpy.ops.object.duplicate_move()
    dup = bpy.context.active_object
    #rename the duplicate prism to new_object_name
    dup.name = new_object_name

    #reset hidden/selectable status on original prism:
    pris.hide_select = True

    #apply all modifiers on duplicate prism:
    if dup and dup.type == 'MESH':
        bpy.context.view_layer.objects.active = dup
        bpy.ops.object.convert(target='MESH')
        
    #If it's a track, invert the normals (invert them back later):
    if foot_or_track == 'TRACK':
        if obj and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.data.flip_normals()

    #apply the boolean difference to the duplicate prism:
    bool = dup.modifiers.new (name="Boolean", type="BOOLEAN")
    # Set the modifier operation to difference
    bool.operation = "DIFFERENCE"
    # Set the modifier object to the track or foot
    bool.object = obj
    #Maybe allow self-intersection?
    #bool.use_self = True
    # Apply the modifier
    bpy.ops.object.modifier_apply ({"object": dup}, modifier=bool.name) #We could comment this out to make things reversible.

    #Reverse the normals back on the track:
    if foot_or_track == 'TRACK':
        if obj and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.data.flip_normals()

    #make prism and original object invisible in the viewport:
    pris.hide_set(True)
    obj.hide_set(True)



#set duplicate colour to red:
    # Get the existing material by name
    mat = bpy.data.materials.get ("Red")

    # If it does not exist, create a new one
    if mat is None:
        mat = bpy.data.materials.new (name="Red")
        mat.diffuse_color = (1, 0, 0, 1)

    # Assign the material to the duplicate object
    dup.active_material = mat
    


####CALCULATION TIME###

#Let's just grab those locators:
    mpa = bpy.context.scene.objects.get ("mpLocatorA")
    mpb = bpy.context.scene.objects.get ("mpLocatorB")
    mph = bpy.context.scene.objects.get ("heelLocator")
    mpaUp = bpy.context.scene.objects.get ("aUp")
    mpbUp = bpy.context.scene.objects.get ("bUp")
#I could keyframe the locators here, but I'm going to leave that out for now.


##some variables used in other calculations:
    mpMid = (mpa.location + mpb.location)/2
    axisMid = (mph.location + mpMid)/2
    mpUp = (mpaUp.location + mpbUp.location)/2 #mid point between the two upper locators
 
##AXIS LENGTH
    axis_length = (mpMid - mph.location).length

##MID AXIS DEPTH
    track_depth = axisMid.z*-1

##HEEL DEPTH
    heel_depth = mph.location.z*-1    

##MPa DEPTH
    mpa_depth = mpa.location.z*-1

##MPB DEPTH
    mpb_depth = mpb.location.z*-1
    
##RELATIVE MID DEPTH
    rel_depth = track_depth/axis_length

##PITCH
    axis = mpMid - mph.location
    pitch = math.degrees(math.asin(axis.z/axis_length))

##ROLL # will need an if statement for left or right.
    ori = bpy.context.scene.objects.get("orientationLocator") # get the original object by name
    bpy.ops.object.select_all(action='DESELECT') # deselect all objects
    ori.select_set(True) # select the original object
    bpy.ops.object.duplicate_move() # duplicate it and move it slightly
    copy = bpy.data.objects["orientationLocator.001"] # get the copy object by name
    if copy: # check if the copy object exists
        bpy.ops.object.visual_transform_apply() # apply its visual transformation
        rot = copy.rotation_euler # get its euler rotation
        roll = math.degrees(rot.x) # get the local X rotation in degrees
        bpy.ops.object.delete() # delete the copy object
    else: # if the copy object does not exist
        print("No copy object found") # print an error message

    if left_or_right == 'LEFT':
        roll = roll*-1

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
    rav = 100*(volume/(pow(base_area, 1.5)))


    #Print out the values to the console - this is useful for debugging or copy-pasting for individual objects.
    print("RAV: ", rav)
    print("RMD: ", axisMid.z)
    print("pitch: ", pitch)
    print("Roll: ", roll)
    print("Arch Volume: ", volume)
    print("Base Area: ", base_area)
    print("Axis Length: ", axis_length)
    print("Mid Axis Depth: ", track_depth)
    print("Heel Depth: ", mph.location.z)
    print("mpA depth: ", mpa.location.z)
    print("mpB depth: ", mpb.location.z)
    print("side: ", left_or_right)

    #Assign variables to the object  
    dup["RAV"] = rav
    dup["RMD"] = track_depth
    dup["Pitch"] = pitch
    dup["Roll"] = roll
    dup["Arch Volume"] = volume
    dup["Base Area"] = base_area
    dup["Axis Length"] = axis_length
    dup["Mid Axis Depth"] = track_depth
    dup["Heel Depth"] = mph.location.z
    dup["mpA Depth"] = mpa.location.z
    dup["mpB Depth"] = mpb.location.z
    dup["Side"] = left_or_right

    ##MAKE A PANEL ON THE OBJECT TO VIEW THEM
    # Create a custom panel class
    class RAVPanel(bpy.types.Panel):
        bl_idname = "OBJECT_PT_rav_panel"
        bl_label = "RAV data2"
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = "object"

        def draw(self, context):
            # Create a layout for UI elements
            layout = self.layout
            #get the active object
            panelobj = context.object
            
            # Display each variable as a label only if an object is selected
            if panelobj:
                #Show values, to 3 decimal places (for now)
                layout.label(text=f"RAV: {panelobj['RAV']:.3f}")
                layout.label(text=f"Relative Mid Depth: {panelobj['RMD']:.3f}")
                layout.label(text=f"Pitch: {panelobj['Pitch']:.3f}")
                layout.label(text=f"Roll: {panelobj['Roll']:.3f}")
                layout.label(text=f"Arch Volume: {panelobj['Arch Volume']:.3f}")
                layout.label(text=f"Base Area: {panelobj['Base Area']:.3f}")
                layout.label(text=f"Axis Length: {panelobj['Axis Length']:.3f}")
                layout.label(text=f"Mid Axis Depth: {panelobj['Mid Axis Depth']:.3f}")
                layout.label(text=f"Heel Depth: {panelobj['Heel Depth']:.3f}")
                layout.label(text=f"mpA Depth: {panelobj['mpA Depth']:.3f}")
                layout.label(text=f"mpB Depth: {panelobj['mpB Depth']:.3f}")
                layout.label(text=f"Side: {panelobj['Side']:s}")
                
                
    # Register the panel class
    bpy.utils.register_class(RAVPanel)

def register(): pass

def unregister(): pass