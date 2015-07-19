import pygame, sys, lemming
from pygame.locals import *
from lemming import mainClock, windowSurface

# constants
FPS = 15  # frames per second

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# initialise emtpy lemmings list and level vars
lemmings = []
elapsed_time = 0

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    # spawn lemmings at regular intervals
    if elapsed_time == 0:
        lemmings.append(lemming.Lemming(450,50, scale=4, permanentskills=['Floater']))
        lemmings.append(lemming.Lemming(550,100, scale=4, inverted=1))
        lemmings.append(lemming.Lemming(50,250, scale=4, reversed=1))
        lemmings.append(lemming.Lemming(150,150, scale=4, reversed=1, inverted=1))
        lemmings.append(lemming.Lemming(250,50, scale=4, reversed=1, rotated=1))
        lemmings.append(lemming.Lemming(350,100, scale=4, reversed=1, inverted=1, rotated=1))
        lemmings.append(lemming.Lemming(250,350, scale=4, rotated=1))
        lemmings.append(lemming.Lemming(350,400, scale=4, inverted=1, rotated=1))

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    for i in range(len(lemmings)):
        # move the lemmings
        lemmings[i].move()
        # draw the lemmings onto the surface
        lemmings[i].draw()


    # increment the timer
    elapsed_time += 1

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(FPS)
