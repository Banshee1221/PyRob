import bge
import bpy
import mathutils

x = 0
y = 0

def moveUnit(obj, dir, steps):
    global x
    global y
    
    
    if dir is "n":
        y = steps
    elif dir is "s":
        y = -steps
    elif dir is "e":
        x = steps
    elif dir is "w":
        x = -steps
        
    #obj.setLinearVelocity([y, x, 0], True)
    obj.worldPosition = [obj.position.x + x,obj.position.y + y,obj.position.z]
