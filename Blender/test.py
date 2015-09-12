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
		self.text = ''
		self.actions = []
		self.passed = False
		self.moved = False
		self.m = move.move()
		self.running = False
		
	def setText(self, stri):
		self.text = stri
	
	def run(self):
				
		error = -1
		if (self.text != ''):
			print(str(self.text))
			print(self.compile_check(str(self.text)))
			print(valid_check(str(self.text)))

			try:
				codeobj = compile(str(self.text), '<string>', 'exec')
				eval(codeobj, globals(), locals())
				self.text = ''
				print(self.actions)
			except Exception as e:
				print(e)
				self.text = ''
				
		if (len(self.actions) > 0):
			currItem = self.actions[0]
			if list(currItem.items())[0][0] == 'move':
				checker = self.m.moveUnitOne(self.Cube, list(currItem.items())[0][1])
				if checker == 1:
					del self.actions[0]
			
		return error
		
	def compile_check(self, code):
		try:
			compile(code, '<string>', 'exec')
		except Exception as e:
			print("Error executing code!\n=====================\nLine:\t{0}\nSnip:\t{1}\nIssue:\t{2}".format(e.lineno, e.text, e))
			return False
		
		return True
		
	def move(self, dir):
		self.actions.append({'move':dir})
		#self.actions.append[{'open':password}]
		
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
	
