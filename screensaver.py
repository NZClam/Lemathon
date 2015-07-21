import pygame, sys, random
import lemming, hotkey
from pygame.locals import *
from lemming import mainClock, windowSurface, WINDOWWIDTH, WINDOWHEIGHT

# function to spawn a random lemming
def get_random_lemming():
    randx = random.randint(0,WINDOWWIDTH)
    randy = random.randint(0,WINDOWHEIGHT)
    randscale = random.randint(1,4)
    randreversed = random.randint(0,1)
    randinverted = random.randint(0,1)
    randrotated = random.randint(0,1)
    skills=list(lemming.SPRITES.keys())
    randaction = random.choice(skills)
    return lemming.Lemming(randx,randy,randscale,randreversed,randinverted,randrotated,randaction)

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

        elif event.type == KEYDOWN:
            new_skill = hotkey.get_hotkey_skill(event.key)
            if new_skill:
                for i in range(len(lemmings)):
                    lemmings[i].change_action(new_skill)

            elif event.key == K_r:
                lemmings.append(get_random_lemming())

    pygame.event.clear()

    # spawn lemming at regular intervals
    if elapsed_time % 15 == 0:
        lemmings.append(get_random_lemming())

    # draw the black background onto the surface
    windowSurface.fill((0,0,0))

    for i in range(len(lemmings)):
        # move the lemmings
        lemmings[i].move()
        # draw the lemmings onto the surface
        lemmings[i].draw()


    # increment the timer
    elapsed_time += 1

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(15)
