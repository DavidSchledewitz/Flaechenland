"""
Game entity classes: Player, Gegner (Enemy), Bullet, Schluessel (Key), Wand (Wall).
"""

import pygame
import math
import random
try:
    from config import BLUE, PLAYER_SIZE, ENEMY_SIZE, ENEMY_HEALTH, ENEMY_SPEED_STANDARD, RANDOM_CHANGE_SCALE, RANDOM_MAX_CHANGE, BOSS_SIZE, BOSS_HEALTH, BOSS_PURSUE_SPEED_MULT, BOSS_SPEED_SCALE_MAX, BOSS_BULLET_SPEED, BOSS_BULLET_COOLDOWN_BASE, BOSS_BULLET_COOLDOWN_MIN, BULLET_SIZE
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
        self.mask = pygame.mask.from_surface(self.image)


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
        """Move with collision detection and handle moving wall pushes.
        Returns True if player was squished between walls.
        """
        squished = False
        
        # First, check if any moving walls are pushing us (even when standing still)
        for wall in walls:
            if hasattr(wall, 'change_x') or hasattr(wall, 'change_y'):
                # Use mask collisions to avoid phantom pushes with polygonal walls
                if self.rect.colliderect(wall.rect) and pygame.sprite.collide_mask(self, wall):
                    # Moving wall is overlapping - step along wall motion until separated
                    dx = 0
                    dy = 0
                    if getattr(wall, 'change_x', 0) > 0:
                        dx = 1
                    elif getattr(wall, 'change_x', 0) < 0:
                        dx = -1
                    if getattr(wall, 'change_y', 0) > 0:
                        dy = 1
                    elif getattr(wall, 'change_y', 0) < 0:
                        dy = -1

                    max_steps = max(abs(getattr(wall, 'change_x', 0)), abs(getattr(wall, 'change_y', 0)), 1) + 2
                    pushed = False
                    for _ in range(int(max_steps)):
                        if dx:
                            self.rect.x += dx
                        if dy:
                            self.rect.y += dy
                        pushed = True
                        if not (self.rect.colliderect(wall.rect) and pygame.sprite.collide_mask(self, wall)):
                            break

                    # After pushing, check if player is now colliding with another wall (squished)
                    if pushed:
                        for other_wall in walls:
                            if other_wall != wall and self.rect.colliderect(other_wall.rect) and pygame.sprite.collide_mask(self, other_wall):
                                squished = True
                                break
        
        # Horizontal
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False, collided=pygame.sprite.collide_mask)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Vertical
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False, collided=pygame.sprite.collide_mask)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
        
        return squished


class Gegner(Block):
    """Moving enemy with boundaries.

    Backwards-compatible constructor; `enemy_group` is optional.
    """
    
    def __init__(self, x, y, speed_x, speed_y, left, right, top, bottom, enemy_group=None, game_mode=None, wall_group=None, player=None):
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
        self.pursuit_counter = 0
        self.player = player
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
        # Pursuit movement: periodically re-orient towards player
        if self.game_mode and getattr(self.game_mode, 'pursuit_enemy_movement', False) and self.player is not None:
            self.pursuit_counter += 1
            if self.pursuit_counter >= getattr(self.game_mode, 'pursuit_interval', 120):
                self.pursuit_counter = 0
                # Vector towards player center
                ex, ey = self.rect.centerx, self.rect.centery
                px, py = self.player.rect.centerx, self.player.rect.centery
                dx = px - ex
                dy = py - ey
                dist = math.hypot(dx, dy)
                if dist > 0:
                    base_speed = ENEMY_SPEED_STANDARD * (self.game_mode.enemy_speed_mult if self.game_mode else 1.0)
                    pursuit_mult = getattr(self.game_mode, 'pursuit_speed_mult', 1.0)
                    speed = base_speed * pursuit_mult
                    self.change_x = (dx / dist) * speed
                    self.change_y = (dy / dist) * speed
        
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
        if self.game_mode and (self.game_mode.random_enemy_movement or getattr(self.game_mode, 'pursuit_enemy_movement', False)) and self.wall_group is not None:
            # Walls-aware movement for chaos mode: per-axis move and clamp to wall surfaces
            dx = self.change_x
            dy = self.change_y
            # Horizontal move
            self.rect.x += dx
            collisions = pygame.sprite.spritecollide(self, self.wall_group, False, collided=pygame.sprite.collide_mask)
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
            collisions = pygame.sprite.spritecollide(self, self.wall_group, False, collided=pygame.sprite.collide_mask)
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

