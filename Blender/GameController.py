import bge
import mathutils
bge.render.showMouse(True)

cont = bge.logic.getCurrentController() # Get the Python controller running the script

obj = cont.owner #Get the object that has the controller

sce = obj.scene # Get the scene the object is in 
#(this is valid if you have a recent build of Blender)

returned = sce.addObject("Cube", obj) # The addObject() function returns a 
print (returned)
#reference to the object instantiated. It adds the 
#object specified ("Cube") with the position, orientation, and scale of
#the reference object used (obj, or the object running this script, in this case)
#vec_a = mathutils.Vector((20.0, 1.0, 0.0))
#returned.worldPosition = returned.worldPosition.lerp(vec_a, .1)
#returned.applyMovement([2, 0, 0], True)
#returned.applyMovement([0, 5, 0], True)

# Or alternatively:

#returned.worldPosition.x += 2.0 # This is global movement, though. 

#To do local movement, you would have to grab the object's world 

#orientation in a column format - just stick with the applyMovement() 

#function if you need local movement for now.