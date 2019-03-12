import matris

class Environment:

	game = None
	session = None
	linescore = 0
	
	def __init__(self, session, matris):
		self.game = matris
		self.session = session
		
		
	def updatestate(self):
		board = self.session.matrix
		contour = []
		state = []
		for j in range(10):
			for i in range(22):
				if board[(i,j)] != None:
					contour.append(i)
					break
				if i == 21:
					contour.append(22)
					
		for i in range(len(contour) - 1):
			state.append(contour[i] - contour[i + 1])
		
		return state
		
		
	def isgap(self):
		board = self.session.matrix
		topcontour = []
		botcontour = []
		
		for j in range(10):
			for i in range(22):
				if board[(i,j)] != None:
					topcontour.append(i)
					break
				if i == 21:
					topcontour.append(22)
					
		for j in range(10):
			for i in range(22):
				if board[(21-i,j)] == None:
					botcontour.append(22-i)
					break
					
		return topcontour != botcontour
	
	
	def highestpoint(self):
		board = self.session.matrix
		high = 23
		
		for j in range(10):
			for i in range(22):
				if board[(i,j)] != None and high > i:
					high = i
					break
		return 22 - high
		
	def sendreward(self, defaultreward = 1, linereward = 5):
		reward = defaultreward
		if self.linescore < self.session.lines:
			reward = (self.session.lines - self.linescore) * linereward
			self.linescore = self.session.lines
		return reward
	
	def checkfail(self):
		if self.isgap():
			return True
		if self.highestpoint() >= 20:
			return True
		return False
