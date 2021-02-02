import pygame
import sys
import random
import time
import threading

xright = [0,0,0]
yright = [348,370,398]

xdown = [755,729,697]
ydown = [0,0,0]

xleft = [1400,1400,1400]
yleft = [498,466,436]

xup = [602,630,657]
yup = [800,800,800]

rightSignalCoods = (530,230)
downSignalCoods = (810,230)
upSignalCoods = (530,550)
leftSignalCoods = (810,550)

rightSignalTimerCoods = (510,230)
downSignalTimerCoods = (840,230)
upSignalTimerCoods = (510,552)
leftSignalTimerCoods = (840,552)

rightSignalTimer = 30
downSignalTimer = 30
upSignalTimer = 30
leftSignalTimer = 30

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, lane, vehicleClass, direction):
        pygame.sprite.Sprite.__init__(self)
        if(direction=='left'):
            self.lane = lane
            self.x = xleft[lane]
            self.y = yleft[lane]
            if(vehicleClass=='car'):
                self.image = pygame.image.load('left/car.png')
            elif(vehicleClass=='bus'):
                self.image = pygame.image.load('left/bus.png')
            elif(vehicleClass=='truck'):
                self.image = pygame.image.load('left/truck.png')
            elif(vehicleClass=='rickshaw'):
                self.image = pygame.image.load('left/rickshaw.png')
            elif(vehicleClass=='bike'):
                self.image = pygame.image.load('left/bike.png')
        elif(direction=='up'):
            self.x = xup[lane]
            self.y = yup[lane]
            if(vehicleClass=='car'):
                self.image = pygame.image.load('up/car.png')
            elif(vehicleClass=='bus'):
                self.image = pygame.image.load('up/bus.png')
            elif(vehicleClass=='truck'):
                self.image = pygame.image.load('up/truck.png')
            elif(vehicleClass=='rickshaw'):
                self.image = pygame.image.load('up/rickshaw.png')
            elif(vehicleClass=='bike'):
                self.image = pygame.image.load('up/bike.png')
        elif(direction=='right'):
            self.x = xright[lane]
            self.y = yright[lane]
            if(vehicleClass=='car'):
                self.image = pygame.image.load('right/car.png')
            elif(vehicleClass=='bus'):
                self.image = pygame.image.load('right/bus.png')
            elif(vehicleClass=='truck'):
                self.image = pygame.image.load('right/truck.png')
            elif(vehicleClass=='rickshaw'):
                self.image = pygame.image.load('right/rickshaw.png')
            elif(vehicleClass=='bike'):
                self.image = pygame.image.load('right/bike.png')
        elif(direction=='down'):
            self.x = xdown[lane]
            self.y = ydown[lane]
            if(vehicleClass=='car'):
                self.image = pygame.image.load('down/car.png')
            elif(vehicleClass=='bus'):
                self.image = pygame.image.load('down/bus.png')
            elif(vehicleClass=='truck'):
                self.image = pygame.image.load('down/truck.png')
            elif(vehicleClass=='rickshaw'):
                self.image = pygame.image.load('down/rickshaw.png')
            elif(vehicleClass=='bike'):
                self.image = pygame.image.load('down/bike.png')
        

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def moveRight(self):
        self.x += 4

    def moveDown(self):
        self.y += 4

    def moveLeft(self):
        self.x -= 4
   
    def moveUp(self):
        self.y -= 4

def refresh(screen, simulation):
    global rightSignalTimer, downSignalTimer, upSignalTimer, leftSignalTimer
    while True:
        rightSignalTimer -= 1
        downSignalTimer -= 1
        upSignalTimer -= 1
        leftSignalTimer -= 1
        time.sleep(1)

class Main:
    pygame.init()
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0) 
    blue = (0, 0, 128)
    screenSize = (1400,800)
    background = pygame.image.load('mod_int.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    simulation = pygame.sprite.Group()

    redSignal = pygame.image.load('signals/red.png')
    yellowSignal = pygame.image.load('signals/yellow.png')
    greenSignal = pygame.image.load('signals/green.png')
    font = pygame.font.Font(None, 30)
    
    counter = 0
    
    vehicle = Vehicle(1,'car','left')
    simulation.add(vehicle)
    counter = counter + 1
    thread = threading.Thread(target=refresh, args=(screen, simulation))
    thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background,(0,0))
        screen.blit(redSignal, rightSignalCoods)
        screen.blit(redSignal, downSignalCoods)
        screen.blit(greenSignal, upSignalCoods)
        screen.blit(redSignal, leftSignalCoods)

        rightSignalText = font.render(str(rightSignalTimer), True, white, black)
        downSignalText = font.render(str(downSignalTimer), True, white, black)
        upSignalText = font.render(str(upSignalTimer), True, white, black)
        leftSignalText = font.render(str(leftSignalTimer), True, white, black)
        screen.blit(rightSignalText,rightSignalTimerCoods)       
        screen.blit(downSignalText,downSignalTimerCoods)
        screen.blit(upSignalText,upSignalTimerCoods)
        screen.blit(leftSignalText,leftSignalTimerCoods) 
        for vehicle in simulation:
            vehicle.render(screen)
            vehicle.moveLeft()
        pygame.display.flip()

Main()

