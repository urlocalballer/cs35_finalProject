import pygame
import random
from defs import *

class Bird():

    def __init__(self, gameDisplay): #Initializes the bird. As this is always created in the same space and only once, it doesn't include many inputs
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0 #need this for machine learning. Need some way to judge how the bird is performing
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):   #same as pipe class
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt): #Move is complicated due to how gravity as well as player inputs affect movement

        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt) #This uses a basic equation of motion. D = VT+A(T^2)
        new_speed = self.speed + (GRAVITY * dt) #Also uses a basic equation. V2 = V1 + AT
        #Equations don't need to be complicated!! As long as it works, use it!

        self.rect.centery += distance #Moves the bird by distance to the right
        self.speed = new_speed  #Updates speed of the bird

        if self.rect.top < 0:   #sets speed to zero if we hit the top of the screen
            self.rect.top = 0
            self.speed = 0

    def jump(self): #if we hit the spacebar we are reset to the start speed
        self.speed = BIRD_START_SPEED

    def draw(self): #draws self
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self): #checks if the bird is dead
        if self.rect.bottom > DISPLAY_H:    #Only dead if bird is at the bottom of the screen
            self.state = BIRD_DEAD
            print('Birdie died')

    def update(self, dt):
        if self.state == BIRD_ALIVE:    #if the bird is alive
            self.time_lived += dt   #increase its fitness
            self.move(dt)   #move it
            self.draw() #make it
            self.check_status() #see if it died
            #and repeat



























