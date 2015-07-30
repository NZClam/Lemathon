import pygame
from pygame.locals import *
import config
from config import *

pygame.init()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Lemathon')

# SPRITES
SPRITESHEET = pygame.image.load('sprites_amiga2p.png').convert()
sprite_size = 16  # pad all sprites to 16x16

# read a single sprite from the sheet
def read_sprite(x, y, width, height, sheet):
    # define a rectangular area on the sheet
    rect = pygame.Rect(x, y, width, height)
    # create a Surface to store the image
    image = pygame.Surface((sprite_size, sprite_size)).convert()
    # copy image from selected are of spreadsheet onto the image surface
    image.blit(sheet, (0,0), rect)
    # set white as transparent
    image.set_colorkey((255, 255, 255))
    return image


# read a row of sprites from the sheet
def read_sprite_row(spritesdict, actionname, xstart, ystart, nsprites, spritesize=16, spritespace=20):
    # initialise dictionary ref
    if actionname not in spritesdict: spritesdict[actionname] = []
    x = xstart
    y = ystart
    for spr in range(nsprites):
        # read sprite and load into dict
        spritesdict[actionname].append(read_sprite(x, y, spritesize, spritesize, SPRITESHEET))
        # move across to next sprite
        x += spritespace


# Load the sprites into sprites dictionary
# See spritesheet image for reference
SPRITES = {}  # initialise
read_sprite_row(SPRITES, 'Walker',     0,  0,   8)
read_sprite_row(SPRITES, 'Ascender', 160,  0,   1)
read_sprite_row(SPRITES, 'Shrugger', 180,  0,   7)
read_sprite_row(SPRITES, 'Shrugger',   0,  20,  1)
read_sprite_row(SPRITES, 'Exiter',    20,  20,  8)
read_sprite_row(SPRITES, 'Faller',     0,  40,  4)
read_sprite_row(SPRITES, 'FloaterStart',  80,  40,  4)
read_sprite_row(SPRITES, 'Floater', 160,  40,  4)
read_sprite_row(SPRITES, 'Floater', 220,  40,  4, spritespace=-20)
read_sprite_row(SPRITES, 'Blocker',    0,  60, 16)
read_sprite_row(SPRITES, 'Climber',    0,  80,  8)
read_sprite_row(SPRITES, 'Hoister',  160,  80,  8)
read_sprite_row(SPRITES, 'Builder',    0, 100, 16)
read_sprite_row(SPRITES, 'Basher',     0, 120, 16)
read_sprite_row(SPRITES, 'Basher',     0, 140, 16)
read_sprite_row(SPRITES, 'Digger',     0, 160,  8)
# infer missing second half of digger animation
read_sprite_row(SPRITES, 'Digger',     1, 160,  8)
for diggersprite in range(8,16):
   SPRITES['Digger'][diggersprite] = pygame.transform.flip(SPRITES['Digger'][diggersprite], True, False)
read_sprite_row(SPRITES, 'Miner',    160, 159,  2)
read_sprite_row(SPRITES, 'Miner',    200, 160,  6)
read_sprite_row(SPRITES, 'Miner',      0, 180, 16)
read_sprite_row(SPRITES, 'Ohnoer',     0, 200, 16)
read_sprite_row(SPRITES, 'Splatter',   0, 220, 16)
read_sprite_row(SPRITES, 'Drowner',    0, 240, 16)
read_sprite_row(SPRITES, 'Burner',     0, 260, 13)
read_sprite_row(SPRITES, 'Exploder', 260, 260,  1)

# Set deltas (dx, dy) per frame for each action
# Blank with the same length as sprites
DELTAS = dict.fromkeys(SPRITES.keys(), [])
for action in DELTAS.keys():
    DELTAS[action] = [(0,0)] * len(SPRITES[action])

# Fill with movement values by replacing zeros
DELTAS['Walker'] = [(1,0)] * len(SPRITES['Walker'])
DELTAS['Ascender'] = [(0,-2)]
DELTAS['Faller'] = [(0,3)] * len(SPRITES['Faller'])
for i in [1,9]: DELTAS['Digger'][i] = (0,1)
for i in list(range(11,16)) + list(range(27,32)): DELTAS['Basher'][i] = (1,0)
DELTAS['Miner'][3] = (2,2)
DELTAS['Miner'][15] = (2,0)
DELTAS['Builder'][0] = (2,-1)
for i in list(range(4,8)): DELTAS['Climber'][i] = (0,-1)
DELTAS['FloaterStart'] = [(0,0), (0,3), (0,0), (0,0)]
DELTAS['Floater'] = [(0,2)] * len(SPRITES['Floater'])
for i in [1,2,3,4]: DELTAS['Hoister'][i] = (0,-2)
