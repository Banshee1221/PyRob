import bge
import mathutils
import move
       
def main(self):
    #print("wot")
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    
    dir = "n"
    movement = 10
    
    if dir is "n":
        print(owner.rayCastTo([owner.localPosition.x, owner.localPosition.y + movement, owner.localPosition.z], 0))
    if dir is "s":
        print(owner.rayCastTo([owner.localPosition.x, owner.localPosition.y - movement, owner.localPosition.z], 0))
    if dir is "e":
        print(owner.rayCastTo([owner.localPosition.x + movement, owner.localPosition.y, owner.localPosition.z], 0))
    if dir is "w":
        print(owner.rayCastTo([owner.localPosition.x - movement, owner.localPosition.y, owner.localPosition.z], 0))
    
    #move.moveUnit(owner, "e", 3)
    #move.moveUnit(owner, "n", 10)
    #move.moveUnit(owner, "e", 2)
    

    
    #setChange("w", 1)
    #startpoint
    #owner.worldPosition = [-9.5,-9.5,0.5]
    
    
    #move(owner, "n", 1)
    
    #win = bpy.data.objects['Icosphere']
    #move(win, "west", 1)
    
def setText(string):

	cont = bge.logic.getCurrentController()
    owner = cont.owner
	print(string)
	
	dir = string
	
	if dir is "n":
		move.moveUnit(owner, "n", 10)