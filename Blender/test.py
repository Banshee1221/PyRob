import bge
import mathutils
import move
import time
import ast

class tester:
	
	def __init__(self):
		scene = bge.logic.getCurrentScene()
		objList = scene.objects
		obj_name = 'Cube'
		self.Cube = objList[obj_name]
		self.lines = []
		self.counter = 0
		self.timer = time.time()+1
		self.passed = False
		self.moved = False
		
	def setText(self, stri):
		#print(stri)
		self.text = stri
		self.lines = stri.split('\n')
	
	def run(self):
				
		error = -1
		if self.counter < len(self.lines):
	
			print(str(self.text))
			print(self.compile_check(str(self.text)))
			print(valid_check(str(self.text)))

		
			#print(str(tmp.x) + " | " + str(tmp.y))

			if self.timer < time.time():
				print("Hello!")
				self.timer = time.time()+1
				try:
					codeobj = compile(str(self.text), '', 'exec')
					eval(codeobj, globals(), locals())
				except AttributeError as e:
					print(e)
				self.counter += 1	
		
		
		else:
			self.counter = 0
			self.lines = []
			
		return error
		
	def compile_check(self, code):
		try:
			compile(code, '<string>', 'single')
		except SyntaxError as e:
			print("Error executing code!\n=====================\nLine:\t{0}\nSnip:\t{1}\nIssue:\t{2}".format(e.lineno, e.text, e))
			return False
		
		return True
		
def valid_check(code):
	try:
		node = ast.parse(code)
		#print(ast.dump(node))
	except SyntaxError:
		return False
	return True
	

	
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
	
