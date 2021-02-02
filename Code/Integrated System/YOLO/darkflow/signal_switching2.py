import random
import math
import time
import cv2
from darkflow.net.build import  TFNet
import matplotlib.pyplot as plt 
import threading
from vehicle_detection import detection
import pygame
import sys

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

xright = [0,0,0]
yright = [348,370,398]

xdown = [755,729,697]
ydown = [0,0,0]

xleft = [1400,1400,1400]
yleft = [498,466,436]

xup = [602,630,657]
yup = [800,800,800]

signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

leftStop = 810 
rightStop = 580
upStop = 545
downStop = 320

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = "30"
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.direction = direction
        self.x = globals()[("x"+direction)][lane]
        self.y = globals()[("y"+direction)][lane]
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.x+self.image.get_rect().width<=rightStop or currentGreen==0):
              self.x += 4
        elif(self.direction=='down'):
            if(self.y+self.image.get_rect().height<=downStop or currentGreen==1):
                self.y += 4
        elif(self.direction=='left'):
            if(self.x>=leftStop or currentGreen==2):
                self.x -= 4
        elif(self.direction=='up'):
            if(self.y>=upStop or currentGreen==3):
                self.y -= 4

def initialize():
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
   detection_result=detection(currentGreen,tfnet)

   for car in detection_result:
      label=car['label']   #extracting label
      print(label)
      if(label=="car"):    # drawing box and writing label
         noOfCars+=1
      if(label=="truck" or label=="bus"):
         noOfBuses+=1
      


   greenTime = math.ceil(((noOfCars*carTime) + (noOfRickshaws*rickshawTime) + (noOfBuses*busTime) + (noOfBikes*bikeTime))/(noOfLanes+1))
   if(greenTime<defaultMinimum):
      greenTime = defaultMinimum
   elif(greenTime>defaultMaximum):
      greenTime = defaultMaximum
   signals[(currentGreen+1)%(noOfSignals)].green = greenTime
   
def repeat():
   global currentGreen, currentYellow
   while(signals[currentGreen].green>0):
      printStatus()
      updateValues()
      if(signals[(currentGreen+1)%(noOfSignals)].red==10):
         print('\a')
         thread = threading.Thread(name="detection",target=setTime, args=())
         thread.start()
      time.sleep(1)
   currentYellow = 1
   while(signals[currentGreen].yellow>0):
      printStatus()
      updateValues()
      time.sleep(1)
   currentYellow = 0
   signals[currentGreen].yellow = defaultYellow
   signals[(currentGreen+2)%(noOfSignals)].red = signals[(currentGreen+1)%(noOfSignals)].yellow+signals[(currentGreen+1)%(noOfSignals)].green
   signals[currentGreen].green = defaultGreen
   signals[currentGreen].red = defaultRed
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

def refresh(screen, simulation):
    global rightSignalTimer, downSignalTimer, upSignalTimer, leftSignalTimer
    while True:
        rightSignalTimer -= 1
        downSignalTimer -= 1
        upSignalTimer -= 1
        leftSignalTimer -= 1
        time.sleep(1)

class Main:
    thread2 = threading.Thread(name="initialization",target=initialize, args=())
    thread2.start()
    black = (0, 0, 0)
    white = (255, 255, 255)
    screenSize = (1400,800)
    background = pygame.image.load('images/mod_int.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    vehicle = Vehicle(0,'bike','right')
    vehicle = Vehicle(1,'car','right')
    vehicle = Vehicle(2,'bus','right')
    vehicle = Vehicle(0,'bike','left')
    vehicle = Vehicle(1,'car','left')
    vehicle = Vehicle(2,'bus','left')
    vehicle = Vehicle(0,'bike','up')
    vehicle = Vehicle(1,'car','up')
    vehicle = Vehicle(2,'bus','up')
    vehicle = Vehicle(0,'bike','down')
    vehicle = Vehicle(1,'car','down')
    vehicle = Vehicle(2,'bus','down')

    # thread3 = threading.Thread(name="traffic_timer",target=refresh, args=(screen, simulation))
    # thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))
        for i in range(0,noOfSignals):
            if(i==currentGreen):
                if(currentYellow==1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red<=10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "--"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["30","30","30","30"]
        for i in range(0,noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods[i]) 
        for vehicle in simulation:
            vehicle.render(screen)
            vehicle.move()
        pygame.display.flip()

Main()

  
