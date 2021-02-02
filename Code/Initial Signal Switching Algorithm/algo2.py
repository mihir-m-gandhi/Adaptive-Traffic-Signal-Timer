import random
import time

defaultRed = 150
defaultYellow = 5
defaultGreen = 30
defaultMinimum = 15
defaultMaximum = 60
currentGreen = 0
currentYellow = 0
signals = []
noOfSignals = 4

class TrafficSignal:
	def __init__(self, red, yellow, green, minimum, maximum):
		self.red = red
		self.yellow = yellow
		self.green = green
		self.minimum = minimum
		self.maximum = maximum

def initialization():
	ts1 = TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
	signals.append(ts1)
	ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
	signals.append(ts2)
	ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
	signals.append(ts3)
	ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
	signals.append(ts4)
	repeat();

def repeat():
	global currentGreen, currentYellow
	while(signals[currentGreen].green>0):
		printStatus()
		updateValues()
		if(signals[(currentGreen+1)%(noOfSignals)].red==5):
			print('\a')
			signals[(currentGreen+1)%(noOfSignals)].green = generateRandom()
		time.sleep(1)
	signals[(currentGreen+2)%(noOfSignals)].red = signals[(currentGreen+1)%(noOfSignals)].yellow+signals[(currentGreen+1)%(noOfSignals)].green
	signals[currentGreen].green = defaultGreen
	signals[currentGreen].red = defaultRed
	#signals[currentGreen].red = signals[(currentGreen-1)%noOfSignals].red+signals[(currentGreen+1)%(noOfSignals)].green
	print('\a')
	currentYellow = 1;
	while(signals[currentGreen].yellow>0):
		printStatus()
		updateValues()
		time.sleep(1)
	currentYellow = 0;
	print('\a')
	currentGreen = (currentGreen+1)%noOfSignals
	repeat();

def printStatus():
	for i in range(0, noOfSignals):
		if(i==currentGreen):
			if(currentYellow==0):
				print(" GREEN TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
			else:
				print("YELLOW TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
		else:
			print("   RED TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
	print()

def updateValues():
	for i in range(0, noOfSignals):
		if(i==currentGreen):
			if(currentYellow==0):
				signals[i].green-=1
			else:
				signals[i].yellow-=1
		else:
			signals[i].red-=1


def generateRandom():
	r = random.randint(0,75)
	if(r<defaultMinimum):
		r = defaultMinimum
	elif(r>defaultMaximum):
		r = defaultMaximum
	return r

initialization()
