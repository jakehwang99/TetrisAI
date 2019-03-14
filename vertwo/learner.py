import pyautogui
import tetrominoes
import time
import matris

import tenv
import tagent

class Learner:
	board = dict()
	
	env = None
	agent = None
	
	def __init__(self, session, matris, timewait):
		self.env = tenv.Environment(session, matris)
		self.agent = tagent.Agent(learningrate = 0.3, discount = 0.7)
		
		matris.redraw()
		
		while self.update(session, matris, timewait):
			if timewait >= 0.5:
				print("learning")
			
		print("session done\n")
	
	def demoaction(self, session, matris):
		session.request_movement('left')
		matris.redraw()
		time.sleep(1)
		
		session.request_movement('right')
		matris.redraw()
		time.sleep(1)
		
		session.hard_drop()
		matris.redraw()
		time.sleep(1)
		
		session.hard_drop()
		matris.redraw()
		time.sleep(1)
		
		session.hard_drop()
		matris.redraw()
		time.sleep(1)
		
	
	def update(self, session, matris, timewait):
		currentstate = self.env.updatestate()
		currentblock = self.convertblock(session.current_tetromino)
		
		currentaction, currentmask, currenti = self.agent.takeaction(session, currentstate, currentblock)
		
		matris.redraw()
		time.sleep(timewait)
		
		if timewait < 0.5:
			nextstate = self.env.updatestate()
			nextblock = self.convertblock(session.current_tetromino)
			reward = self.env.sendreward(defaultreward = 2, linereward = 3)
			
			if self.env.checkfail():
				print(self.agent.updateq(currentstate, currentmask, currenti, currentblock, currentaction, -1, nextstate, nextblock))
				return False
			else:
				print(self.agent.updateq(currentstate, currentmask, currenti, currentblock, currentaction, reward, nextstate, nextblock))
		else:
			print(self.env.highestpoint())
			if self.env.highestpoint() >= 18:
				return False
		return True
		
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
