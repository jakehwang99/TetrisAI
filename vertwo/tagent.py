from collections import defaultdict
import pyautogui
import time
import matris

class Agent:
	#qvalues: input is block, dict: input is (mask + action)
	qvalues = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]
	alpha = 0
	gamma = 0
	age = 0

	def __init__(self, learningrate = 0.5, discount = 0.5):
		self.alpha = learningrate
		self.gamma = discount
		print(learningrate,discount)
	
	def sendmask(self, state, width):
		mask = []
		for i in range(10 - width + 1):
			con = ""
			for j in range(width - 1):
				con = con + str(state[i+j]) + ","
			mask.append(con)
		return mask
	
	def maxaction(self, state, block):
		table = self.qvalues[block]
		bestaction = -1
		bestmask = -1
		besti = -1
		bestq = -999
		
		mask2 = self.sendmask(state, 2)
		mask3 = self.sendmask(state, 3)
		mask4 = self.sendmask(state, 4)
		
		if self.age % 2 == 0:
			if block == 0:
				#(no flip) mask4: N
				for i in range(len(mask4)):
					if bestq < table[mask4[i] + "0"]:
						bestaction = 0
						bestmask = 4
						besti = i
						bestq = table[mask4[i] + "0"]
				#(1 flip) mask2: L, N
				for j in range(2):
					for i in range(len(mask2)):
						if bestq < table[mask2[i] + str(j)]:
							bestaction = j + 1
							bestmask = 2
							besti = i
							bestq = table[mask2[i] + str(j)]
						
			elif block == 1:
		
				#(no flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[i] + "0"]:
						bestaction = 0
						bestmask = 2
						besti = i
						bestq = table[mask2[i] + "0"]

			elif block == 3 or block == 4:
		
				#(no flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[i] + "0"]:
						bestaction = 0
						bestmask = 3
						besti = i
						bestq = table[mask3[i] + "0"]
			
				#(flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[i] + "1"]:
						bestaction = 1
						bestmask = 2
						besti = i
						bestq = table[mask2[i] + "1"]
					
			else:
			#make more compact, combine for loops
				#(no flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[i] + "0"]:
						bestaction = 0
						bestmask = 3
						besti = i
						bestq = table[mask3[i] + "0"]
				
				#(flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[i] + "1"]:
						bestaction = 1
						bestmask = 2
						besti = i
						bestq = table[mask2[i] + "1"]
			
				#(flip/flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[i] + "2"]:
						bestaction = 2
						bestmask = 3
						besti = i
						bestq = table[mask3[i] + "2"]
					
				#(flip/flip/flip/right) mask4: N
				for i in range(len(mask2)):
					if bestq < table[mask2[i] + "3"]:
						bestaction = 3
						bestmask = 2
						besti = i
						bestq = table[mask2[i] + "3"]
		else:
			if block == 0:
				#(no flip) mask4: N
				for i in range(len(mask4)):
					if bestq < table[mask4[len(mask4) - i - 1] + "0"]:
						bestaction = 0
						bestmask = 4
						besti = len(mask4) - i - 1
						bestq = table[mask4[len(mask4) - i - 1] + "0"]
				#(1 flip) mask2: L, N
				for j in range(2):
					for i in range(len(mask2)):
						if bestq < table[mask2[len(mask2) - i - 1] + str(j)]:
							bestaction = j + 1
							bestmask = 2
							besti = len(mask2) - i - 1
							bestq = table[mask2[len(mask2) - i - 1] + str(j)]
						
			elif block == 1:
		
				#(no flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[len(mask2) - i - 1] + "0"]:
						bestaction = 0
						bestmask = 2
						besti = len(mask2) - i - 1
						bestq = table[mask2[len(mask2) - i - 1] + "0"]

			elif block == 3 or block == 4:
		
				#(no flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[len(mask3) - i - 1] + "0"]:
						bestaction = 0
						bestmask = 3
						besti = len(mask3) - i - 1
						bestq = table[mask3[len(mask3) - i - 1] + "0"]
			
				#(flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[len(mask2) - i - 1] + "1"]:
						bestaction = 1
						bestmask = 2
						besti = len(mask2) - i - 1
						bestq = table[mask2[len(mask2) - i - 1] + "1"]
			else:
				#make more compact, combine for loops
				#(no flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[len(mask3) - i - 1] + "0"]:
						bestaction = 0
						bestmask = 3
						besti = len(mask3) - i - 1
						bestq = table[mask3[len(mask3) - i - 1] + "0"]
				
				#(flip) mask2: N
				for i in range(len(mask2)):
					if bestq < table[mask2[len(mask2) - i - 1] + "1"]:
						bestaction = 1
						bestmask = 2
						besti = len(mask2) - i - 1
						bestq = table[mask2[len(mask2) - i - 1] + "1"]
			
				#(flip/flip) mask3: N
				for i in range(len(mask3)):
					if bestq < table[mask3[len(mask3) - i - 1] + "2"]:
						bestaction = 2
						bestmask = 3
						besti = len(mask3) - i - 1
						bestq = table[mask3[len(mask3) - i - 1] + "2"]
					
				#(flip/flip/flip/right) mask4: N
				for i in range(len(mask2)):
					if bestq < table[mask2[len(mask2) - i - 1] + "3"]:
						bestaction = 3
						bestmask = 2
						besti = len(mask2) - i - 1
						bestq = table[mask2[len(mask2) - i - 1] + "3"]
		
		if bestmask == 2:
			return bestaction, mask2, bestmask, besti
		elif bestmask == 3:
			return bestaction, mask3, bestmask, besti
		else:
			return bestaction, mask4, bestmask, besti
	
	
	#greedy policy
	def takeaction(self, session, state, block):
		nextaction, mask, bestwidth, besti = self.maxaction(state, block)
		
		#take catered action
		#time.sleep(1)
		self.inputcommand(session, block, nextaction, bestwidth, besti)
		session.hard_drop()#pyautogui.press('space')
		
		self.age += 1
		
		return nextaction, mask, besti
	
	def inputcommand(self,session, block, action, width, i):
	
		#calculate shift blocks need to move
		shift = i - 3
		if width == 2:
			shift = shift - 1
	
		#flip blocks based on action
		if block != 0:
			for i in range(action):
				session.request_rotation()#pyautogui.press('up')
				if i == 3:
					session.request_movement("right")#pyautogui.press('right')
		
		#special case for block 0
		if block == 0 and action != 0:
			session.request_rotation()#pyautogui.press('up')
			if action == 1:
				session.request_movement("left")#pyautogui.press('left')
				
		#translate based on shift
		for i in range(abs(shift)):
			if shift < 0:
				session.request_movement("left")#pyautogui.press('left')
			else:
				session.request_movement("right")#pyautogui.press('right')
		
	#updates q-value table
	def updateq(self, state, mask, besti, block, action, reward, nextstate, nextblock):
		table = self.qvalues[block]
		curq = table[mask[besti] + str(action)]
		nextaction, nextmask, masknum, nexti = self.maxaction(nextstate,nextblock)
		curnextq = table[nextmask[nexti] + str(nextaction)]
		newq = curq + self.alpha * (reward + (self.gamma * curnextq) - curq)
		table[mask[besti] + str(action)] = newq
		return curq, newq
		
	#if agent failed, will attempt to reset board
	def resetboard(self):
		print("resetting")
		#pyautogui.press('esc')
		time.sleep(0.25)
		#pyautogui.press('enter')
