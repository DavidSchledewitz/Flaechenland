"""
Room design data for Flächenland.
Defines walls, keys, and enemies for each room.

Wall format: [x, y, width, height, color (optional)]
Moving wall format: {'moving': True, 'x': ..., 'y': ..., 'width': ..., 'height': ..., 'speed_x': ..., 'speed_y': ..., 'left': ..., 'right': ..., 'top': ..., 'bottom': ...}
Polygon obstacle format: {'type': 'polygon', 'x': ..., 'y': ..., 'width': ..., 'height': ..., 'speed_x': ..., 'speed_y': ..., 'left': ..., 'right': ..., 'top': ..., 'bottom': ..., 'shape': 'diamond'|'triangle'|'pentagon', 'color': (r,g,b), 'points': [(x,y), ...]}
Key format: (x, y)
Enemy format: [x, y, speed_x, speed_y, left, right, top, bottom]
"""

# Anfangsraum (Starting room)
ANFANGSRAUM = {
    "walls": [
        [0, 0, 550, 20],
        [650, 0, 550, 20],
        [0, 680, 550, 20],
        [650, 680, 550, 20],
        [0, 400, 20, 280],
        [0, 20, 20, 280],
        [1180, 20, 20, 280],
        [1180, 400, 20, 280],
        [-20, 300, 20, 100],  # invisible boundary
        [1201, 300, 20, 100],
        [550, -20, 100, 20],
        [550, 701, 100, 20],
        {"moving": True, "x": 150, "y": 300, "width": 100, "height": 20, 
         "speed_x": 2, "speed_y": 0, "left": 20, "right": 1180, "top": 20, "bottom": 680},
        # Diamond obstacles for tighter navigation
        {"type": "polygon", "x": 520, "y": 250, "width": 60, "height": 60,
         "speed_x": 2, "speed_y": 1, "left": 300, "right": 900, "top": 200, "bottom": 460},
    ],
    "keys": [(150, 200)],
    "enemies": [],
}

# Raumlinks (Left room)
RAUMLINKS = {
    "walls": [
        [0, 0, 1200, 20],
        [0, 680, 1200, 20],
        [0, 20, 20, 680],
        [1180, 20, 20, 280],
        [1180, 400, 20, 480],
        [160, 20, 20, 480],
        [500, 270, 20, 430],
        [520, 270, 150, 20],
        [790, 20, 20, 480],
        [1201, 300, 20, 100],
    ],
    "keys": [(70, 335)],
    "enemies": [
        [65, 30, 0, 2, 20, 1180, 20, 500],
        [710, 270, 0, -1, 20, 1180, 270, 680],
        [195, 40, 0, -1, 20, 1180, 40, 660],
        [275, 195, 0, -1, 20, 1180, 40, 660],
        [355, 350, 0, -1, 20, 1180, 40, 660],
        [435, 505, 0, -1, 20, 1180, 40, 660],
    ],
}

# Raumrechts (Right room)
RAUMRECHTS = {
    "walls": [
        [0, 0, 1200, 20],
        [0, 680, 1200, 20],
        [1180, 20, 20, 680],
        [0, 20, 20, 280],
        [0, 400, 20, 280],
        [800, 410, 20, 280],
        [800, 20, 20, 270],
        [-20, 300, 20, 100],
    ],
    "keys": [(1125, 335)],
    "enemies": [
        [200, 200, 1, -2, 20, 800, 20, 680],
        [200, 450, 1, 2, 20, 800, 20, 680],
        [920, 325, 0, 1, 20, 1180, 50, 650],
    ],
}

# Raumunten (Bottom room)
RAUMUNTEN = {
    "walls": [
        [0, 680, 1200, 20],
        [0, 20, 20, 680],
        [1180, 20, 20, 680],
        [0, 0, 550, 20],
        [650, 0, 550, 20],
        [250, 20, 20, 195],
        [360, 20, 20, 195],
        [250, 350, 20, 185],
        [360, 350, 20, 185],
        [270, 515, 90, 20],
        [380, 350, 440, 20],
        [930, 20, 20, 195],
        [820, 20, 20, 195],
        [820, 350, 20, 195],
        [930, 350, 20, 195],
        [840, 525, 90, 20],
        [550, -20, 100, 20],
    ],
    "keys": [(580, 440)],
    "enemies": [
        [290, 30, 0, -1, 20, 1180, 30, 505],
        [860, 30, 0, -1, 20, 1180, 30, 505],
        [380, 505, -1, 1, 380, 820, 370, 680],
        [770, 505, 1, -1, 380, 820, 370, 680],
    ],
}

