# Seetup script for RAVBlender.  Written by Peter FAlkingham, based on Steve Gatesy's Maya version, and with coding help from ChatGPT!

import bpy
import bmesh
import math
from mathutils import Vector
context = bpy.context

###Check if bits exist, and if so, make selectable, then delete
  # make the prism not directly selectable.  commented for debugging ***
if "prism" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["prism"].hide_select = False
    bpy.data.objects["prism"].select_set(True)
    bpy.ops.object.delete()
if "aUp" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["aUp"].hide_select = False 
    bpy.data.objects["aUp"].select_set(True)
    bpy.ops.object.delete()
if "bUp" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["bUp"].hide_select = False
    bpy.data.objects["bUp"].select_set(True)
    bpy.ops.object.delete()
if "heelUp" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["heelUp"].hide_select = False
    bpy.data.objects["heelUp"].select_set(True)
    bpy.ops.object.delete()
if "mpLocatorA" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["mpLocatorA"].select_set(True)
    bpy.ops.object.delete()
if "mpLocatorB" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["mpLocatorB"].select_set(True)
    bpy.ops.object.delete()
if "heelLocator" in bpy.data.objects:
    # Object exists, select it and delete it
    bpy.data.objects["heelLocator"].select_set(True)
    bpy.ops.object.delete()



###Now do script
#create and rename locators
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, -2, 0), scale=(1, 1, 1))
bpy.context.active_object.name='heelLocator'
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(-1, 1, 0), scale=(1, 1, 1))
bpy.context.active_object.name='mpLocatorA'
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(1, 1, 0), scale=(1, 1, 1))
bpy.context.active_object.name='mpLocatorB'

#create objects to refer to these later - ####delete if not used
heelLoc = bpy.data.objects["heelLocator"]
aLoc = bpy.data.objects["mpLocatorA"]
bLoc = bpy.data.objects["mpLocatorB"]


#create and rename prism
bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=2, depth=2, align='WORLD', location=(0, 0, 1), scale=(1, 1, 1))
bpy.context.active_object.name='prism'
obj = bpy.context.scene.objects["prism"]

#now make sure lower and upper vertices of prism are in initial position.
#heel
obj.data.vertices[0].co.y =-2   #lower heel
obj.data.vertices[1].co.y =-2   #upper heel
#mpa
obj.data.vertices[2].co.y =1    #MpA low
obj.data.vertices[3].co.y =1    #MpA High
obj.data.vertices[2].co.x =-1
obj.data.vertices[3].co.x =-1
#mpb
obj.data.vertices[4].co.y =1    #MPB low
obj.data.vertices[5].co.y =1    #MpB high.
obj.data.vertices[4].co.x =1
obj.data.vertices[5].co.x =1


####Up to here, we've created a prism, and placed the verticies in the correct place.
#now to drive lower vertices by locators:
#Set up vertex groups to attach hooks to
vghl = obj.vertex_groups.new(name="vertexGrp_HeelLow")
vghl.add([0], 1.0, "REPLACE")
vgal = obj.vertex_groups.new(name="vertexGrp_ALow")
vgal.add([2], 1.0, "REPLACE")
vgbl = obj.vertex_groups.new(name="vertexGrp_BLow")
vgbl.add([4], 1.0, "REPLACE")

vghh = obj.vertex_groups.new(name="vertexGrp_HeelHigh")
vghh.add([1], 1.0, "REPLACE")
vgah = obj.vertex_groups.new(name="vertexGrp_AHigh")
vgah.add([3], 1.0, "REPLACE")
vgbh = obj.vertex_groups.new(name="vertexGrp_BHigh")
vgbh.add([5], 1.0, "REPLACE")