class Boss(Block):
    """Boss enemy that pursues the player, speeds up, and shoots more often as it loses health."""
    def __init__(self, x, y, left, right, top, bottom, enemy_group=None, wall_group=None, player=None, game_mode=None, bullet_group=None):
        super().__init__((255, 50, 50), BOSS_SIZE, BOSS_SIZE)
        self.rect.x = x
        self.rect.y = y
        self.max_health = BOSS_HEALTH
        self.gesundheit = BOSS_HEALTH
        self.left_boundary = left
        self.right_boundary = right
        self.top_boundary = top
        self.bottom_boundary = bottom
        self.wall_group = wall_group
        self.player = player
        self.game_mode = game_mode
        self.bullet_group = bullet_group
        base_speed = ENEMY_SPEED_STANDARD * (game_mode.enemy_speed_mult if game_mode else 1.0)
        self.base_speed = base_speed * BOSS_PURSUE_SPEED_MULT
        self.change_x = 0
        self.change_y = 0
        self.shoot_timer = 0
        if enemy_group is not None:
            enemy_group.add(self)

    def update(self):
        # Pursue player
        if self.player is not None:
            ex, ey = self.rect.centerx, self.rect.centery
            px, py = self.player.rect.centerx, self.player.rect.centery
            dx = px - ex
            dy = py - ey
            dist = math.hypot(dx, dy)
            if dist > 0:
                # Speed scales with missing health
                missing_ratio = (self.max_health - self.gesundheit) / max(1, self.max_health)
                speed = self.base_speed * (1.0 + missing_ratio * (BOSS_SPEED_SCALE_MAX - 1.0))
                self.change_x = (dx / dist) * speed
                self.change_y = (dy / dist) * speed

        # Clamp speed
        max_speed = RANDOM_MAX_CHANGE * ENEMY_SPEED_STANDARD * (self.game_mode.enemy_speed_mult if self.game_mode else 1.0) * BOSS_PURSUE_SPEED_MULT
        if self.change_x > max_speed:
            self.change_x = max_speed
        elif self.change_x < -max_speed:
            self.change_x = -max_speed
        if self.change_y > max_speed:
            self.change_y = max_speed
        elif self.change_y < -max_speed:
            self.change_y = -max_speed

        # Walls-aware movement similar to chaos
        dx = self.change_x
        dy = self.change_y
        self.rect.x += dx
        collisions = pygame.sprite.spritecollide(self, self.wall_group, False, collided=pygame.sprite.collide_mask) if self.wall_group is not None else []
        if collisions:
            if dx > 0:
                nearest_left = min(w.rect.left for w in collisions)
                self.rect.right = nearest_left
            else:
                nearest_right = max(w.rect.right for w in collisions)
                self.rect.left = nearest_right
        # Vertical
        self.rect.y += dy
        collisions = pygame.sprite.spritecollide(self, self.wall_group, False, collided=pygame.sprite.collide_mask) if self.wall_group is not None else []
        if collisions:
            if dy > 0:
                nearest_top = min(w.rect.top for w in collisions)
                self.rect.bottom = nearest_top
            else:
                nearest_bottom = max(w.rect.bottom for w in collisions)
                self.rect.top = nearest_bottom

        # Boundary clamp
        if self.rect.right > self.right_boundary:
            self.rect.right = self.right_boundary
        elif self.rect.left < self.left_boundary:
            self.rect.left = self.left_boundary
        if self.rect.bottom > self.bottom_boundary:
            self.rect.bottom = self.bottom_boundary
        elif self.rect.top < self.top_boundary:
            self.rect.top = self.top_boundary

        # Shooting: fire towards player, faster as health drops
        if self.player is not None and self.bullet_group is not None:
            self.shoot_timer += 1
            missing_ratio = (self.max_health - self.gesundheit) / max(1, self.max_health)
            cooldown = BOSS_BULLET_COOLDOWN_BASE - missing_ratio * (BOSS_BULLET_COOLDOWN_BASE - BOSS_BULLET_COOLDOWN_MIN)
            cooldown = max(BOSS_BULLET_COOLDOWN_MIN, int(cooldown))
            if self.shoot_timer >= cooldown:
                self.shoot_timer = 0
                BossBullet(self.rect.centerx, self.rect.centery, self.player.rect.centerx, self.player.rect.centery, self.bullet_group)


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


