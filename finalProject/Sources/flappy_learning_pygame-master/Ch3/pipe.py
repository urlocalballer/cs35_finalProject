import pygame
import random
from defs import *


class Pipe():

    def __init__(self, gameDisplay, x, y, pipe_type):
        """
        gameDisplay is current display pipe is rendered on
        x is current x position of top left of pipe
        y is current y position of top left of pipe
        pipe_type shows if the pipe moves or not
        """
        self.gameDisplay = gameDisplay  #sets it so that the pipe is displayed on current display
        self.state = PIPE_MOVING    #sets it so that this is a moving pope
        self.pipe_type = pipe_type  #Sets the pipe speed
        self.img = pygame.image.load(PIPE_FILENAME) #sets the image file used for the pipe
        self.rect = self.img.get_rect() #defines the rectangle for the pipe by making it reliant on the dimensions of the png
        self.set_position(x, y) #sets position of the pipe at the inputted x and y
        print('PIPE_MOVING')

    def set_position(self, x, y):   #Sets the position of the pipe by updating where its rectangle is located, or defined movememnt by current position
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy): #Moves the pipe by deltaX and deltaY, or defined movement by change in posiiton
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self): #uses blit to draw rectangle on display
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self): #This checks if the current x position of the top left of the pipe is off the screen
        if self.rect.right < 0:
            self.state = PIPE_DONE
            print('PIPE_DONE')

    def update(self, dt):   #updates current position of pipe
        if self.state == PIPE_MOVING:
            self.move_position(-(PIPE_SPEED * dt), 0)   #moves pipe by its speed multiplied by the time since last frame in the negative x
            self.draw() #draw to actually put it at that position
            self.check_status()
