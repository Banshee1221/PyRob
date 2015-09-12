import bge
import bpy
import mathutils
import time

class move:
	def __init__(self):
		#pass
		self.moving = False
		self.endTime = 0
		self.startTime = 0
		self.endPos = []
		self.startPos = []
		
	def moveUnitOne(self, obj, dir):
		
		x = 0
		y = 0
		 
		if dir is "n":
			y = 1
		elif dir is "s":
			y = -1
		elif dir is "e":
			x = 1
		elif dir is "w":
			x = -1
			
		
		if (self.moving == False):
			self.startTime = time.time()
			self.endTime = self.startTime + 0.25
			self.moving = True
			self.endPos = [obj.position.x + x,obj.position.y + y,obj.position.z]
			self.startPos = [obj.position.x, obj.position.y, obj.position.z]
		
		percent = (time.time() - self.startTime) * 4
		if (percent < 1):
			print(percent)
			obj.worldPosition = lerp(self.startPos, self.endPos, percent)
		else:
			percent = 1
			obj.worldPosition = lerp(self.startPos, self.endPos, percent)
			self.moving = False
		#obj.worldPosition = [obj.position.x + x,obj.position.y + y,obj.position.z]
		return percent
		
	def moveUnit(self, obj, dir, steps):
		x = 0
		y = 0
		
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
		
def lerp(startPos, endPos, percent):
	x = startPos[0] + percent*(endPos[0] - startPos[0])
	y = startPos[1] + percent*(endPos[1] - startPos[1])
	return([x, y, startPos[2]])