# Raumoben (Top room)
RAUMOBEN = {
    "walls": [
        [0, 0, 1200, 20],
        [0, 20, 20, 660],
        [1180, 20, 20, 660],
        [0, 680, 550, 20],
        [650, 680, 550, 20],
        [220, 320, 760, 20],
        [590, 340, 20, 100],
        [500, 20, 20, 150],
        [680, 20, 20, 150],
        [550, 701, 100, 20],
    ],
    "keys": [(580, 35)],
    "enemies": [
        [640, 360, 1, 0, 630, 1160, 20, 680],
        [510, 360, -1, 0, 40, 570, 20, 680],
        [20, 135, -1, 1, 20, 500, 20, 320],
        [450, 135, 1, -1, 20, 500, 20, 320],
        [700, 135, -1, 1, 700, 1180, 20, 320],
        [1130, 135, 1, -1, 700, 1180, 20, 320],
    ],
}

# Ordered list of rooms (matches room order: 0=start, 1=left, 2=right, 3=bottom, 4=top)
ROOMS = [ANFANGSRAUM, RAUMLINKS, RAUMRECHTS, RAUMUNTEN, RAUMOBEN]

# Pre-boss antechamber: some enemies, no keys, with rising lava effect
VORRAUM_BOSS = {
    "walls": [
        [0, 0, 1200, 20],
        [0, 680, 1200, 20],
        [0, 20, 20, 680],
        [1180, 20, 20, 680],
        [300, 200, 600, 20],
        [300, 460, 600, 20],
        # Dark magma rising from bottom
        {"moving": True, "x": 20, "y": 750, "width": 1160, "height": 700,
         "speed_x": 0, "speed_y": -0.3, "left": 0, "right": 1200, "top": -100, "bottom": 1380,
         "color": (100, 50, 10), "hazard": True},
    ],
    "keys": [],
    "enemies": [
        [200, 120, 1, 1, 20, 1180, 20, 680],
        [1000, 560, -1, -1, 20, 1180, 20, 680],
        [500, 350, 0, 1, 20, 1180, 20, 680],
    ],
}

# Boss room: single boss pursues player with moving walls
BOSS_RAUM = {
    "walls": [
        [0, 0, 1200, 20],
        [0, 680, 1200, 20],
        [0, 20, 20, 680],
        [1180, 20, 20, 680],
        # Moving walls for additional challenge
        {"moving": True, "x": 400, "y": 100, "width": 20, "height": 150, 
         "speed_x": 0, "speed_y": 3, "left": 20, "right": 1180, "top": 20, "bottom": 680},
        {"moving": True, "x": 780, "y": 450, "width": 20, "height": 150, 
         "speed_x": 0, "speed_y": -3, "left": 20, "right": 1180, "top": 20, "bottom": 680},
        {"moving": True, "x": 500, "y": 320, "width": 200, "height": 20, 
         "speed_x": 2, "speed_y": 0, "left": 20, "right": 1180, "top": 20, "bottom": 680},
        # Moving diamonds that cross the arena
        {"type": "polygon", "x": 300, "y": 240, "width": 70, "height": 70,
         "speed_x": 3, "speed_y": 2, "left": 40, "right": 1100, "top": 60, "bottom": 640},
        {"type": "polygon", "x": 820, "y": 360, "width": 70, "height": 70,
         "speed_x": -3, "speed_y": -2, "left": 40, "right": 1100, "top": 60, "bottom": 640},
    ],
    "keys": [],
    "enemies": [
        {"type": "boss", "x": 600, "y": 350, "left": 20, "right": 1180, "top": 20, "bottom": 680},
    ],
}

# Append new rooms at the end
ROOMS.extend([VORRAUM_BOSS, BOSS_RAUM])
