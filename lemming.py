import pygame
from config import WINDOWHEIGHT, WINDOWWIDTH
from init import windowSurface, sprite_size, SPRITES, DELTAS

# Define Lemming class
class Lemming():
    def __init__(self, xpos, ypos, scale=2, reversed=False, inverted=False, rotated=False, action='Faller', permanentskills=[]):
        # Skill action - by convention, lemmings start as Fallers but advance one frame (and state) before drawn
        self.action = action
        self.numframes = len(SPRITES[self.action])  # length of animation loop for current action
        # Place in the animation loop. Animations start from 0 but lemmings advance one frame before first drawn.
        self.frame = -1

        # Permanent skills, counters
        self.permanentskills = permanentskills
        self.cumfalldist = 0  # fall distance tracker
        self.assignable = True
        self.removed = False

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

        # skip if already removed
        if self.removed: return None

        # Do removal from level when ending death or exiting animation, or leaving level boundary
        if self.remove(): return None

        # Do change of action resulting from skill assignment

        # Do automatic change of action when ending an animation that doesn't loop (eg. shrugger -> walker)
        if self.auto_change_action(): pass

        # If not changing action, advance one frame within same action
        else:
            self.frame = (self.frame + 1) % self.numframes

        # update sprite
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


    # change action
    def change_action(self, new_action):
        self.action = new_action
        self.numframes = len(SPRITES[self.action])  # length of animation loop for current action
        self.frame = 0

    def auto_change_action(self):
        # Faller -> Floater start (opening umbrella)
        if self.action == 'Faller' and 'Floater' in self.permanentskills and self.cumfalldist >= 24:
            self.change_action('FloaterStart')

        # Floater start -> Floater
        elif self.action == 'FloaterStart' and self.frame == len(DELTAS['FloaterStart']) - 1:
            self.change_action('Floater')

        # Ohnoer -> Exploder
        elif self.action == 'Ohnoer' and self.frame == len(DELTAS['Ohnoer']) - 1:
            self.change_action('Exploder')

        # Hoister -> Walker
        elif self.action == 'Hoister' and self.frame == len(DELTAS['Hoister']) - 1:
            self.change_action('Walker')
            self.char.left -= self.scale
            self.char.top += 2*self.scale

        # Shrugger -> Walker
        elif self.action == 'Shrugger' and self.frame == len(DELTAS['Shrugger']) - 1:
            self.change_action('Walker')

        # Return True if action changed, otherwise return False
        else: return False
        return True

    def remove(self):
        if self.action in ['Exiter', 'Splatter', 'Drowner', 'Burner', 'Exploder'] and self.frame == len(DELTAS[self.action]) - 1:
            self.removed = True

        else: return False
        return True

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
        if not self.removed: windowSurface.blit(self.sprite, self.char)



