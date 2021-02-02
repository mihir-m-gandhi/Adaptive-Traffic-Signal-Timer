# WINDOW NOT CLOSING
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

leftStop = 810 
rightStop = 580
upStop = 545
downStop = 320

pygame.init()
simulation = pygame.sprite.Group()

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
            if(self.x+self.image.get_rect().width<=rightStop):
              self.x += 4
        elif(self.direction=='down'):
            if(self.y+self.image.get_rect().height<=downStop):
                self.y += 4
        elif(self.direction=='left'):
            if(self.x>=leftStop):
                self.x -= 4
        elif(self.direction=='up'):
            if(self.y>=upStop):
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
    black = (0, 0, 0)
    white = (255, 255, 255)
    screenSize = (1400,800)
<<<<<<< HEAD
    background = pygame.image.load('./mod_int.png')
=======
    background = pygame.image.load('images/mod_int.png')
>>>>>>> 30213bea5b74e3bdbd08d414cd33a6e88f8ab8b8

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

<<<<<<< HEAD
    simulation = pygame.sprite.Group()

    redSignal = pygame.image.load('./signals/red.png')
    yellowSignal = pygame.image.load('./signals/yellow.png')
    greenSignal = pygame.image.load('./signals/green.png')
=======
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
>>>>>>> 30213bea5b74e3bdbd08d414cd33a6e88f8ab8b8
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

    thread = threading.Thread(target=refresh, args=(screen, simulation))
    thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))
        screen.blit(redSignal, rightSignalCoods)
        screen.blit(redSignal, downSignalCoods)
        screen.blit(redSignal, upSignalCoods)
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
            vehicle.move()
        pygame.display.flip()

Main()

