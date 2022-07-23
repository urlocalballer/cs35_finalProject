import pygame
import random
from defs import *


class Pipe():

    def __init__(self, gameDisplay, x, y, pipe_type):
        self.gameDisplay = gameDisplay
        self.state = PIPE_MOVING
        self.pipe_type = pipe_type
        self.img = pygame.image.load(PIPE_FILENAME)
        self.rect = self.img.get_rect()
        if pipe_type == PIPE_UPPER: #If the pipe is an upper pipe, it gets moved up
            y = y - self.rect.height
        self.set_position(x, y)

    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0:
            self.state = PIPE_DONE

    def update(self, dt):
        if self.state == PIPE_MOVING:
            self.move_position(-(PIPE_SPEED * dt), 0)
            self.draw()
            self.check_status()


class PipeCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.pipes = []


    def add_new_pipe_pair(self, x): #creates a pair of pipes on top and bottom to travel at the same time

        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE)  #top pipe goes in at a random y position
        bottom_y = top_y + PIPE_GAP_SIZE #Bottom pipe goes in at the same random y position plus the length of a pipe and a gap

        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER) #creates upper pipe
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER) #creates lower pipe

        self.pipes.append(p1) #adds pipes to pipe list
        self.pipes.append(p2)

    def create_new_set(self):   #This creates the two beginning pipes at the beginning of the screen
        self.pipes = [] #only pipes there are
        placed = PIPE_FIRST

        while placed < DISPLAY_W:   #New pipes are added after the first pair so that the screen isn't empty 
            self.add_new_pipe_pair(placed)
            placed += PIPE_ADD_GAP

    def update(self, dt):   #This updates all of the pipes

        rightmost = 0   #rightmost position of most recently added pipe.

        for p in self.pipes:    #updates the position of every pipe and then if it has the highest x position, it is now the rightmost pipe
            p.update(dt)
            if p.pipe_type == PIPE_UPPER:
                if p.rect.left > rightmost:
                    rightmost = p.rect.left

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP):  #If there is a length of the pipe gaps after all pipes, we add a new pipe
            self.add_new_pipe_pair(DISPLAY_W)

        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING]  #we then update the list of pipes to include this new pipe, and then removes pipes from this list that have passed the left hand of the screen

































































