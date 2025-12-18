# Flaechenland
This is a game created for a school programming project, with a lot of passion, creativity, and... hardcoding. As simple as it is, it is fun to play! Created by Marius Menzel, Milena Czierlinski, Lasse Schmidt and David Schledewitz.

## How to Start the Game

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Installation & Running (Linux)

1. Clone or download this repository, i.e.
   ```bash
   git clone https://github.com/DavidSchledewitz/Flaechenland.git
   ```
2. Navigate to the game directory:
   ```bash
   cd Flaechenland
   ```
3. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
4. Run the game:
   ```bash
   python3 Flaechenland.py
   ```

### Game Controls
- **W, A, S, D** - Move your character
- **Arrow Keys** - Shoot in the corresponding direction
- Collect all keys to win!
- Avoid enemies or shoot them down

### Known Issues/Ideas (fix if you like)

#### Issues
- Exit handling during the game (window closes now, but process doesnt stop? Good enough for now)
- Display size is static

#### Ideas
- A LOT of hardcoding in the classes. Would be nice to have a collected property class for like cooldown movement speed, enemy lifes and so on, to easily adjust properties
- MORE ROOOOMS, rooms behind rooms, checkpoints, ets
- If a enemy is killed, theres a chance to drop items? speed boost, fire power, lives?
- Different enemy classes (green sniper enemies?)
- Add split seconds for speedrun enthusiasts?

# Enjoy playing Flaechenland!
