import pyautogui
import tenv
import tagent
import tetrominoes
import time
import matris

class Learning:
	board = dict()
	
	env = None
	agent = None
	
	currentblock = 0
	currentstate = []
	currentaction = 0
	currenti = 0
	currentmask = []
	
	age = 0
	
	def __init__(self, session, lines, block, board, maxwidth, maxheight):
	
		self.currentblock = self.convertblock(block)
		self.board = board
		
		self.env = tenv.Tenv(board, lines, maxwidth, maxheight)
		self.agent = tagent.Tagent(learningrate = 0.7, discount = 0.7)
		
		self.currentstate = self.env.updatestate(self.board)
		self.currentaction, self.currentmask, self.currenti = self.agent.takeaction(session, self.currentstate, self.currentblock)
		print(self.board)
		print("finished action")
	
	def update(self, session, newlines, newblock, newboard):
	
		#check failstate
		
		print(newboard)
		
		if self.env.checkfailed(0) == 1:
			print("block: " + str(self.currentblock))
			print(self.agent.updateq(self.currentstate, self.currentmask, self.currenti, self.currentblock, self.currentaction, -5, self.currentstate, 0))
			print("agentfailed")
			print()
			time.sleep(2)
			session.gameover()
			#pyautogui.press('escape')
			
			
		nextstate = self.env.updatestate(newboard)
		nextblock = self.convertblock(newblock)
		reward = self.env.updatereward(newlines)
		
		print("block: " + str(self.currentblock))
		print(self.agent.updateq(self.currentstate, self.currentmask, self.currenti, self.currentblock, self.currentaction, reward, nextstate, nextblock))
		
		self.currentblock = nextblock
		self.board = newboard
		
		self.currentstate = nextstate
		self.currentaction, self.currentmask, self.currenti = self.agent.takeaction(session, self.currentstate, self.currentblock)
		print("finished action")
		
	def convertblock(self, block):
		#print(tetrominoes.tetrominoes)
		if block == tetrominoes.tetrominoes["long"]:
			return 0
		elif block == tetrominoes.tetrominoes["square"]:
			return 1
		elif block == tetrominoes.tetrominoes["hat"]:
			return 2
		elif block == tetrominoes.tetrominoes["right_snake"]:
			return 3
		elif block == tetrominoes.tetrominoes["left_snake"]:
			return 4
		elif block == tetrominoes.tetrominoes["left_gun"]:
			return 5
		elif block == tetrominoes.tetrominoes["right_gun"]:
			return 6
