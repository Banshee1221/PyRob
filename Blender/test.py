import bge
import mathutils
import move
import time

class tester:
	
	def __init__(self):
		scene = bge.logic.getCurrentScene()
		objList = scene.objects
		obj_name = 'Cube'
		self.Cube = objList[obj_name]
		self.lines = []
		self.counter = 0
		self.timer = time.time()+1
		
	def setText(self, stri):
		print(stri)
		
		self.lines = stri.split('\n')
		
		
	
	def run(self):
		error = -1
		if self.counter < len(self.lines):
	
			#print(str(tmp.x) + " | " + str(tmp.y))
			
			if self.timer < time.time():
				self.timer = time.time()+1
				dir = self.lines[self.counter].split(',')[0]
				mov = int(self.lines[self.counter].split(',')[1])
				self.counter += 1
				if dir[0] is "n":
					if (self.Cube.rayCastTo([self.Cube.localPosition.x, self.Cube.localPosition.y + mov, self.Cube.localPosition.z], 0)) is None:
						move.moveUnit(self.Cube, "n", mov)
					else:
						error = self.counter
						self.counter = len(self.lines)
				if dir[0] is "s":
					if (self.Cube.rayCastTo([self.Cube.localPosition.x, self.Cube.localPosition.y - mov, self.Cube.localPosition.z], 0)) is None:
						move.moveUnit(self.Cube, "s", mov)
					else:
						error = self.counter
						self.counter = len(self.lines)
				if dir[0] is "e":
					if (self.Cube.rayCastTo([self.Cube.localPosition.x + mov, self.Cube.localPosition.y, self.Cube.localPosition.z], 0)) is None:
						move.moveUnit(self.Cube, "e", mov)
					else:
						error = self.counter
						self.counter = len(self.lines)
				if dir[0] is "w":
					if (self.Cube.rayCastTo([self.Cube.localPosition.x - mov, self.Cube.localPosition.y, self.Cube.localPosition.z], 0)) is None:
						move.moveUnit(self.Cube, "w", mov)
					else:
						error = self.counter
						self.counter = len(self.lines)
		else:
			self.counter = 0
			self.lines = []
			
		return error
		
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
	
