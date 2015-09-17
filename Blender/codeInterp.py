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
	actionsLen = 0
	step = 1
	winObj = ""
	
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
		
		
		for i in bge.logic.getCurrentScene().objects:
			if "win" in str(i):
				self.winObj = bge.logic.getCurrentScene().objects[str(i)]
		#print(self.winObj)	
		if (self.text != ''):
			tmp = while_check(str(self.text))
			self.text = tmp
			print(str(self.text))
			print(self.compile_check(str(self.text)))
			print(valid_check(str(self.text)))

			try:
				codeobj = compile(str(self.text), '<string>', 'exec')
				eval(codeobj, globals(), locals())
				self.actionsLen = len(self.actions)
				self.step = 1
				self.text = ''
				print(self.actions)
			except Exception as e:
				self.text = ''
				return e
				
		if (len(self.actions) > 0):
			currItem = self.actions[0]
			if list(currItem.items())[0][0] == 'move':
				checker = self.m.moveUnitOne(self.Cube, list(currItem.items())[0][1], self.winObj)
				if checker == -1:
					print("Error!")
					self.step += 1
					del self.actions[:]
					
				elif checker == 1:
					self.step += 1
					del self.actions[0]
					
				elif checker == 2:
					self.step += 1
					del self.actions[0]
					return -2
		
		if len(self.actions) == 0:
			return 0
		
		return (self.step / self.actionsLen)
		
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

def while_check(code):
	tab = False
	pass1 = False
	tmpArr = code.split('\n')
	lineCount = 0
	wordList = ["_tmpWhileTrackCounter = 0","_tmpWhileTrackCounter += 1", "if _tmpWhileTrackCounter >= 21:", "break"]
	for all in tmpArr:
		if pass1:
			lineCount += 1
			pass
		elif "while" in all:
			if "\t" in all or "\t" in tmpArr[lineCount + 1]:
				tab = True
			spacing = len(all) - len(all.lstrip())
			spacing1 = len(tmpArr[lineCount + 1]) - len(tmpArr[lineCount + 1].lstrip())
			#print(spacing)
			if tab:
				tmpArr.insert(lineCount, wordList[0].rjust(len(wordList[0]) + spacing, "\t"))
				tmpArr.insert(lineCount + 2, wordList[1].rjust(len(wordList[1]) + spacing1, "\t"))
				tmpArr.insert(lineCount + 3, wordList[2].rjust(len(wordList[2]) + spacing1, "\t"))
				tmpArr.insert(lineCount + 4, wordList[3].rjust(len(wordList[3]) + spacing1 + 1, "\t"))
				pass1 = True
			else:
				tmpArr.insert(lineCount, wordList[0].rjust(len(wordList[0]) + spacing))
				tmpArr.insert(lineCount + 2, wordList[1].rjust(len(wordList[1]) + spacing1))
				tmpArr.insert(lineCount + 3, wordList[2].rjust(len(wordList[2]) + spacing1))
				tmpArr.insert(lineCount + 4, wordList[3].rjust(len(wordList[3]) + spacing1 + 4))
				pass1 = True
		lineCount += 1
	
	retVal = '\n'.join([str(x) for x in tmpArr])
	#print(retVal)
	return retVal
			
	
def main(self):
	print("wot")