class BossBullet(pygame.sprite.Sprite):
    """Boss projectile aimed at the player."""

    def __init__(self, x, y, target_x, target_y, bullet_group):
        super().__init__()
        size = max(4, BULLET_SIZE)  # reuse size baseline
        self.image = pygame.Surface([size, size])
        self.image.fill((255, 120, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.change_x = (dx / dist) * BOSS_BULLET_SPEED
        self.change_y = (dy / dist) * BOSS_BULLET_SPEED
        bullet_group.add(self)

    def update(self):
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
        self.mask = pygame.mask.from_surface(self.image)
        if wall_list is not None:
            wall_list.add(self)


class MovingWall(pygame.sprite.Sprite):
    """Moving wall obstacle that bounces within boundaries."""
    
    def __init__(self, x, y, width, height, speed_x, speed_y, left, right, top, bottom, wall_list=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((200, 200, 200))  # Light gray
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = speed_x
        self.change_y = speed_y
        self.left_boundary = left
        self.right_boundary = right
        self.top_boundary = top
        self.bottom_boundary = bottom
        self.mask = pygame.mask.from_surface(self.image)
        if wall_list is not None:
            wall_list.add(self)
    
    def update(self):
        """Move wall and bounce off boundaries."""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # Bounce off boundaries
        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
            # Clamp to boundary
            if self.rect.right > self.right_boundary:
                self.rect.right = self.right_boundary
            if self.rect.left < self.left_boundary:
                self.rect.left = self.left_boundary
        
        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1
            # Clamp to boundary
            if self.rect.bottom > self.bottom_boundary:
                self.rect.bottom = self.bottom_boundary
            if self.rect.top < self.top_boundary:
                self.rect.top = self.top_boundary


class PolygonObstacle(pygame.sprite.Sprite):
    """Polygonal obstacle (diamond/triangle/pentagon/custom) with precise mask collisions."""
    def __init__(self, x, y, width, height, speed_x, speed_y, left, right, top, bottom,
                 color=(250, 200, 55), shape="diamond", points=None, wall_list=None):
        super().__init__()
        # Use SRCALPHA to allow transparent areas around the polygon shape
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        vertices = self._build_points(shape, width, height, points)
        pygame.draw.polygon(self.image, color, vertices)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = speed_x
        self.change_y = speed_y
        self.left_boundary = left
        self.right_boundary = right
        self.top_boundary = top
        self.bottom_boundary = bottom
        self.mask = pygame.mask.from_surface(self.image)
        if wall_list is not None:
            wall_list.add(self)

    def _build_points(self, shape, width, height, points_override):
        """Return polygon vertices based on requested shape or explicit points."""
        if points_override:
            return points_override

        cx, cy = width / 2.0, height / 2.0
        if shape == "diamond":
            return [(cx, 0), (width - 1, cy), (cx, height - 1), (0, cy)]
        if shape == "triangle":
            return [(cx, 0), (width - 1, height - 1), (0, height - 1)]
        if shape == "triangle_down":
            return [(0, 0), (width - 1, 0), (cx, height - 1)]
        if shape == "circle":
            # Approximate circle with a polygon
            num_points = 20
            return [
                (cx + (width / 2 - 1) * math.cos(2 * math.pi * i / num_points),
                 cy + (height / 2 - 1) * math.sin(2 * math.pi * i / num_points))
                for i in range(num_points)
            ]
        if shape == "pentagon":
            # Regular pentagon inscribed in the rectangle, oriented with a flat base
            import math
            radius = min(width, height) / 2.1
            angle_offset = -math.pi / 2  # point up
            return [
                (cx + radius * math.cos(angle_offset + i * 2 * math.pi / 5),
                 cy + radius * math.sin(angle_offset + i * 2 * math.pi / 5))
                for i in range(5)
            ]
        # Fallback to diamond
        return [(cx, 0), (width - 1, cy), (cx, height - 1), (0, cy)]

    def update(self):
        """Move polygon and bounce within boundaries."""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
            if self.rect.right > self.right_boundary:
                self.rect.right = self.right_boundary
            if self.rect.left < self.left_boundary:
                self.rect.left = self.left_boundary

        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1
            if self.rect.bottom > self.bottom_boundary:
                self.rect.bottom = self.bottom_boundary
            if self.rect.top < self.top_boundary:
                self.rect.top = self.top_boundary


class Raum(object):
    """Container class for per-room sprite groups."""
    wall_list = None
    enemy_sprites = None
    key_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
