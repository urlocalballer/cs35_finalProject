import pygame
from defs import *
from pipe import PipeCollection
from bird import Bird

def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration', font, x_pos, y_pos + gap, gameDisplay)


def run_game():

    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
    pygame.display.set_caption('Learn to fly')

    running = True
    bgImg = pygame.image.load(BG_FILENAME)
    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    bird = Bird(gameDisplay)


    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    num_iterations = 1  #this shows the number of birds that have been created

    while running:

        dt = clock.tick(FPS)
        game_time += dt

        gameDisplay.blit(bgImg, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                else:
                    running = False

        pipes.update(dt)
        bird.update(dt, pipes.pipes) #remember, the pipe collection is called pipes, so we have to access pipes.pipes

        if bird.state == BIRD_DEAD: #if bird dies
            pipes.create_new_set()  #empty set of pipes and create a new one
            game_time = 0   #reset the fitness score
            bird = Bird(gameDisplay)    #create a new bird
            num_iterations += 1 #increase the number of generations

        update_data_labels(gameDisplay, dt, game_time, num_iterations, label_font)
        pygame.display.update()



if __name__== "__main__":
    run_game()

































