import bge
def main(self):
	print ('ero')

class test:
	def __init__(self):
		scene = bge.logic.getCurrentScene()
		objList = scene.objects
		obj_name = 'Cube'
		self.cube = objList[obj_name]
		self.test = True
	
	def change(self):
		if self.test:
			self.cube.worldPosition = [1, 2, 3]
			self.test = False
		else:
			self.cube.worldPosition = [-2, -2, 2]
			self.test = True
