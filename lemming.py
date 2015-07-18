import pygame
from pygame.locals import *

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
        # Skill action - by convention, lemmings start as Fallers but advance one frame (and state) before drawn
        self.action = 'Walker'
        self.numframes = len(SPRITES[self.action])  # length of animation loop for current action
        self.frame = 0  # place in the animation loop
        self.xspeed = 1  # speed - placeholder - replace with change in position per action per frame
        self.yspeed = 0

        # ORIENTATION
        # Convention to represent orientation with three flags:
        # - REVERSED = False if facing right or down, True if facing left or up
        # - INVERTED = False if on floor or left wall, True if on ceiling or right wall
        # - ROTATED = False if on floor or ceiling, True if on left or right wall
        #             (i.e. swap dx and dy, given that y increases down the screen)
        # Notes:
        # - Turning at wall, Reverser skill and Blocker effect toggle "reversed"
        # - Inverter toggles "inverted" (and adjusts position)
        # - Upturner cycle facing right: FFF -> TTT -> TTF -> FFT
        # - Upturner cycle facing left:  TFF -> TFT -> FTF -> FTT
        # - Downturner cycles: as above but in reverse order
        self.reversed = False
        self.inverted = False
        self.rotated = False

        # SCALE
        # 1 = small, 2 = normal, 4 = big
        self.scale = 4

        # SPRITE
        # Define box to draw sprite on
        self.char = pygame.Rect(xpos, ypos, sprite_size*self.scale, sprite_size*self.scale)
        # Get sprite and draw on box
        self.sprite = self.getSprite()

    # Get Sprite, modified for orientation and size
    def getSprite(self):
        sprite = SPRITES[self.action][self.frame]  # base image
        sprite = pygame.transform.flip(sprite, self.reversed, self.inverted)
        if self.rotated: sprite =  pygame.transform.rotate(sprite, 270)
        sprite = pygame.transform.scale(sprite, (sprite_size*self.scale, sprite_size*self.scale))
        return sprite


    # move by one frame
    def move(self):
        # Determine change in position
        dx = self.xspeed
        dy = self.yspeed
        # reverse
        if self.reversed: dx *= -1
        # invert
        if self.inverted: dy *= -1
        # rotate
        if self.rotated: dx, dy = dy, dx

        # scale
        dx = self.scale * dx
        dy = self.scale * dy

        # change position according to computed dx and dy
        self.char.left += dx
        self.char.top += dy

        # advance animation frame
        self.frame = (self.frame + 1) % self.numframes
        self.sprite = self.getSprite()

        # Wrap around the edge of the map
        # if the lemming goes off the top or bottom of the screen, wrap around
        if self.char.top < 0 or self.char.bottom > WINDOWHEIGHT:
            self.char.top %= WINDOWHEIGHT

        # Turn around at the side of the map
        if self.char.centerx <= 0 or self.char.centerx >= WINDOWWIDTH:
            self.reversed = not(self.reversed)


    # draw to screen
    def draw(self):
        windowSurface.blit(self.sprite, self.char)



# read from sprite sheet
SPRITESHEET = pygame.image.load('sprites_amiga.png').convert()
sprite_size = 16  # pad all sprites to 16x16

# read a single sprite from the sheet
def read_sprite(x, y, width, height, sheet):
    # define a rectangular area on the sheet
    rect = pygame.Rect(x, y, width, height)
    # create a Surface to store the image
    image = pygame.Surface((sprite_size, sprite_size)).convert()
    # copy image from selected are of spreadsheet onto the image surface
    image.blit(sheet, (0,0), rect)
    # set black as transparent
    image.set_colorkey((0, 0, 0))
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