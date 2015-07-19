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
    def __init__(self, xpos, ypos, scale=2, reversed=False, inverted=False, rotated=False, permanentskills=[]):
        # Skill action - by convention, lemmings start as Fallers but advance one frame (and state) before drawn
        self.action = 'Faller'
        self.numframes = len(SPRITES[self.action])  # length of animation loop for current action
        self.frame = 0  # place in the animation loop

        # Permanent skills, counters
        self.permanentskills = permanentskills
        self.cumfalldist = 0  # fall distance tracker

        # ORIENTATION
        # Convention to represent orientation with three flags:
        # - REVERSED = False if facing right or down, True if facing left or up
        # - INVERTED = False if on floor or left wall, True if on ceiling or right wall
        # - ROTATED = False if on floor or ceiling, True if on left or right wall
        #             (i.e. swap dx and dy, given that y increases down the screen)
        # Notes:
        # - Turning at wall, Reverser skill and Blocker effect toggle "reversed"
        # - Inverter toggles "inverted" (and adjusts position)
        # - Facing direction: right=F*F, left=T*F, up=T*T, down = F*T (* = any: inverted status doesn't matter)
        # - Upturner cycle facing right: FFF -> TTT -> TTF -> FFT
        # - Upturner cycle facing left:  TFF -> TFT -> FTF -> FTT
        # - Downturner cycles: as above but in reverse order
        self.reversed = reversed
        self.inverted = inverted
        self.rotated = rotated

        # SCALE
        # 1 = small, 2 = normal, 4 = big
        self.scale = scale

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

        # advance animation frame
        # change action if needed
        if self.action == 'Faller' and 'Floater' in self.permanentskills and self.cumfalldist >= 24:
            self.action = 'Floater'
            self.frame=0
        elif self.action == 'Floater' and self.frame == 3:
            self.action = 'Floater2'
            self.frame=0
        # otherwise advance frame within same action
        else:
            self.frame = (self.frame + 1) % self.numframes

        self.sprite = self.getSprite()

        # if faller, increment fall distance
        if self.action == 'Faller': self.cumfalldist += 3
        else: self.cumfalldist = 0

        # Turn around at the edge of the map if facing that edge
        if self.char.centerx >= WINDOWWIDTH  and self.get_facing() == 'R' or \
           self.char.centerx <= 0            and self.get_facing() == 'L' or \
           self.char.centery >= WINDOWHEIGHT and self.get_facing() == 'D' or \
           self.char.centery <= 0            and self.get_facing() == 'U':
            self.reversed = not self.reversed

        # Wrap around at the edge of the map, if facing perpendicular to that edge
        if (self.char.centery < 0 or self.char.centery > WINDOWHEIGHT) and not self.rotated:
            self.char.centery %= WINDOWHEIGHT
        if (self.char.centerx < 0 or self.char.centerx > WINDOWWIDTH) and self.rotated:
            self.char.centerx %= WINDOWWIDTH

        # Determine change in position
        dx, dy = DELTAS[self.action][self.frame]
        # reverse
        if self.reversed: dx *= -1
        # invert
        if self.inverted: dy *= -1
        # rotate
        if self.rotated: dx, dy = -dy, dx

        # scale
        dx = self.scale * dx
        dy = self.scale * dy

        # change position according to computed dx and dy
        self.char.left += dx
        self.char.top += dy

    # get facing direction
    def get_facing(self):
        if self.reversed:
            if self.rotated: return 'U'
            else: return 'L'
        else:
            if self.rotated: return 'D'
            else: return 'R'


    # draw to screen
    def draw(self):
        windowSurface.blit(self.sprite, self.char)



# read from sprite sheet
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
read_sprite_row(SPRITES, 'Floater',  80,  40,  4)
read_sprite_row(SPRITES, 'Floater2', 160,  40,  4)
read_sprite_row(SPRITES, 'Floater2', 220,  40,  4, spritespace=-20)
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
DELTAS['Floater'] = [(0,0), (0,3), (0,0), (0,0)]
DELTAS['Floater2'] = [(0,2)] * len(SPRITES['Floater2'])
for i in list(range(1,5)): DELTAS['Hoister'][i] = (0,-2)