#Now constrain lower vertices to locators
#constrain vertex 0 to heelLocator
mod = obj.modifiers.new("heelHook", "HOOK")
mod.object = bpy.data.objects["heelLocator"]
mod.vertex_group = "vertexGrp_HeelLow"
mod.strength = 1.
#constrain vertex 1 to mpA
mod = obj.modifiers.new("mpAHook", "HOOK")
mod.object = bpy.data.objects["mpLocatorA"]
mod.vertex_group = "vertexGrp_ALow"
mod.strength = 1.
#constrain vertex 2 to mpB
mod = obj.modifiers.new("mpBHook", "HOOK")
mod.object = bpy.data.objects["mpLocatorB"]
mod.vertex_group = "vertexGrp_BLow"
mod.strength = 1.


#####So far, create prism and locators, then hook lower vertices to locators. 
###Now create upper locators
#create locators for upper:
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, -2, 2), radius = 0.2)
bpy.context.active_object.name='heelUp'
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(-1, 1, 2), radius = 0.2)
bpy.context.active_object.name='aUp'
bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(1, 1, 2), radius = 0.2)
bpy.context.active_object.name='bUp'

#create objects to refer to these later - ####delete if not used
hUpLoc = bpy.data.objects["heelUp"]
aUPLoc = bpy.data.objects["aUp"]
bUPLoc = bpy.data.objects["bUp"]

#attach with hooks.
#Now constrain lower vertices to locators
#constrain vertex 0 to heelLocator
mod = obj.modifiers.new("heelUpHook", "HOOK")
mod.object = bpy.data.objects["heelUp"]
mod.vertex_group = "vertexGrp_HeelHigh"
mod.strength = 1.
#constrain vertex 1 to mpA
mod = obj.modifiers.new("mpuAHook", "HOOK")
mod.object = bpy.data.objects["aUp"]
mod.vertex_group = "vertexGrp_AHigh"
mod.strength = 1.
#constrain vertex 2 to mpB
mod = obj.modifiers.new("mpuBHook", "HOOK")
mod.object = bpy.data.objects["bUp"]
mod.vertex_group = "vertexGrp_BHigh"
mod.strength = 1.

##
#drivers!
##


#For Heel
driver = bpy.data.objects["heelUp"].driver_add("location")

####THE FOLLOWING LOOP WAS OPTIMIZED FROM MY ORIGINAL CODE BY CHATGPT:

# Create a list of tuples containing the driver index, data path for the
# bottomHeel variable, and data path for the normVec variable
drivers = [(0, 'location[0]', 'data.polygons[4].normal[0]'),(1, 'location[1]', 'data.polygons[4].normal[1]'),(2, 'location[2]', 'data.polygons[4].normal[2]')]

# Iterate over the list of drivers
for index, bottom_heel_path, norm_vec_path in drivers:
    # Create the bottomHeel variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[0].name = 'bottomHeel'
    driver[index].driver.variables[0].type = 'SINGLE_PROP'
    driver[index].driver.variables[0].targets[0].id = bpy.data.objects["heelLocator"]
    driver[index].driver.variables[0].targets[0].data_path = bottom_heel_path
    # Create the normVec variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[1].name = 'normVec'
    driver[index].driver.variables[1].type = 'SINGLE_PROP'
    driver[index].driver.variables[1].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[1].targets[0].data_path = norm_vec_path
    # Create the offset variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[2].name = 'offset'
    driver[index].driver.variables[2].type = 'SINGLE_PROP'
    driver[index].driver.variables[2].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[2].targets[0].data_path = 'scale.z'
    # Set the expression for the driver
    driver[index].driver.expression = "bottomHeel+(normVec*-1*(offset+1))"


#for MPA
driver = bpy.data.objects["aUp"].driver_add("location")

####THE FOLLOWING LOOP WAS OPTIMIZED FROM MY ORIGINAL CODE BY CHATGPT:

# Create a list of tuples containing the driver index, data path for the
# bottomHeel variable, and data path for the normVec variable
drivers = [(0, 'location[0]', 'data.polygons[4].normal[0]'),(1, 'location[1]', 'data.polygons[4].normal[1]'),(2, 'location[2]', 'data.polygons[4].normal[2]')]

