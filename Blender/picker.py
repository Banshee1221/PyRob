import bge

class pickup:

	scores = {'pickup':50}
	
	def __init__(self):
		pass
		
	def evaluate(self, object):
		toStr = str(object)
		
		if toStr in scores:
			return scores[toStr]
			
		return -1