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
# Enemy
ENEMY_SIZE = 50
ENEMY_SPEED_STANDARD = 5
ENEMY_HEALTH = 5
# CHAOS
RANDOM_INTERVAL = 10 # frames between direction changes
RANDOM_CHANGE_SCALE = 0.08  # fraction of standard speed to change by
RANDOM_MAX_CHANGE = 2.0  # max speed change factor



# Bullet
BULLET_SIZE = 4
PLAYER_BULLET_SPEED = 12
BULLET_COOLDOWN_FRAMES = 5

# Timing
FRAME_RATE = 60

# Game Over Screen (outer coordinates, inner = outer offset by +1)
BUTTON_PLAY_AGAIN = (299, 480, 600, 130)  # (x, y, width, height)
BUTTON_QUIT = (50, 560, 200, 80)
GAME_OVER_TEXT_POS = (82, 150)
PLAY_AGAIN_TEXT_POS = (330, 500)#game over screen
QUIT_TEXT_POS = (80, 575)

# Difficulty Selection Screen TODO: not hardcoded anymore

#### Winning Screen
BUTTON_WIN_REPLAY = (800, 550, 350, 100)
VICTORY_REPLAY_TEXT_POS = (BUTTON_WIN_REPLAY[0]+20, BUTTON_WIN_REPLAY[1]+15)
VICTORY_TITLE_POS = (60, -40)
    #highscore list spacing and position (Winning screen)
HIGHSCORES_TITLE_POS = (60, 200)
HIGHSCORES_LIST_Y_START = 235
HIGHSCORES_LINE_SPACING = 30
    #Score of current run (Winning screen)
SCORE_BLOCK_X = 60
SCORE_BLOCK_Y = 550
SCORE_LINE_SPACING = 45

#Fonts
FONT_FAMILY = "Calibri"
FONT_MONO = "Courier New"
###Font sizes
# Difficulty selection screen fonts
FONT_SELECT_TITLE_SIZE = (FONT_FAMILY, 120, True, False)
FONT_SELECT_MODE_SIZE = (FONT_FAMILY, 60, True, False)
#Game over
FONT_GAME_OVER_SIZE = (FONT_FAMILY, 200, True, False) #(font, size, bold, italic)
FONT_PLAY_AGAIN_SIZE = (FONT_FAMILY, 100, True, False)
FONT_QUIT_SIZE = (FONT_FAMILY, 60, True, False)
#Winning
FONT_VICTORY_TITLE_SIZE = (FONT_FAMILY, 220, True, False)
FONT_VICTORY_REPLAY_SIZE = (FONT_FAMILY, 67, True, False)
FONT_SCORE_SIZE = (FONT_FAMILY, 50, True, True)
FONT_HIGHSCORES_SIZE = (FONT_FAMILY, 25, False, False)
FONT_HIGHSCORES_MONOSPACE_SIZE = (FONT_MONO, 20, False, False)  # Monospace for aligned highscores
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


# Game Modes and Difficulty Settings
class GameMode:
    """Encapsulates game difficulty and property multipliers."""
    def __init__(self, name, player_speed_mult=1.0, enemy_speed_mult=1.0, 
                 enemy_health_mult=1.0, cooldown_mult=1.0, score_mult=1.0,
                 random_enemy_movement=False, random_interval=60):
        self.name = name
        self.player_speed_mult = player_speed_mult
        self.enemy_speed_mult = enemy_speed_mult
        self.enemy_health_mult = enemy_health_mult
        self.cooldown_mult = cooldown_mult
        self.score_mult = score_mult
        self.random_enemy_movement = random_enemy_movement
        self.random_interval = random_interval  # frames between direction changes 
    
    def get_player_speed(self):
        return max(1, int(PLAYER_SPEED * self.player_speed_mult))
    
    # def get_enemy_speed(self):
    #     return max(1, int(ENEMY_SPEED_STANDARD * self.enemy_speed_mult))
    
    def get_enemy_health(self):
        return max(1, int(ENEMY_HEALTH * self.enemy_health_mult))
    def get_cooldown_frames(self):
        return max(1, int(BULLET_COOLDOWN_FRAMES * self.cooldown_mult))
    
    def get_score_multiplier(self):
        return self.score_mult
    
    def __repr__(self):
        return f"GameMode({self.name})"


# Pre-defined game modes
EASY_MODE = GameMode(
    name="EASY",
    player_speed_mult=1.5,
    enemy_speed_mult=0.7,
    enemy_health_mult=0.6,
    cooldown_mult=0.5,
    score_mult=0.8
)

NORMAL_MODE = GameMode(
    name="NORMAL",
    player_speed_mult=1.0,
    enemy_speed_mult=1.0,
    enemy_health_mult=1.0,
    cooldown_mult=1.0,
    score_mult=1.0
)

HARD_MODE = GameMode(
    name="HARD",
    player_speed_mult=0.8,
    enemy_speed_mult=1.3,
    enemy_health_mult=1.5,
    cooldown_mult=2,
    score_mult=1.2
)

IMPOSSIBLE_MODE = GameMode(
    name="IMPOSSIBLE",
    player_speed_mult=0.7,
    enemy_speed_mult=1.6,
    enemy_health_mult=2.0,
    cooldown_mult=3,
    score_mult=1.5
)

CHAOS_MODE = GameMode(
    name="CHAOS",
    player_speed_mult=1.0,
    enemy_speed_mult=1.0,
    enemy_health_mult=1.0,
    cooldown_mult=1.0,
    score_mult=1.8,
    random_enemy_movement=True,
    random_interval= RANDOM_INTERVAL  # Change direction every x frames
)

# Available game modes
GAME_MODES = {
    "EASY": EASY_MODE,
    "NORMAL": NORMAL_MODE,
    "HARD": HARD_MODE,
    "IMPOSSIBLE": IMPOSSIBLE_MODE,
    "CHAOS": CHAOS_MODE
}

# Default game mode
DEFAULT_MODE = NORMAL_MODE
