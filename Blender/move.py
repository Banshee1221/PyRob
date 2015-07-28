import bge
import bpy
import mathutils

x = 0
y = 0

def moveUnit(obj, dir, steps):
    global x
    global y
    
    
    if dir is "n":
        x = steps
    elif dir is "s":
        x = -steps
    elif dir is "e":
        y = steps
    elif dir is "w":
        y = -steps
        
    obj.setLinearVelocity([y, x, 0], True)
    
