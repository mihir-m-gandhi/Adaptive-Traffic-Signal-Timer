# DISPLAY COUNT OF VEHICLES PASSED (PER UNIT TIME)
# LAG
# MESAURE OF PERFORMANCE

# *** IMAGE XY COOD IS TOP LEFT
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
   'threshold':0.3  #minimum confidence factor to create a box, greater than 0.3 good
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

carTime = 4
bikeTime = 2
rickshawTime = 3 
busTime = 5

# noOfCars = 0
# noOfBikes = 0
# noOfBuses =0
# noOfRickshaws = 0
noOfLanes = 1

speeds = {'car':1.5, 'bus':1, 'truck':1, 'rickshaw':1.4, 'bike':1.8}
x = {'right':[500,500,500], 'down':[755,727,697], 'left':[810,810,810], 'up':[602,627,657]}
y = {'right':[348,370,398], 'down':[250,250,250], 'left':[498,466,436], 'up':[545,545,545]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

vehicleCountTexts = ["0", "0", "0", "0"]
vehicleCountCoods = [(500,210),(860,210),(860,550),(500,550)]

stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}
image_counter=1
gap = 15
gap2 = 15

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
        self.noOfCars=0
        self.noOfBikes=0
        self.noOfBuses=0
        self.noOfRickshaw=0
        
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0

        vehicles[direction][lane].append(self)

        # self.stop = stops[direction][lane]
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)

        if(direction=='right'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]

            temp = self.image.get_rect().width + gap
            x[direction][lane] -= temp
            stops[direction][lane] -= temp

        elif(direction=='left'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.image.get_rect().width + gap
            x[direction][lane] += temp
            stops[direction][lane] += temp

        elif(direction=='down'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].image.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]
            temp = self.image.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='up'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].image.get_rect().height + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.image.get_rect().height + gap
            y[direction][lane] += temp
            stops[direction][lane] += temp
        time.sleep(0.5)
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.image.get_rect().width>stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if((self.x+self.image.get_rect().width<=self.stop or self.x+self.image.get_rect().width>stopLines[self.direction] or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.image.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - gap2))):                
              self.x += self.speed
        
        elif(self.direction=='down'):
            # if(self in vehicles[self.direction][self.lane]):
            #     index = vehicles[self.direction][self.lane].index(self)
            #     print(index)
            #index = vehicles[self.direction][self.lane].index(self)
            if(self.crossed==0 and self.y+self.image.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if((self.y+self.image.get_rect().height<=self.stop or self.y+self.image.get_rect().height>stopLines[self.direction] or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.image.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - gap2))):                
                self.y += self.speed
            # if(self.y+self.image.get_rect().height>stopLines[self.direction]):
            #     vehicles[self.direction][self.lane].pop(index)
            #     print(len(vehicles[self.direction][self.lane]))
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if((self.x>=self.stop or self.x<stopLines[self.direction] or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + gap2))):                
                self.x -= self.speed
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if((self.y>=self.stop or self.y<stopLines[self.direction] or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height +  gap2))):
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
    setTime(currentGreen)
    signals[currentGreen+1].red=signals[currentGreen].green+signals[currentGreen].yellow
    repeat()
    # repeat()

def setTime(signal_number):
    global image_counter 
    detection_result=detection(signal_number,tfnet,image_counter)
    image_counter+=1
    signals[signal_number].noOfBikes=0
    signals[signal_number].noOfCars=0
    signals[signal_number].noOfBuses=0
    signals[signal_number].noOfRickshaw=0
    for vehicle in detection_result:
        label=vehicle['label']   #extracting label
    
        if(label=="car"):    # drawing box and writing label
            signals[signal_number].noOfCars+=1

            Vehicle(random.randint(1,2),"car", directionNumbers[signal_number])
        elif(label=="truck" or label=="bus"):
            signals[signal_number].noOfBuses+=1
            Vehicle(random.randint(1,2),"bus", directionNumbers[signal_number])

        elif(label=="auto"):
            signals[signal_number].noOfRickshaw+=1
            Vehicle(random.randint(1,2),"auto", directionNumbers[signal_number])

        else:
            signals[signal_number].noOfBikes+=1
            Vehicle(0,"bike", directionNumbers[signal_number])
    
    
    
    greenTime = math.ceil(((signals[signal_number].noOfCars*carTime) + (signals[signal_number].noOfRickshaw*rickshawTime) + (signals[signal_number].noOfBuses*busTime) + (signals[signal_number].noOfBikes*bikeTime))/(noOfLanes+1))
    if(greenTime<defaultMinimum):
        greenTime = defaultMinimum
    elif(greenTime>defaultMaximum):
        greenTime = defaultMaximum
    signals[signal_number].green = greenTime

    print("time set",signal_number)
    print(detection_result)
   
def repeat():
    global currentGreen, currentYellow
    print(threading.currentThread().getName())
    while(signals[currentGreen].green>0):
        printStatus()
        updateValues()
        if(signals[(currentGreen+1)%(noOfSignals)].red==10):
            print('\a')
            thread = threading.Thread(name="detection",target=setTime, args=([(currentGreen+1)%noOfSignals]))
            thread.start()
            # setTime()
        time.sleep(1)
    currentYellow = 1
    vehicleCountTexts[currentGreen] = "0"
    for i in range(0,3):
        stops[directionNumbers[currentGreen]][i] = defaultStop[directionNumbers[currentGreen]]
 
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
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

# def generateVehicles():
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
    # while(True):
    #     vehicle_type = random.randint(0,4)
    #     if(vehicle_type==4):
    #         lane_number = 0
    #     else:
    #         lane_number = random.randint(0,1) + 1
    #     direction_number = random.randint(0,3)
    #     Vehicle(lane_number, vehicleTypes[vehicle_type], directionNumbers[direction_number])
    #     time.sleep(1)

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

    # thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())
    # thread3.start()
    # setTime(currentGreen)
    # repeatThread=threading.Thread(name="repeat",target=repeat)
    # repeatThread.start()
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
            vehicleCountTexts[i] = font.render(str(vehicles[directionNumbers[i]]['crossed']), True, black, white)
            screen.blit(vehicleCountTexts[i],vehicleCountCoods[i])

        for vehicle in simulation:
            vehicle.render(screen)
            vehicle.move()
        pygame.display.flip()

Main()
