"""
Game entity classes: Player, Gegner (Enemy), Bullet, Schluessel (Key), Wand (Wall).
"""

import pygame
import random
try:
    from config import BLUE, PLAYER_SIZE, ENEMY_SIZE, ENEMY_HEALTH, ENEMY_SPEED_STANDARD, RANDOM_CHANGE_SCALE, RANDOM_MAX_CHANGE
except Exception:
    BLUE = (0, 0, 255)
    PLAYER_SIZE = 50


class Block(pygame.sprite.Sprite):
    """Base class for rectangular sprites."""
    
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Player(Block):
    """Playable character with movement.

    Backwards-compatible constructor:
    - Player(x, y) uses defaults from config
    - Player(x, y, size) custom size
    - Player(x, y, size, all_sprites_list) also adds itself to provided group
    - Player(x, y, all_sprites_list=group) via keyword argument
    """

    def __init__(self, x, y, size=None, all_sprites_list=None):
        if size is None:
            size = PLAYER_SIZE
        super().__init__(BLUE, size, size)
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        if all_sprites_list is not None:
            all_sprites_list.add(self)

    def update(self, x, y):
        """Add velocity."""
        self.change_x += x
        self.change_y += y

    def set(self, x, y):
        """Set position."""
        self.rect.x = x
        self.rect.y = y

    def move(self, walls):
        """Move with collision detection."""
        # Horizontal
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Vertical
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom


class Gegner(Block):
    """Moving enemy with boundaries.

    Backwards-compatible constructor; `enemy_group` is optional.
    """
    
    def __init__(self, x, y, speed_x, speed_y, left, right, top, bottom, enemy_group=None, game_mode=None, wall_group=None):
        super().__init__((255, 0, 0), ENEMY_SIZE, ENEMY_SIZE)  # RED
        self.rect.x = x
        self.rect.y = y
        self.gesundheit = ENEMY_HEALTH
        base_speed = ENEMY_SPEED_STANDARD * (game_mode.enemy_speed_mult if game_mode is not None else 1.0)
        self.change_x = speed_x * base_speed
        self.change_y = speed_y * base_speed
        # Clamp initial speed to max 2x standard (scaled by mode)
        max_speed_init = 2 * ENEMY_SPEED_STANDARD * (game_mode.enemy_speed_mult if game_mode is not None else 1.0)
        if self.change_x > max_speed_init:
            self.change_x = max_speed_init
        elif self.change_x < -max_speed_init:
            self.change_x = -max_speed_init
        if self.change_y > max_speed_init:
            self.change_y = max_speed_init
        elif self.change_y < -max_speed_init:
            self.change_y = -max_speed_init
        self.left_boundary = left
        self.right_boundary = right
        self.top_boundary = top
        self.bottom_boundary = bottom
        self.wall_group = wall_group
        self.game_mode = game_mode
        self.random_counter = 0
        if enemy_group is not None:
            enemy_group.add(self)

    def update(self):
        """Move within boundaries and bounce."""
        # Random movement mode
        if self.game_mode and self.game_mode.random_enemy_movement:
            self.random_counter += 1
            if self.random_counter >= self.game_mode.random_interval:
                self.random_counter = 0
                # Randomly change direction
                if random.random() < 0.5:
                    self.change_x += random.choice([-1, 1]) * ENEMY_SPEED_STANDARD * RANDOM_CHANGE_SCALE * self.game_mode.enemy_speed_mult
                if random.random() < 0.5:
                    self.change_y += random.choice([-1, 1]) * ENEMY_SPEED_STANDARD * RANDOM_CHANGE_SCALE * self.game_mode.enemy_speed_mult
        
        # Clamp speed every frame to avoid runaway velocities (2x standard * mode)
        max_speed = RANDOM_MAX_CHANGE * ENEMY_SPEED_STANDARD * (self.game_mode.enemy_speed_mult if self.game_mode else 1.0)
        if self.change_x > max_speed:
            self.change_x = max_speed
        elif self.change_x < -max_speed:
            self.change_x = -max_speed
        if self.change_y > max_speed:
            self.change_y = max_speed
        elif self.change_y < -max_speed:
            self.change_y = -max_speed
        
        # Movement and collision handling
        if self.game_mode and self.game_mode.random_enemy_movement and self.wall_group is not None:
            # Walls-aware movement for chaos mode: per-axis move and clamp to wall surfaces
            dx = self.change_x
            dy = self.change_y
            # Horizontal move
            self.rect.x += dx
            collisions = pygame.sprite.spritecollide(self, self.wall_group, False)
            if collisions:
                # Clamp to the nearest wall surface depending on movement direction
                if dx > 0:
                    nearest_left = min(w.rect.left for w in collisions)
                    self.rect.right = nearest_left
                else:
                    nearest_right = max(w.rect.right for w in collisions)
                    self.rect.left = nearest_right
                self.change_x *= -1
            # Vertical move
            self.rect.y += dy
            collisions = pygame.sprite.spritecollide(self, self.wall_group, False)
            if collisions:
                if dy > 0:
                    nearest_top = min(w.rect.top for w in collisions)
                    self.rect.bottom = nearest_top
                else:
                    nearest_bottom = max(w.rect.bottom for w in collisions)
                    self.rect.top = nearest_bottom
                self.change_y *= -1
        else:
            # Default: move then clamp within rectangular boundaries
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            # Clamp position to boundaries and bounce if overshooting (axis-specific)
            if self.rect.right > self.right_boundary:
                self.rect.right = self.right_boundary
                self.change_x *= -1
            elif self.rect.left < self.left_boundary:
                self.rect.left = self.left_boundary
                self.change_x *= -1
            if self.rect.bottom > self.bottom_boundary:
                self.rect.bottom = self.bottom_boundary
                self.change_y *= -1
            elif self.rect.top < self.top_boundary:
                self.rect.top = self.top_boundary
                self.change_y *= -1


