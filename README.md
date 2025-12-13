# Flaechenland
This is a game created for a school programming project, with a lot of passion, creativity, and... hardcoding. As simple as it is, it is fun to play! Created by Marius Menzel, Milena Czierlinski, Lasse Schmidt and David Schledewitz.

## How to Start the Game

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Installation & Running

#### On Linux:

1. Clone or download this repository
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

#### On Windows (probably, not tested):

1. Clone or download this repository
2. Open Command Prompt or PowerShell and navigate to the game directory:
   ```cmd
   cd Flaechenland
   ```
3. Install the required dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Run the game:
   ```cmd
   python Flaechenland.py
   ```

### Game Controls
- **W, A, S, D** - Move your character
- **Arrow Keys** - Shoot in the corresponding direction
- Collect all keys to win!
- Avoid enemies or shoot them down

### Known Issues/Ideas (fix if you like)

#### Issues
- Exit handling during the game
- If the mouse is on top of the play again button in case of game over, the area check instantly starts a new game. Button presses can lead to permanent movement of the player character in one direction. Probable fix is to clarify the conditions for restarting the game
- Display size is static

#### Ideas
- Highscore -> Highscore list with username
- A LOT of hardcoding in the classes. Would be nice to have a collected property class for like cooldown movement speed, enemy lifes and so on, to easily adjust properties
- MORE ROOOOMS, rooms behind rooms, checkpoints, ets
- If a enemy is killed, theres a chance to drop items? speed boost, fire power, lives?
- Different enemy classes (green sniper enemies?)

# Enjoy playing Flaechenland!
