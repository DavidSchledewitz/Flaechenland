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
- more to come

### Known Issues/Ideas (fix if you like)

#### Issues
- Exit handling during the game (window closes now, but process doesnt stop? Good enough for now)
- Display size is static
- Starting game, selecting gamemode and in parallel pressing awsd, means auto movement into the opposite direction, should be a quick fix
- Gamemodes still a bit buggy (i.e. phasing through walls), please help finding and fixing
   - Especially Chaos mode (even though really funny), might have some issues
- Difficulty Selection Screen TODO: not hardcoded anymore
- Instant death in boss rooooms. Rather push back or invisibility (and blocked shooting) for a second or so

#### Ideas
- GAMEMODES: easy, hard, impossible. I.e. with speed variation of the oponents, or tracking oponents?
   - **PARTIALLY DONE, impossible needs to be crazier**, touch wall: dead/ Lava filling rooms, variable walls, enemy sizes
- Moving walls: important is the edge case handling. Being squished between walls, leads to lost life
- MORE ROOOOMS, rooms behind rooms, checkpoints, etc
   - labyrinth level with keys that open up walls, so you need strategy
- If a enemy is killed, theres a chance to drop items? speed boost, fire power, lives, invisibility for 5 sec?
- Different enemy classes (green sniper enemies?, heat seakers)
- different keys? effects? doors to unlock? (colors)
- New action buttons (hook, different weapons, chnging with number keys, JUMPING/short invisibility with right tool)
   - action button to take key (changing color of player, to transit walls of the respective color)
- Alle keys? man spawned in BOSS LEVEL, ist super gross (wir dn grosser und schneller, je weniger leben er noch hat), mehr leben als normale gegner
   - vorraum mit gegnern die man ausschalten muss, lava die den raum von einer seite fuellt
- skins for yourself (character, possibly with different starting wepon later?), also skins for opponents, walls etc

# Enjoy playing Flaechenland!
