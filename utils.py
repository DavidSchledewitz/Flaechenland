"""
Utility functions: highscores, room building, bullet clearing.
"""

import json
import os
from datetime import datetime
import pygame
from entities import Wand, Schluessel, Gegner, Raum
from room_data import ROOMS
from config import HIGHSCORES_FILE, MAX_HIGHSCORES, FRAME_RATE

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


def add_highscore(username, score, frame_count):
    """Add a new score to the highscore list and return top N."""
    highscores = load_highscores()
    
    new_entry = {
        "username": username,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time": frames_to_time_string(frame_count)
    }
    highscores.append(new_entry)
    
    highscores.sort(key=lambda x: x["score"], reverse=True)
    highscores = highscores[:MAX_HIGHSCORES]
    
    save_highscores(highscores)
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
def build_room_groups(walls, keys, enemies, wall_group, key_group, enemy_group):
    """Create sprite groups for a room from data lists."""
    for wall in walls:
        Wand(*wall[:4], wall_group)
    
    for key in keys:
        Schluessel(*key, key_group)
    
    for enemy in enemies:
        Gegner(*enemy, enemy_group)

def create_rooms_from_data():
    """Create room instances from imported room data."""
    room_instances = []
    for room_data in ROOMS:
        room = Raum()
        # Use build_room_groups to populate room groups
        build_room_groups(
            room_data["walls"], room_data["keys"], room_data["enemies"],
            room.wall_list, room.key_list, room.enemy_sprites
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
