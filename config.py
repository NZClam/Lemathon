import pygame
from pygame.locals import *

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

# constants
FPS = 15  # frames per second

# Hotkeys
def get_hotkey_skill(key):
    for skill, hotkey in hotkeys_skills:
        if hotkey == key:
            return skill
    #return ''

hotkeys_skills = []
hotkeys_skills.append(('Walker', K_w))
hotkeys_skills.append(('Climber', K_F3))
hotkeys_skills.append(('Floater', K_F4))
hotkeys_skills.append(('Ohnoer', K_F5))
hotkeys_skills.append(('Blocker', K_F6))
hotkeys_skills.append(('Builder', K_F7))
hotkeys_skills.append(('Basher', K_F8))
hotkeys_skills.append(('Miner', K_F9))
hotkeys_skills.append(('Digger', K_F10))
