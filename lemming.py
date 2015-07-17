import pygame

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Lemathon')

# Define Lemming class
class Lemming():
    def __init__(self, xpos, ypos):

        self.char = pygame.Rect(xpos, ypos, 10, 10)
        self.action = 'Faller'  # By convention, lemmings fall from hatches
        self.frame = 0
        self.numframes = len(SPRITES[self.action])
        self.xspeed = 0
        self.yspeed = 3


# read from sprite sheet
SPRITESHEET = pygame.image.load('sprites_amiga.png').convert()

# read a single sprite from the sheet
def read_sprite(x, y, width, height, sheet):
    # define a rectangular area on the sheet
    rect = pygame.Rect(x, y, width, height)
    # create a Surface to store the image
    image = pygame.Surface(rect.size).convert()
    # copy image from selected are of spreadsheet onto the image surface
    image.blit(sheet, (0,0), rect)
    return image


# read a row of sprites from the sheet
def read_sprite_row(actionname, xstart, ystart, spritewidth, spriteheight, ncols, nrows, spritesdict):
    # initialise dictionary ref
    spritesdict[actionname] = []
    x = xstart
    y = ystart
    for row in range(nrows):
        for col in range(ncols):
            # read sprite and load into dict
            spritesdict[actionname].append(read_sprite(x, y, spritewidth, spriteheight, SPRITESHEET))
            # move across to next sprite
            x += spritewidth
            # if at end of row, move down to start of next row
            if col == ncols - 1:
                x = xstart
                y += spriteheight


# Load the sprites into sprites dictionary
SPRITES = {}  # initialise
read_sprite_row('Walker', 15, 0, 16, 10, 8, 1, SPRITES)
read_sprite_row('Faller', 11, 20, 16, 10, 4, 1, SPRITES)
#...
read_sprite_row('Shrugger', 17, 224, 16, 10, 8, 1, SPRITES)