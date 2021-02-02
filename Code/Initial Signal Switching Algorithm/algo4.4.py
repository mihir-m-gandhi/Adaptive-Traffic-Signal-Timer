import random
import math
import time
import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 
import threading

options={
   'model':'./cfg/yolo.cfg',     #specifying the path of model
   'load':'./bin/yolov2.weights',   #weights
   'threshold':0.3     #minimum confidence factor to create a box, greater than 0.3 good
}

tfnet=TFNet(options)    #READ ABOUT TFNET

defaultRed = 150
defaultYellow = 5
defaultGreen = 30
defaultMinimum = 15
defaultMaximum = 60
currentGreen = 0
currentYellow = 0
signals = []
noOfSignals = 4

carTime = 8
bikeTime = 5
rickshawTime = 6 
busTime = 10 

noOfCars = 0
noOfBikes = 0
noOfBuses =0
noOfRickshaws = 0
noOfLanes = 1

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
	repeat()

def setTime():
    global noOfCars, noOfBikes, noOfBuses, noOfRickshaws, noOfLanes
	#getData()
	# greenTime = math.ceil(((noOfCars*carTime) + (noOfRickshaws*rickshawTime) + (noOfBuses*busTime))/noOfLanes) + (noOfBikes*bikeTime)
    fileName = "(currentGreen+1)"+".jpg"
    img=cv2.imread("2.jpg",cv2.IMREAD_COLOR)    #taking input image (colour)           
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   #bgr to rgb
    result=tfnet.return_predict(img)
    print(result)

    for car in result:
        label=car['label']   #extracting label
        print(label)
        if(label=="car"):    # drawing box and writing label
            noOfCars+=1
            # top_left=(car['topleft']['x'],car['topleft']['y'])
            # bottom_right=(car['bottomright']['x'],car['bottomright']['y'])
            # img=cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)    #green box of width 5
            # img=cv2.putText(img,label,top_left,cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)   #image, label, position, font, font scale, colour: black, line width

		

    #plt.imshow(img)
    #plt.show()

    greenTime = math.ceil(((noOfCars*carTime) + (noOfRickshaws*rickshawTime) + (noOfBuses*busTime) + (noOfBikes*bikeTime))/(noOfLanes+1))
    if(greenTime<defaultMinimum):
        greenTime = defaultMinimum
    elif(greenTime>defaultMaximum):
        greenTime = defaultMaximum
    signals[(currentGreen+1)%(noOfSignals)].green = greenTime


thread = threading.Thread(target=setTime, args=())

def repeat():
	global currentGreen, currentYellow
	while(signals[currentGreen].green>0):
		printStatus()
		updateValues()
		if(signals[(currentGreen+1)%(noOfSignals)].red==10):
			print('\a')
			thread.start()
		time.sleep(1)
	signals[(currentGreen+2)%(noOfSignals)].red = signals[(currentGreen+1)%(noOfSignals)].yellow+signals[(currentGreen+1)%(noOfSignals)].green
	signals[currentGreen].green = defaultGreen
	signals[currentGreen].red = defaultRed
	#signals[currentGreen].red = signals[(currentGreen-1)%noOfSignals].red+signals[(currentGreen+1)%(noOfSignals)].green
	print('\a')
	currentYellow = 1
	while(signals[currentGreen].yellow>0):
		printStatus()
		updateValues()
		time.sleep(1)
	currentYellow = 0
	print('\a')
	currentGreen = (currentGreen+1)%noOfSignals
	repeat()

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

def getData():
	global noOfCars, noOfBikes, noOfBuses, noOfRickshaws, noOfLanes
	noOfCars = random.randint(0,10)
	noOfBikes = random.randint(0,10)
	noOfBuses = random.randint(0,10)
	noOfRickshaws = random.randint(0,10)
	noOfLanes = random.randint(2,3)
	print(noOfCars, noOfBikes, noOfRickshaws, noOfBuses, noOfLanes)

def generateRandom():
	r = random.randint(0,75)
	if(r<defaultMinimum):
		r = defaultMinimum
	elif(r>defaultMaximum):
		r = defaultMaximum
	return r

initialization()
