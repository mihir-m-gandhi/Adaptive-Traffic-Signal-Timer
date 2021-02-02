# RESET STOP POSITIONS
# VEHICLES STUCK IN BETWEEN
import random
import math
import time
import cv2
from darkflow.net.build import TFNet
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

speeds = {'car':3, 'bus':2.5, 'truck':2.5, 'rickshaw':2.7, 'bike':3.3}
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[]}, 'down': {0:[], 1:[], 2:[]}, 'left': {0:[], 1:[], 2:[]}, 'up': {0:[], 1:[], 2:[]}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

stopLines = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}

gap = 15
gap2 = 20

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
        self.speed = speeds[vehicleClass]
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.stop = stops[direction][lane]
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)
        if(direction=='right'):
            temp = self.image.get_rect().width + gap
            x[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='left'):
            temp = self.image.get_rect().width + gap
            x[direction][lane] += temp
            stops[direction][lane] += temp
        elif(direction=='down'):
            temp = self.image.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='up'):
            temp = self.image.get_rect().height + gap
            y[direction][lane] += temp
            stops[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.x+self.image.get_rect().width<=self.stop or (currentGreen==0 and (self.index==0 or self.x<=(vehicles[self.direction][self.lane][self.index-1].x - vehicles[self.direction][self.lane][self.index-1].image.get_rect().width - gap2)))):                
              self.x += self.speed
        elif(self.direction=='down'):
            if(self.y+self.image.get_rect().height<=self.stop or (currentGreen==1 and (self.index==0 or self.y<=(vehicles[self.direction][self.lane][self.index-1].y - vehicles[self.direction][self.lane][self.index-1].image.get_rect().height - gap2)))):                
                self.y += self.speed
        elif(self.direction=='left'):
            if(self.x>=self.stop or (currentGreen==2 and (self.index==0 or self.x>=(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + gap2)))):                
                self.x -= self.speed
        elif(self.direction=='up'):
            if(self.y>=self.stop or (currentGreen==3 and (self.index==0 or self.y>=(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  gap2)))):
                self.y -= self.speed

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
   detection_result=detection(currentGreen,tfnet)

   for vehicle in detection_result:
      label=vehicle['label']   #extracting label
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

def generateVehicles():
    # Vehicle(0,'bike','right')
    # Vehicle(1,'car','right')
    # Vehicle(2,'bus','right')
    # Vehicle(0,'bike','right')
    # Vehicle(1,'car','right')
    # Vehicle(2,'bus','right')
    # Vehicle(0,'bike','down')
    # Vehicle(1,'car','down')
    # Vehicle(2,'bus','down')
    # Vehicle(0,'bike','down')
    # Vehicle(1,'truck','down')
    # Vehicle(2,'bus','down')
    while(True):
        vehicle_type = random.randint(0,4)
        if(vehicle_type==4):
            lane_number = 0
        else:
            lane_number = random.randint(0,1) + 1
        direction_number = random.randint(0,3)
        Vehicle(lane_number, vehicleTypes[vehicle_type], directionNumbers[direction_number])
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

    thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())
    thread3.start()

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

  
