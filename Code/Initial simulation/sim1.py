# RELATIVE PATH

import pygame, sys, random

pygame.init()

xleft = [0,0,0]
yleft = [348,370,398]

xup = [755,729,697]
yup = [0,0,0]

xright = [1400,1400,1400]
yright = [498,466,436]

xdown = [602,630,657]
ydown = [800,800,800]

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, x, y, c, d):
        pygame.sprite.Sprite.__init__(self)
        if(d==1):
            self.x = xleft[x]
            self.y = yleft[y]
            if(c==1):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/left/car.png')
            elif(c==2):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/left/bus.png')
            elif(c==3):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/left/truck.png')
            elif(c==4):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/left/rickshaw.png')
            elif(c==5):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/left/bike.png')
        elif(d==2):
            self.x = xup[x]
            self.y = yup[y]
            if(c==1):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/up/car.png')
            elif(c==2):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/up/bus.png')
            elif(c==3):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/up/truck.png')
            elif(c==4):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/up/rickshaw.png')
            elif(c==5):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/up/bike.png')
        elif(d==3):
            self.x = xright[x]
            self.y = yright[y]
            if(c==1):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/right/car.png')
            elif(c==2):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/right/bus.png')
            elif(c==3):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/right/truck.png')
            elif(c==4):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/right/rickshaw.png')
            elif(c==5):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/right/bike.png')
        elif(d==4):
            self.x = xdown[x]
            self.y = ydown[y]
            if(c==1):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/down/car.png')
            elif(c==2):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/down/bus.png')
            elif(c==3):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/down/truck.png')
            elif(c==4):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/down/rickshaw.png')
            elif(c==5):
                self.image = pygame.image.load('/Users/mihir/Documents/BE_project/sim/down/bike.png')
        

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def moveRight(self):
        # if(self.x > 1400):
        #     self.x = 0
        self.x += 4

    def moveDown(self):
        # if(self.x > 1400):
        #     self.x = 0
        self.y += 4

    def moveLeft(self):
        # if(self.x > 1400):
        #     self.x = 0
        self.x -= 4
   
    def moveUp(self):
        # if(self.x > 1400):
        #     self.x = 0
        self.y -= 4

class Main:
    clock = pygame.time.Clock()

    screenSize = (1400,800)
    background = pygame.image.load('/Users/mihir/Documents/BE_project/sim/mod_int.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    simulation = pygame.sprite.Group()

    redSignal = pygame.image.load('/Users/mihir/Documents/BE_project/sim/signals/red.png')
    yellowSignal = pygame.image.load('/Users/mihir/Documents/BE_project/sim/signals/yellow.png')
    greenSignal = pygame.image.load('/Users/mihir/Documents/BE_project/sim/signals/green.png')
    counter = 0
    
    vehicle = Vehicle(1,1,1,4)
    simulation.add(vehicle)
    counter = counter + 1
    vehicle = Vehicle(2,2,2,4)
    simulation.add(vehicle)
    counter = counter + 1
    vehicle = Vehicle(0,0,5,4)
    simulation.add(vehicle)
    counter = counter + 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))
        screen.blit(redSignal, (530,230))
        screen.blit(redSignal, (810,230))
        screen.blit(greenSignal, (530,550))
        screen.blit(redSignal, (810,550))

        for vehicle in simulation:
            vehicle.render(screen)
            vehicle.moveUp()

        clock.tick(60)

        pygame.display.flip()


Main()

