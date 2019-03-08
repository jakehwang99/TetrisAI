import pyautogui

#blocks numbering
#	I = 0
#	O = 1
#	T = 2
#	S = 3
#	Z = 4
#	J = 5
#	L = 6
class Tenv:
	board = dict()
	state = []
	lines = 0
	#block = ""
	
	maxw = 0
	maxh = 0

	def __init__(self, board, lines, maxwidth, maxheight):
		self.board = board
		self.lines = lines
		#self.block = block
		
		self.maxw = maxwidth
		self.maxh = maxheight

	#send agent what state the tetris board is at
	def updatestate(self, board):
		state = []
		previous = 0
		self.board = board
		
		#print(board)
		for j in range(10):
			for i in range(22):
				if board[(i,j)] != None:
					if j != 0:
						state.append(i - previous)
					previous = i# - 1
					break
				if i == 21:
					if j != 0:
						#state = state + str((17 - i) - previous) + ","
						state.append(i-previous)
					previous = 21
		self.state = state
		#print(state)
		return state

	#send agent reward recieved for action
	def updatereward(self, newlines):
		reward = 0
		if self.lines != newlines:
			reward = newlines - self.lines
		self.lines = newlines
		return reward
	
	#checks if agent failed (returns 1 when failed)
	def checkfailed(self, trial):
		#check if top of board
		for i in range(self.maxw):
			if self.board[(2, i)] != None:
				print("ceiling")
				return 1
		
		#check for gaps
		if trial == 0:
			first = 0
			for j in range(self.maxw):
				for i in range(self.maxh):
					if self.board[(self.maxh - i - 1, j)] != None:
						first = self.maxh - i
						break
					if self.maxh - i -1 == 0:
						first = 0
				for i in range(self.maxh):
					if self.board[(i,j)] == None:
						if first != i:
							return 1
						break
		return 0

				
