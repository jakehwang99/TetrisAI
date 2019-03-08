import time
import pyautogui
import tenv
import tagent

#initializing tetris environment
x, y, width, height = pyautogui.locateOnScreen('temp/home.png',confidence=0.9)
environment = tenv.Tenv(x, y, width, height)

#initializing tetris agent
agent = tagent.Tagent(learningrate=0.7,discount=0.7)

#starting tetris game
pyautogui.moveTo(x+(width/2),y+(height*0.4128))
pyautogui.click()
pyautogui.moveTo(x,y)
time.sleep(2.75)

#start qlearning training
cases = 1
while True:
	age = 0
	time.sleep(0.075)
	board = environment.updateboard()
	while True:
		if age == 0:
			currentstate =[0,0,0,0,0,0,0,0,0,0]
		else:
			currentstate = environment.updatestate()
		currentblock = environment.updateblock()
		#print(currentstate)
		currentaction, mask, besti = agent.takeaction(currentstate, currentblock)
		
		#print(mask)
		
		print("block: " + str(currentblock) + ", besti: " + str(besti) + " [" + mask[besti] + "] action: " + str(currentaction))
		
		print(board)
		
		time.sleep(0.085)
		board = environment.updateboard()
		
		trial = 0
		if cases % 20 == 0:
			print(cases)
			trial = 1
		
		
		if environment.checkfailed(trial) == 1:
			cases += 1
			print(agent.updateq(currentstate, mask, besti, currentblock, currentaction, -5, currentstate, 0))
			print("agent failed")
			agent.resetboard()
			time.sleep(3)
			break
		if trial == 1:
			nextstate = environment.updatestate()#currentstate#environment.sendstate()
			nextblock = environment.updateblock()
			reward = environment.updatereward()
			print(agent.updateq(currentstate, mask, besti, currentblock, currentaction, reward, nextstate, nextblock))
		age += 1
		print()
	
