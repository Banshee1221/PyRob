import bge

class pickup:

	scores = {'pickup':50}
	
	def __init__(self):
		pass
		
	def confirmObject(self, player):
		rayTest = player.rayCastTo([player.localPosition.x, player.localPosition.y, player.localPosition.z - 0.6], 0)
		
		try:
			return str(rayTest)
		except:
			return -1
	
	def evaluate(self, player):
		
		rayTest = player.rayCastTo([player.localPosition.x, player.localPosition.y, player.localPosition.z - 0.6], 0)
	
		try:
			return self.scores[rayTest]
		except:
			return -1
		
		#print(scores)
		#print(scores[str(rayTest)])
		
		