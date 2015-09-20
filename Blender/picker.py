import bge

class pickup:

	scores = {'pickup':50}
	
	def __init__(self):
		pass
		
	def evaluate(self, player, object):
	
		rayTest = player.rayCastTo([player.localPosition.x, player.localPosition.y, player.localPosition.z - 0.6], 0)
		
		#print(scores)
		#print(scores[str(rayTest)])
		
		try:
			return self.scores[str(rayTest)]
		except:
			return -1