# Iterate over the list of drivers
for index, bottom_heel_path, norm_vec_path in drivers:
    # Create the bottomHeel variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[0].name = 'bottomA'
    driver[index].driver.variables[0].type = 'SINGLE_PROP'
    driver[index].driver.variables[0].targets[0].id = bpy.data.objects["mpLocatorA"]
    driver[index].driver.variables[0].targets[0].data_path = bottom_heel_path
    # Create the normVec variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[1].name = 'normVec'
    driver[index].driver.variables[1].type = 'SINGLE_PROP'
    driver[index].driver.variables[1].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[1].targets[0].data_path = norm_vec_path
    # Create the offset variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[2].name = 'offset'
    driver[index].driver.variables[2].type = 'SINGLE_PROP'
    driver[index].driver.variables[2].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[2].targets[0].data_path = 'scale.z'
    # Set the expression for the driver
    driver[index].driver.expression = "bottomA+(normVec*-1*(offset+1))"
    
    
#For MPB
#for MPA
driver = bpy.data.objects["bUp"].driver_add("location")

####THE FOLLOWING LOOP WAS OPTIMIZED FROM MY ORIGINAL CODE BY CHATGPT:

# Create a list of tuples containing the driver index, data path for the
# bottomHeel variable, and data path for the normVec variable
drivers = [(0, 'location[0]', 'data.polygons[4].normal[0]'),(1, 'location[1]', 'data.polygons[4].normal[1]'),(2, 'location[2]', 'data.polygons[4].normal[2]')]

# Iterate over the list of drivers
for index, bottom_heel_path, norm_vec_path in drivers:
    # Create the bottomHeel variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[0].name = 'bottomB'
    driver[index].driver.variables[0].type = 'SINGLE_PROP'
    driver[index].driver.variables[0].targets[0].id = bpy.data.objects["mpLocatorB"]
    driver[index].driver.variables[0].targets[0].data_path = bottom_heel_path
    # Create the normVec variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[1].name = 'normVec'
    driver[index].driver.variables[1].type = 'SINGLE_PROP'
    driver[index].driver.variables[1].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[1].targets[0].data_path = norm_vec_path
    # Create the offset variable
    driver[index].driver.variables.new()
    driver[index].driver.variables[2].name = 'offset'
    driver[index].driver.variables[2].type = 'SINGLE_PROP'
    driver[index].driver.variables[2].targets[0].id = bpy.data.objects["prism"]
    driver[index].driver.variables[2].targets[0].data_path = 'scale.z'
    # Set the expression for the driver
    driver[index].driver.expression = "bottomB+(normVec*-1*(offset+1))"
    

#add a custom property to the prism that drives xyz scale
# Add a custom property called "PrismHeight"
bpy.data.objects['prism']['prismHeight'] = 2.00


# Set the value of the "PrismHeight" property
#obj.get("PrismHeight") = 2


#drive prism scale with this
driver = bpy.data.objects["prism"].driver_add("scale")
for x in range(0,3):
    print(x)
    driver[x].driver.variables.new()
    driver[x].driver.variables[0].name = 'scaleDriver'
    driver[x].driver.variables[0].type = 'SINGLE_PROP'
    driver[x].driver.variables[0].targets[0].id = bpy.data.objects["prism"]
    driver[x].driver.variables[0].targets[0].data_path = "[\"prismHeight\"]"
    driver[x].driver.expression = "scaleDriver/2"

#make the prism not selectable
bpy.data.objects["prism"].hide_select = True  # make the prism not directly selectable.  commented for debugging ***
bpy.data.objects["aUp"].hide_select = True 
bpy.data.objects["bUp"].hide_select = True 
bpy.data.objects["heelUp"].hide_select = True 
### make the upper locators not selectable, and hidden


###move upper locators to a new collection to clean up outliner.


###check if material exists, and if not, create and apply to prism.