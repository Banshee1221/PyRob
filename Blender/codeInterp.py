import bge
import mathutils
import mover
import time
import ast

class tester:

	staticPosX = -9.5
	staticPosY = -9.5
	staticPosZ = 1.06
	actions = []
	
	def __init__(self):
		scene = bge.logic.getCurrentScene()
		objList = scene.objects
		obj_name = 'Cube'
		self.Cube = objList[obj_name]
		self.text = ''
		self.passed = False
		self.moved = False
		self.m = mover.mover()
		self.running = False
		
	def setText(self, stri):
		self.text = stri
	
	def run(self):
				
		error = ""
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
				self.text = ''
				return e
				
		if (len(self.actions) > 0):
			currItem = self.actions[0]
			if list(currItem.items())[0][0] == 'move':
				checker = self.m.moveUnitOne(self.Cube, list(currItem.items())[0][1])
				if checker == -1:
					print("Error!")
					del self.actions[0]
				elif checker == 1:
					del self.actions[0]
				elif checker == 2:
					del self.actions[0]
					print("WINNER!")
			
		return error
		
	def compile_check(self, code):
		try:
			compile(code, '<string>', 'exec')
		except Exception as e:
			print("Error executing code!\n=====================\nLine:\t{0}\nSnip:\t{1}\nIssue:\t{2}".format(e.lineno, e.text, e))
			return False
		
		return True
	
	def resetPos(self):
		self.Cube.worldPosition = [self.staticPosX, self.staticPosY, self.staticPosZ]
	
	@classmethod
	def move(cls, dir):
		cls.actions.append({'move':dir})
		#self.actions.append[{'open':password}]
		
def moveUp():
	tester.move("n")
	
def moveDown():
	tester.move("s")
	
def moveRight():
	tester.move("e")
	
def moveLeft():
	tester.move("w")
		
def valid_check(code):
	try:
		node = ast.parse(code)
		#print(ast.dump(node))
	except SyntaxError:
		return False
	return True
	
def main(self):
	print("wot")
