import pygame
import random
from defs import *

class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):

        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self):
        self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):  #Note: parentheses are (self, pipes). That means we are making a reference to the pipes class
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes)

    def check_hits(self, pipes):    #Note: parentheses are (self, pipes). That means we are making a reference to the pipes class
        for p in pipes: #loops over every pipe
            if p.rect.colliderect(self.rect):   #this checks if the two rectangles are colliding
                self.state = BIRD_DEAD  #if they are, we set the bird to be dead
                break   #and stop right there. There's no reason to check other pipes

    def update(self, dt, pipes):    #Note: parentheses are (self, pipes). That means we are making a reference to the pipes class
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.draw()
            self.check_status(pipes)



























