import pygame
from defs import *

def update_label(data, title, font, x, y, gameDisplay):
    """
    This function takes in data and renders it and then displays it on the screen in the upper left.
    data: number
    title: label
    font: font
    x: x placement
    y: y placement
    gameDisplay: display to output to
    """
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, font):
    """
    updates data and labels
    """
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)


def run_game():

    pygame.init()   #Initializes pygame- needed to run any game
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))    #set width and height of display as well as keep reference name for display
    pygame.display.set_caption('Learn to fly')  #sets title of window

    running = True  #for while loop
    bgImg = pygame.image.load(BG_FILENAME)  #loads background image and keeps reference name
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)   #Creates a font to use for labels in top left

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0

    while running:

        dt = clock.tick(FPS)    #keeps track of how much game time has elapsed as well as sets frames per second
        game_time += dt

        gameDisplay.blit(bgImg, (0, 0)) #puts a blit on the display


        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #stops the loop running the game and display if user quits
                running = False
            elif event.type == pygame.KEYDOWN:  #stops the loop running the game and display if user presses a down key(?)
                running = False

        update_data_labels(gameDisplay, dt, game_time, label_font)

        pygame.display.update() #updates the display



if __name__== "__main__":
    run_game()

































