import pygame, sys, lemming
from pygame.locals import *
from lemming import mainClock, windowSurface

# constants
FPS = 15  # frames per second



# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# spawn a lemming
lem1 = lemming.Lemming(100,100)

# run the game loop
while True:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    # draw the lemming onto the surface
    lem1.frame = (lem1.frame + 1) % lem1.numframes
    lem1.char.left += lem1.xspeed
    lem1.char.top += lem1.yspeed
    windowSurface.blit(lemming.SPRITES[lem1.action][lem1.frame], lem1.char)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(FPS)
