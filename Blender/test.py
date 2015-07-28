import bge
import mathutils
import move


class tester:
	
	def __init__(self):
		scene = bge.logic.getCurrentScene()
		objList = scene.objects
		obj_name = 'Cube'
		self.Cube = objList[obj_name]
		self.lines = []
		self.counter = 0
		
	def setText(self, stri):
		print(stri)
		
		self.lines = stri.split('\n')
		
		
	
	def run(self):
		if self.counter < len(self.lines):
	
			tmp = self.Cube.getLinearVelocity()
			print(str(tmp.x) + " | " + str(tmp.y))
			
			if tmp.x == 0 and tmp.y == 0:
				dir = self.lines[self.counter].split(',')[0]
				mov = int(self.lines[self.counter].split(',')[1])
				self.counter += 1
				if dir[0] is "n":
					move.moveUnit(self.Cube, "n", mov)
				if dir[0] is "s":
					move.moveUnit(self.Cube, "s", mov)
				if dir[0] is "e":
					move.moveUnit(self.Cube, "e", mov)
				if dir[0] is "w":
					move.moveUnit(self.Cube, "w", mov)
		else:
			self.counter = 0
		
def main(self):
	print("wot")
	
	#if dir is "n":
	#	print(owner.rayCastTo([owner.localPosition.x, owner.localPosition.y + movement, owner.localPosition.z], 0))
	#if dir is "s":
	#	print(owner.rayCastTo([owner.localPosition.x, owner.localPosition.y - movement, owner.localPosition.z], 0))
	#if dir is "e":
	#	print(owner.rayCastTo([owner.localPosition.x + movement, owner.localPosition.y, owner.localPosition.z], 0))
	#if dir is "w":
	#	print(owner.rayCastTo([owner.localPosition.x - movement, owner.localPosition.y, owner.localPosition.z], 0))
	
	#move.moveUnit(owner, "e", 3)
	#move.moveUnit(owner, "n", 10)
	#move.moveUnit(owner, "e", 2)
	

	
	#setChange("w", 1)
	#startpoint
	#owner.worldPosition = [-9.5,-9.5,0.5]
	
	
	#move(owner, "n", 1)
	
	#win = bpy.data.objects['Icosphere']
	#move(win, "west", 1)
	
