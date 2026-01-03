"""
Utility functions: highscores, room building, bullet clearing.
"""

import json
import os
from datetime import datetime
import pygame
from entities import Wand, MovingWall, PolygonObstacle, Schluessel, Gegner, Boss, Raum
from room_data import ROOMS
from config import HIGHSCORES_FILE, MAX_HIGHSCORES, FRAME_RATE, ENEMY_HEALTH

####################################Highscore related functions
def load_highscores():
    """Load highscores from JSON file."""
    if os.path.exists(HIGHSCORES_FILE):
        try:
            with open(HIGHSCORES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_highscores(highscores):
    """Save highscores to JSON file."""
    with open(HIGHSCORES_FILE, "w") as f:
        json.dump(highscores, f, indent=2)


def add_highscore(username, score, date, frame_count, mode=None):
    """Add a new score to the highscore list and return top N.
    Optionally records the game mode used.
    """
    highscores = load_highscores()
    
    new_entry = {
        "username": username,
        "score": score,
        "date": date,
        "time": frames_to_time_string(frame_count),
        "mode": mode
    }
    highscores.append(new_entry)
    
    highscores.sort(key=lambda x: x["score"], reverse=True)
    save_highscores(highscores)
    # highscores = highscores[:MAX_HIGHSCORES]
    
    return highscores

#time frame calculation
def frames_to_time_string(frame_count):
    """Convert frame count to MM:SS.ms format string"""
    total_seconds = frame_count // FRAME_RATE
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    milliseconds = (round((frame_count % FRAME_RATE) / FRAME_RATE * 100))
    return "{0:02}:{1:02}.{2:02}".format(minutes, seconds, milliseconds)

######################################Room building functions
def build_room_groups(walls, keys, enemies, wall_group, key_group, enemy_group, game_mode=None, player=None, boss_bullet_group=None):
    """Create sprite groups for a room from data lists.
    
    If game_mode is provided, adjust enemy speed and health values.
    Enemy data format: [x, y, speed_x, speed_y, left, right, top, bottom]
    Wall data format: [x, y, width, height] or dict with 'moving'/'type' keys
    """
    for wall in walls:
        if isinstance(wall, dict):
            if wall.get('type') == 'polygon':
                PolygonObstacle(
                    wall['x'], wall['y'], wall['width'], wall['height'],
                    wall.get('speed_x', 0), wall.get('speed_y', 0),
                    wall['left'], wall['right'], wall['top'], wall['bottom'],
                    color=wall.get('color', (250, 200, 55)),#orange
                    shape=wall.get('shape', 'diamond'),
                    points=wall.get('points'),
                    wall_list=wall_group
                )
            elif wall.get('moving'):
                MovingWall(wall['x'], wall['y'], wall['width'], wall['height'],
                          wall['speed_x'], wall['speed_y'],
                          wall['left'], wall['right'], wall['top'], wall['bottom'],
                          wall_group)
            else:
                Wand(wall['x'], wall['y'], wall['width'], wall['height'], wall_group)
        else:
            Wand(*wall[:4], wall_group)
    
    for key in keys:
        Schluessel(*key, key_group)
    
    for enemy_data in enemies:
        if isinstance(enemy_data, dict) and enemy_data.get("type") == "boss":
            enemy = Boss(
                enemy_data["x"], enemy_data["y"],
                enemy_data["left"], enemy_data["right"],
                enemy_data["top"], enemy_data["bottom"],
                enemy_group=enemy_group, wall_group=wall_group, player=player, game_mode=game_mode, bullet_group=boss_bullet_group
            )
            # Boss health is not scaled by game mode - use full BOSS_HEALTH
        else:
            enemy = Gegner(*enemy_data, enemy_group, game_mode, wall_group, player)
            # Apply health multiplier only to regular enemies
            if game_mode is not None:
                enemy.gesundheit = max(1, int(ENEMY_HEALTH * game_mode.enemy_health_mult))
            
def create_rooms_from_data(game_mode=None, player=None, boss_bullet_group=None):
    """Create room instances from imported room data.
    
    If game_mode is provided, enemies will have adjusted speed and health.
    """
    room_instances = []
    for room_data in ROOMS:
        room = Raum()
        # Use build_room_groups to populate room groups
        build_room_groups(
            room_data["walls"], room_data["keys"], room_data["enemies"],
            room.wall_list, room.key_list, room.enemy_sprites, game_mode, player, boss_bullet_group
        )
        room_instances.append(room)
    return room_instances

def clear_bullets(bullet_list):
    """Clear all bullets from list."""
    bullet_list.empty()
#Cleanup function for smooth exit of the game
def cleanup_pygame():
    """Clean exit pygame: clear sprite groups and quit."""
    try:
        pygame.display.quit()
    except Exception:
        pass
    try:
        pygame.quit()
    except Exception:
        pass