class Bullet(Block):
    """Projectile with direction."""
    
    def __init__(self, direction, x, y, player_size, bullet_size, bullet_speed, bullet_list):
        super().__init__((255, 255, 255), bullet_size, bullet_size)  # WHITE
        self.rect.x = x
        self.rect.y = y
        center_offset = (player_size - bullet_size) // 2

        if direction == "oben":
            self.rect.x = x + center_offset
            self.change_x = 0
            self.change_y = -bullet_speed
        elif direction == "unten":
            self.rect.x = x + center_offset
            self.rect.y = y + player_size - bullet_size
            self.change_x = 0
            self.change_y = bullet_speed
        elif direction == "links":
            self.rect.y = y + center_offset
            self.change_x = -bullet_speed
            self.change_y = 0
        elif direction == "rechts":
            self.rect.x = x + player_size - bullet_size
            self.rect.y = y + center_offset
            self.change_x = bullet_speed
            self.change_y = 0
        else:
            self.change_x = 0
            self.change_y = 0

        bullet_list.add(self)

    def update(self):
        """Move bullet."""
        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Schluessel(pygame.sprite.Sprite):
    """Key item to collect. Optional group auto-add.

    Backwards-compatible:
    - Schluessel(x, y) (no auto-add)
    - Schluessel(x, y, key_list) auto-adds to provided group
    Uses the same image and scaling as the legacy inline class.
    """
    
    def __init__(self, x, y, key_list=None):
        super().__init__()
        img = pygame.image.load("key-icon.png").convert()
        img = pygame.transform.scale(img, (30, 30))
        img.set_colorkey((255, 255, 255))  # WHITE
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if key_list is not None:
            key_list.add(self)


class Wand(pygame.sprite.Sprite):
    """Wall for collision. Optional group auto-add."""
    
    def __init__(self, x, y, width, height, wall_list=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))  # WHITE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if wall_list is not None:
            wall_list.add(self)


class Raum(object):
    """Container class for per-room sprite groups."""
    wall_list = None
    enemy_sprites = None
    key_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
