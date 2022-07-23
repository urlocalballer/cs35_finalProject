# Add background image and music

import pygame
from pygame.locals import *
import time
import random
import numpy as np
import scipy.special

DATA_FONT_SIZE = 18
DATA_FONT_COLOR =  (40,40,40)
SNAKE_X_START = 40
SNAKE_Y_START = 40
LEFT_CHANCE = 0
RIGHT_CHANCE = 0.25
UP_CHANCE = 0.5
DOWN_CHANCE = 0.75
FPS = 30
DISPLAY_W = 1000
DISPLAY_H = 800
SNAKE_ALIVE = 1
SNAKE_DEAD = 0
MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
MUTATION_ARRAY_MIX_PERC = 0.5
MUTATION_CUT_OFF = 0.4
MUTATION_BAD_TO_KEEP = 0.1
MUTATION_MODIFY_CHANCE_LIMIT = 0.4
NNET_INPUTS = 5 #CHANGE THIS TO 5
NNET_HIDDEN = 5
NNET_OUTPUTS = 4 #CHANGE THIS MAYBE
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
GENERATION_SIZE = 10
#MAX_DIST = int(1.2*np.sqrt(np.square(DISPLAY_W)+np.square(DISPLAY_H)))
MAX_DIST = 50
#MAX_DIST = 10 Test code


def angle_between(p1, p2): #stolen from https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, snakes, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive', font, x_pos, y_pos + gap, gameDisplay)
    for s in snakes.snakes:
        y_pos = update_label((s.moves_left,s.score,s.fitness),'Snake\'s Stats', font, x_pos, y_pos + gap, gameDisplay)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE
        self.rect = self.image.get_rect()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.state = SNAKE_ALIVE
        self.length = 1
        self.x = [SNAKE_X_START]
        self.y = [SNAKE_Y_START]
        self.fitness = 0
        self.time_lived = 0
        self.moves_left = MAX_DIST
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.score = 0
        self.apple = Apple(parent_screen)
        self.rect = self.image.get_rect()
        self.apple.draw()


    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self, snakes):
        # update body
        #print('being called')
        self.moves_left -= 1
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        if self == snakes[0]:
            self.draw()

    def draw(self):
        if self.state==SNAKE_ALIVE:
            for i in range(self.length):
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def moveSnakeNet(self): #Added this function myself from the flappy bird tutorial. This is for the neural network snake to know which way to turn
        inputs = self.get_inputs()
        probs = self.nnet.get_outputs(inputs)
        # outputs: [upProb, downProb, leftProb, rightProb]
        
        maxIndex = np.where(probs == (max(probs)))[0]
        #print(probs, maxIndex)
        if maxIndex == 0:
            self.move_up()
        elif maxIndex == 1:
            self.move_down()
        elif maxIndex == 2:
            self.move_left()
        elif maxIndex == 3:
            self.move_right()
        # if val > 0.25:
        #     self.move_down()
        # elif val > 0.25:
        #     self.move_up()
        # elif val > 0.25:
        #     self.move_right()
        # else:
        #     self.move_down()

    def reset(self): #Added this function myself from the flappy bird tutorial. Resets the snake.
        self.state = SNAKE_ALIVE
        self.fitness = 0
        self.time_lived = 0
        self.moves_left = MAX_DIST
        self.x = [SNAKE_X_START]
        self.y = [SNAKE_Y_START]

    def update(self, dt, snakes): #Added this function myself from the flappy bird tutorial. updates the values of the snake.
        if self.state == SNAKE_ALIVE:
            self.time_lived += dt
            self.moveSnakeNet()
            self.walk(snakes)
            self.fitness = ((self.score+1)/(self.time_lived+0.01))*200
            if self.moves_left == 0:
                self.score  -=2
                self.state = SNAKE_DEAD
            if self.x[0] < 0 or self.x[0] > DISPLAY_W or self.y[0] < 0 or self.y[0]>DISPLAY_H:
                self.state = SNAKE_DEAD
                

    def get_inputs(self): #Added this function myself from the flappy bird tutorial.
        """
        There's a lot I needed to change with this function. First off, instead of 2 inputs, there's more. 
        We have the distance to the apple, the distance to each of the four walls
        """

        applePos = (self.apple.x,self.apple.y)
        snakePos = (self.x[0],self.y[0])
        angleBTWN = angle_between(applePos,snakePos)

        #hypDist = np.sqrt(np.square(apple.x-self.x[0])+np.square(apple.y-self.y[0]))
        

        inputs = [
            
            ((self.y[0]/DISPLAY_H)*0.99)+0.01,
            ((self.x[0]/DISPLAY_W)*0.99)+0.01,

            #(distToApple/(np.sqrt(np.square(DISPLAY_H)+np.square(DISPLAY_W))) *0.99)+0.01
            ((self.apple.x/DISPLAY_W)*0.99)+0.01,
            ((self.apple.y/DISPLAY_W)*0.99)+0.01,
            ((angleBTWN)/(2*np.pi))
        ]

        return inputs

    def create_offspring(p1, p2, gameDisplay): #Added this function myself from the flappy bird tutorial. Makes a new snake neural network baby
        new_snake = Snake(gameDisplay)
        new_snake.nnet.create_mixed_weights(p1.nnet, p2.nnet) #mixes the neural nets so that their baby interprets data kinda like the both
        return new_snake

class SnakeCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.snakes = []
        self.create_new_generation()

    def create_new_generation(self):
        self.snakes = []
        for i in range(0, GENERATION_SIZE):
            self.snakes.append(Snake(self.gameDisplay))

    def update(self, dt):
        num_alive = 0
        for s in self.snakes:
            
            s.update(dt, self.snakes)

                    

                # snake colliding with itself

            if s.state == SNAKE_ALIVE:
                num_alive += 1

        return num_alive

    def evolve_population(self):

        for s in self.snakes:
            s.fitness += s.time_lived

        self.snakes.sort(key=lambda x: x.fitness) #, reverse=True

        cut_off = int(len(self.snakes) * MUTATION_CUT_OFF) #how many of the good birds from this generation we want to keep
        good_snakes = self.snakes[0:cut_off] #these are the best snakes from this generation
        bad_snakes = self.snakes[cut_off:] #these are the rest
        num_bad_to_take = int(len(self.snakes) * MUTATION_BAD_TO_KEEP) #but we take some of the bad snakes

        for b in bad_snakes: #modifies the weights of the shitty snakes for some variation
            b.nnet.modify_weights()

        new_snakes = []

        idx_bad_to_take = np.random.choice(np.arange(len(bad_snakes)), num_bad_to_take, replace=False)

        for index in idx_bad_to_take: #first we add the bad birds
            new_snakes.append(bad_snakes[index])

        new_snakes.extend(good_snakes)

        children_needed = len(self.snakes) - len(new_snakes)

        while len(new_snakes) < len(self.snakes): #while we still need snakes
            idx_to_breed = np.random.choice(np.arange(len(good_snakes)), 2, replace=False) #take the index of two good snakes to breed
            if idx_to_breed[0] != idx_to_breed[1]: #make sure we don't just make the same snake again
                new_snake = Snake.create_offspring(good_snakes[idx_to_breed[0]], good_snakes[idx_to_breed[1]], self.gameDisplay) #new baby snake
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT: #and maybe we mutate the baby snake too
                    new_snake.nnet.modify_weights()
                new_snakes.append(new_snake) #then add it to the list
        #print(new_snakes[0])
        for s in new_snakes: #reset every new snake
            #print(f'S is {s} with type{type(s)}')

            s.reset()

        self.snakes = new_snakes #and then make this the new new_snakes
        self.snakes.sort(key=lambda x: x.fitness) #, reverse=True


