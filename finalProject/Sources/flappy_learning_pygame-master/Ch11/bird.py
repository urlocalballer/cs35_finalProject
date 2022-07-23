import pygame
import random
from defs import *
from nnet import Nnet

class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS) #Each bird is its own neural net
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

    def jump(self, pipes):
        inputs = self.get_inputs(pipes) #gives you distance from the pipes as calculated by the neural network
        val = self.nnet.get_max_value(inputs)
        if val > JUMP_CHANCE: #if
            self.speed = BIRD_START_SPEED #then jump

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes)

    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes) #jump as part of update process, before resetting position and checking status
            self.draw()
            self.check_status(pipes)


    def get_inputs(self, pipes): #gets the input to be used in neural net

        closest = DISPLAY_W * 2 #assume the closest is the furthest away possible
        bottom_y = 0    #with a defualt value of 0
        for p in pipes: #for every pipe
            if p.pipe_type == PIPE_UPPER and p.rect.right < closest and p.rect.right > self.rect.left: #check if it's closer than the closest and is on our right
                closest = p.rect.right #set it to be the closest
                bottom_y = p.rect.bottom #keep tabs on its y pos


        horizontal_distance = closest - self.rect.centerx #calculating horizontal distance
        vertical_distance = (self.rect.centery) - (bottom_y + PIPE_GAP_SIZE / 2) #calculating vertical distance

        inputs = [ #normalizing distances
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            ((( vertical_distance + Y_SHIFT) / NORMALIZER ) * 0.99 ) + 0.01
        ]

        return inputs



class BirdCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        for b in self.birds:
            b.update(dt, pipes)
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive



















