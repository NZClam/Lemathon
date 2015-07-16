import pygame, sys, time
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Lemathon')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# read from sprite sheet
SPRITESHEET = pygame.image.load('sprites_amiga.png').convert()

# select a single sprite
def readSprite(x, y, width, height, sheet=SPRITESHEET):
    rect = pygame.Rect(x, y, width, height)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0,0), rect)
    return image

# load sprites
SPRITES = {'Walker':[]}
i = 1
x = 18
y = 0
while(i <= 8):
    SPRITES['Walker'].append(readSprite(x, y, 10, 10))
    i += 1
    x += 16

# spawn a lemming
char = pygame.Rect(200, 100, 10, 10)
action = 'Walker'

# frame id for walker loop
frame = 0

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
    frame = (frame + 1) % 8
    char.left += 1
    windowSurface.blit(SPRITES[action][frame], char)

    # draw the window onto the screen
    pygame.display.update()
    mainClock.tick(15)
