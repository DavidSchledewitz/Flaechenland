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

#Fonts
FONT_FAMILY = "Calibri"

### UI Text positions and sizes
#button texts
GAME_OVER_TEXT_POS = (82, 150)
PLAY_AGAIN_TEXT_POS = (330, 500)#game over screen
VICTORY_REPLAY_TEXT_POS = (BUTTON_WIN_REPLAY[0]+20, BUTTON_WIN_REPLAY[1]+80)
QUIT_TEXT_POS = (80, 575)
#title texts
VICTORY_TITLE_POS = (60, -40)
#Score of current run
SCORE_BLOCK_X = 60
SCORE_BLOCK_Y = 550
SCORE_LINE_SPACING = 45
#highscore list spacing and position
HIGHSCORES_TITLE_POS = (60, 200)
HIGHSCORES_LIST_Y_START = 235
HIGHSCORES_LINE_SPACING = 30

#Font sizes
FONT_GAME_OVER_SIZE = (FONT_FAMILY, 200, True, False) #(font, size, bold, italic)
FONT_PLAY_AGAIN_SIZE = (FONT_FAMILY, 100, True, False)
FONT_QUIT_SIZE = (FONT_FAMILY, 60, True, False)
FONT_VICTORY_TITLE_SIZE = (FONT_FAMILY, 220, True, False)
FONT_VICTORY_REPLAY_SIZE = (FONT_FAMILY, 90, True, False)
FONT_SCORE_SIZE = (FONT_FAMILY, 50, True, True)
FONT_HIGHSCORES_SIZE = (FONT_FAMILY, 25, False, False)
FONT_HUD_SIZE = (FONT_FAMILY, 25, True, False)
#Name input fonts and text positions
NAME_ENTER_SCREEN_POS = (200, 300)
NAME_INPUT_POS = (200, 400)
FONT_NAME_ENTER_SCREEN_SIZE = (FONT_FAMILY, 60, True, False)
FONT_NAME_INPUT_SIZE = (FONT_FAMILY, 40, False, False)


# Doors (using rectangles for collision detection)
START_DOOR_TOP = pygame.Rect(550, 0, 51, 21)
START_DOOR_BOTTOM = pygame.Rect(550, 629, 51, 71)
START_DOOR_LEFT = pygame.Rect(0, 300, 21, 51)
START_DOOR_RIGHT = pygame.Rect(1129, 300, 71, 51)


# Door transitions: (door_rect, from_room, to_room, spawn_coords)
DOOR_TRANSITIONS = [
	(START_DOOR_TOP, 0, 4, [575, 615]),
	(START_DOOR_BOTTOM, 0, 3, [575, 35]),
	(START_DOOR_LEFT, 0, 1, [1115, 325]),
	(START_DOOR_RIGHT, 0, 2, [35, 325]),
	(START_DOOR_RIGHT, 1, 0, [35, 325]),
	(START_DOOR_LEFT, 2, 0, [1115, 325]),
	(START_DOOR_BOTTOM, 4, 0, [575, 35]),
	(START_DOOR_TOP, 3, 0, [575, 615])
]



#ROOM 0 creation data
# Starting room overlay coordinates (labels, arrows, keys, instructions)
ROOM0_LABELS = [
	("1", (1155, 340)),  # Right door
	("2", (595, 35)),    # Top door
	("3", (30, 340)),    # Left door
	("4", (595, 645))    # Bottom door
]

ROOM0_ARROWS = [
	{"rect": (635, 347, 20, 6), "polygon": ((655, 342), (655, 358), (667, 350))},  # Right arrow
	{"rect": (545, 347, 20, 6), "polygon": ((545, 342), (545, 358), (533, 350))},  # Left arrow
	{"rect": (597, 295, 6, 20), "polygon": ((592, 295), (608, 295), (600, 283))},  # Up arrow
	{"rect": (597, 385, 6, 20), "polygon": ((592, 405), (608, 405), (600, 417))}   # Down arrow
]

ROOM0_KEY_LABELS = [
	("W", (590, 260)),
	("S", (595, 420)),
	("D", (671, 339)),
	("A", (516, 339))
]

ROOM0_SHOOT_TEXT_POS = (35, 650)
ROOM0_KEYS_TEXT_POS = (55, 155)

# Highscores
HIGHSCORES_FILE = "highscores.json"
MAX_HIGHSCORES = 10
