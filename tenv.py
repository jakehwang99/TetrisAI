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
	#line score coordinates and dimensions
	xl = 0
	yl = 0
	wl = 0
	hl = 0
	#board coordinates and dimensions
	xb = 0
	yb = 0
	wb = 0
	hb = 0
	#cell coordinates and dimensions
	xc = 0
	yc = 0
	wc = 0
	hc = 0
	
	board = []
	state = []
	#lines = 0	

	def __init__(self, x, y, width, height):
		self.xl = int(x + (width * 0.10987))
		self.yl = int(y + (height * 0.826229))
		self.wl = int(width * 0.14938271604)
		self.hl = int(height * 0.04590163934)
		
		self.xb = int(x + (width * 0.335))
		self.yb = int(y + (height * 0.0673))
		self.wb = int(width * 0.3337)
		self.hb = int(height * 0.8686)

		self.wc = self.wb / 10
		self.hc = self.hb / 20
		self.xc = self.xb + (self.wc / 2)
		self.yc = self.yb + self.hb - (self.hc / 2)
		
		#print(width,height,self.xc,self.yc)
		
		#qvalue = [[0 for x in range(200)] for y in range(32)]
		#where x is each of the number of states, and y is number of actions
		self.board = [[0 for x in range(10)] for y in range(20)]
		#self.lines = 0

	def boardpic(self):
		im = pyautogui.screenshot(region=(self.xb, self.yb, self.wb, self.hb))
		#im.save('temp/board.png')
		return im

	def linepic(self):
		im = pyautogui.screenshot(region=(self.xl, self.yl, self.wl, self.hl))
		im.save('temp/line.png')
		return im

	def updateboard(self):
		imboard = self.boardpic()
		imline = self.linepic()
		
		xcount = self.wc / 2
		ycount = self.hb - (self.hc / 2)
		
		xs = xcount
		ys = ycount
	
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				r,g,b = imboard.getpixel((xcount,ycount))
				if r == 0 and g == 0 and b == 0:
					self.board[i][j] = 0
				else:
					self.board[i][j] = 1
				xcount = xcount + self.wc
				#print(i,j)
			xcount = xs
			ycount = ycount - self.hc
		#print(self.board)
		return self.board

	#send agent what state the tetris board is at
	def updatestate(self):
		state = []
		previous = 0
		
		for j in range(len(self.board[0])):
			for i in range(18):
				if self.board[17-i][j] == 1:
					if j != 0:
						#state = state + str((17 - i + 1) - previous) + ","
						state.append((17-i+1)-previous)
					previous = 17 - i + 1
					break
				if 17 - i == 0:
					if j != 0:
						#state = state + str((17 - i) - previous) + ","
						state.append((17-i)-previous)
					previous = 0
		self.state = state
		return state

	#send agent what block the tetris board is at
	def updateblock(self):
		if self.board[18][6] == 1:
			#print("I")
			return 0
		elif self.board[18][5] == 0:
			#print("S")
			return 3
		elif self.board[19][5] == 1:
			if self.board[18][3] == 1:
				#print("L")
				return 6
			else:
				#print("O")
				return 1
		elif self.board[18][3] == 0:
			#print("Z")
			return 4
		elif self.board[19][4] == 1:
			#print("T")
			return 2
		else:
			#print("J")
			return 5
		return 0

	#send agent reward recieved for action
	def updatereward(self):
		reward = 1		
		try:
			pyautogui.locateOnScreen('temp/line.png',region=(self.xl-5,self.yl-5,self.wl+10,self.hl+10))
		except Exception:
			reward = 5
		return reward
	
	#checks if agent failed (returns 1 when failed)
	def checkfailed(self, trial):
		#check if top of board
		for i in range(10):
			if self.board[17][i] == 1:
				return 1
		
		#check for gaps
		if trial == 0:
			first = 0
			for j in range(len(self.board[0])):
				for i in range(18):
					if self.board[17-i][j] == 1:
						first = 17 - i + 1
						break
					if 17 - i == 0:
						first = 0
				for i in range(18):
					if self.board[i][j] == 0:
						if first != i:
							return 1
						break
		return 0

				
