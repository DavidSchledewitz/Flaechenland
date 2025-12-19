"""
Game configuration: constants, colors, screen settings, buttons, doors, fonts.
"""

import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Player
PLAYER_SIZE = 50
PLAYER_START = (575, 325)
PLAYER_SPEED = 5
PLAYER_HEALTH = 5

# Bullet
BULLET_SIZE = 4
PLAYER_BULLET_SPEED = 12
BULLET_COOLDOWN_FRAMES = 5

# Timing
FRAME_RATE = 60

# UI Buttons - Game Over Screen (outer coordinates, inner = outer offset by +1)
BUTTON_PLAY_AGAIN = (299, 480, 600, 130)  # (x, y, width, height)
BUTTON_QUIT = (50, 560, 200, 80)
BUTTON_WIN_REPLAY = (700, 400, 450, 250)

# Doors (using rectangles for collision detection)
START_DOOR_TOP = pygame.Rect(550, 0, 51, 21)
START_DOOR_BOTTOM = pygame.Rect(550, 629, 51, 71)
START_DOOR_LEFT = pygame.Rect(0, 300, 21, 51)
START_DOOR_RIGHT = pygame.Rect(1129, 300, 71, 51)

# Font
FONT_FAMILY = "Calibri"

# Highscores
HIGHSCORES_FILE = "highscores.json"
MAX_HIGHSCORES = 10
