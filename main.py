import pygame, sys, random
import lemming, config
from pygame.locals import *
from config import WINDOWWIDTH, WINDOWHEIGHT, FPS
from init import windowSurface

# initialise emtpy lemmings list and level vars
lemmings = []
mainClock = pygame.time.Clock()
elapsed_time = 0

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            new_skill = config.get_hotkey_skill(event.key)
            if new_skill:
                for i in range(len(lemmings)):
                    lemmings[i].change_action(new_skill)

    pygame.event.clear()

    # spawn lemming at regular intervals
    if elapsed_time % 15 == 0:
        lemmings.append(lemming.Lemming(100,100,scale=2))

    # draw the black background onto the surface
    windowSurface.fill(0)

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