class Nnet:

    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weight_hidden_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))
        self.activation_function = lambda x: scipy.special.expit(x)
        self.softMax = lambda x: scipy.special.softmax(x)

    def get_outputs(self, inputs_list):
        inputs = np.array(inputs_list).T #, ndmin=2
        hidden_inputs = np.dot(self.weight_input_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        final_outputs = self.softMax(final_inputs)
        return final_outputs

    # def get_max_value(self, inputs_list):
    #     outputs = self.get_outputs(inputs_list)
    #     return np.max(outputs

    def modify_weights(self):
        Nnet.modify_array(self.weight_input_hidden)
        Nnet.modify_array(self.weight_hidden_output)

    def create_mixed_weights(self, net1, net2):
        self.weight_input_hidden = Nnet.get_mix_from_arrays(net1.weight_input_hidden,  net2.weight_input_hidden)
        self.weight_hidden_output = Nnet.get_mix_from_arrays(net1.weight_hidden_output,  net2.weight_hidden_output)       

    def modify_array(a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def get_mix_from_arrays(ar1, ar2):

        total_entries = ar1.size
        num_rows = ar1.shape[0]
        num_cols = ar1.shape[1]

        num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERC)
        idx = np.random.choice(np.arange(total_entries),  num_to_take, replace=False)

        res = np.random.rand(num_rows, num_cols)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                index = row * num_cols + col
                if index in idx:
                    res[row][col] = ar1[row][col]
                else:
                    res[row][col] = ar2[row][col]

        return res


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.snakes = SnakeCollection(self.surface)

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if (abs(x1-x2) <= SIZE+300) and (abs(y1-y2) <= SIZE+300):
            return True
        return False

        

    # def display_score(self, num_alive, num_iterations,snakes,game_time): #need to add more to display
    #     bestSnake = snakes.snakes[0]
    #     font = pygame.font.SysFont('arial',30)
    #     alive_counter = font.render(f"Number Alive: {num_alive}",True,(0,0,0))
    #     numIter = font.render(f"Iteration Number: {num_iterations}",True,(0,0,0))
    #     bestSnakeMoves = font.render(f"Moves Left: {bestSnake.moves_left}",True,(0,0,0))
    #     elapsedTime = font.render(f"Elapsed Time: {game_time}",True,(0,0,0))
    #     self.surface.blit(numIter,(10,10))
    #     self.surface.blit(alive_counter,(10,50))
    #     self.surface.blit(bestSnakeMoves,(10,90))
    #     self.surface.blit(elapsedTime,(10,130))

    # def show_game_over(self):
    #     self.render_background()
    #     font = pygame.font.SysFont('arial', 30)
    #     line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
    #     self.surface.blit(line1, (200, 300))
    #     line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
    #     self.surface.blit(line2, (200, 350))
    #     pygame.mixer.music.pause()
    #     pygame.display.flip()

    def run(self):
        running = True
        pause = False

        snakes = SnakeCollection(self.surface)

        clock = pygame.time.Clock()
        label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)
        game_time = 0
        num_iterations = 1   

        while running:
            bg = pygame.image.load("resources/background.jpg")
            self.surface.blit(bg, (0,0))
            dt = clock.tick(FPS)
            game_time += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False

            
            

            num_alive = snakes.update(dt)
                
            for s in self.snakes.snakes:
                if s.rect.colliderect(s.apple.rect):
                    self.play_sound("ding")
                    s.increase_length()
                    #self.snake.fitness += 1 # we increase the fitness of a snake if it eats an apple
                    s.score += 1
                    s.moves_left += MAX_DIST
                    s.apple.move()

                #print(game_time)
            if num_alive == 0:
                game_time = 0
                snakes.evolve_population()
                num_iterations += 1
            
            
            update_data_labels(self.surface, dt, game_time, num_iterations, num_alive, snakes, label_font)

            pygame.display.update()

            # snake eating apple scenario




    # def play(self, dt):
    #I moved this entire function to just be inside the while Running loop

    #     self.render_background()
    #     self.apple.draw()
    #     self.snake.update(dt, self.apple) #instead of simply walking, the snake updates
        
    #     num_alive = self.snakes.update(dt)

    #     if num_alive == 0:
    #         game_time = 0
    #         self.snakes.evolve_population()
    #         num_iterations += 1
        
    #     self.display_score()
    #     pygame.display.flip()

    #     # snake eating apple scenario
    #     if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
    #         self.play_sound("ding")
    #         self.snake.increase_length()
    #         self.snake.fitness += 1 # we increase the fitness of a snake if it eats an apple
    #         self.apple.move()
            

    #     # snake colliding with itself
    #     for i in range(3, self.snake.length):
    #         if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
    #             self.play_sound('crash')
    #             self.snake.state = SNAKE_DEAD
    #             raise "Collision Occurred"
            

if __name__ == '__main__':
    game = Game()
    game.run()