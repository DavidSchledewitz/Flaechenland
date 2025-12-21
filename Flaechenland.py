#!/usr/bin/python3

#Flächenland - Ein Softwareprojekt von David, Marius, Milena und Lasse, Q2a 2017
import pygame
import json
import os
from datetime import datetime
# import random
import sys

# Import configuration and utilities
from config import *
from room_data import ROOMS
from entities import Player, Gegner, Wand, Schluessel, Bullet, Raum
from utils import load_highscores, add_highscore, clear_bullets, frames_to_time_string, create_rooms_from_data, cleanup_pygame

# Global sprite groups
bullet_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
key_list = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

def cleanup_quit():
    """Clean sprite groups and pygame."""
    bullet_list.empty()
    all_sprites_list.empty()
    cleanup_pygame()

"""------------------------------------------------------ Game difficulty Window ------------------------------------------------------------"""
def select_difficulty():
    """Display difficulty selection menu and return chosen GameMode."""
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Flächenland - Select Difficulty")
    
    font_title = pygame.font.SysFont(*FONT_SELECT_TITLE_SIZE)
    font_mode = pygame.font.SysFont(*FONT_SELECT_MODE_SIZE)
    
    modes_list = [("1", EASY_MODE), ("2", NORMAL_MODE), ("3", HARD_MODE), ("4", IMPOSSIBLE_MODE), ("5", CHAOS_MODE)]
    selected_idx = 1  # Default: Normal
    
    selecting = True
    clock = pygame.time.Clock()
    
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cleanup_quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_idx = (selected_idx + 1) % len(modes_list)
                elif event.key == pygame.K_UP:
                    selected_idx = (selected_idx - 1) % len(modes_list)
                elif event.key == pygame.K_RETURN:
                    selecting = False
        
        screen.fill(BLACK)
        
        # Title
        title = font_title.render("SELECT DIFFICULTY", True, YELLOW)
        screen.blit(title, (100, 100))
        
        # Mode options
        y_pos = 250
        for idx, (_, mode) in enumerate(modes_list):
            color = YELLOW if idx == selected_idx else GREEN
            text = font_mode.render(f"{idx+1}. {mode.name.upper()}", True, color)
            screen.blit(text, (200, y_pos))
            y_pos += 70
        
        # Info text
        info_font = pygame.font.SysFont(*FONT_HUD_SIZE)
        info = info_font.render("Use UP/DOWN to choose, ENTER to confirm", True, WHITE)
        screen.blit(info, (200, 650))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.display.quit()
    return modes_list[selected_idx][1]

"""------------------------------------------------------ MAIN PROGRAM ------------------------------------------------------------"""

def run_game(game_mode=None):
    """------------------------------------------------- Initialization ------------------------------------------------------------"""
    # Use provided game mode or select one
    if game_mode is None:
        game_mode = select_difficulty()
        if game_mode is False:  # User quit during selection
            return False
    
    # Reset global groups to avoid accumulation across runs
    bullet_list.empty()
    all_sprites_list.empty()

    pygame.init()
    pygame.mouse.set_visible(False) #hide mouse cursor

    size = (SCREEN_WIDTH, SCREEN_HEIGHT) #Erstellen des Fensters des Spiels
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Flächenland")
    Spieler = Player(*PLAYER_START, all_sprites_list=all_sprites_list) #Erstellung der Spielfigur (outsourced)

    Koordinaten = list(PLAYER_START) # Anfangskoordinaten

    Punktzahl = 0 # erstellen einer Variablen für die Punktzahl
    Daten = False # benötigt, damit highscore nur eunmal abgerufen wird

    # Loop until the user clicks the close button.
    done = False
 
    # Bildanzahl pro Sekunde festlegen
    clock = pygame.time.Clock()
    frame_count = 0
    score = 0
    leben = PLAYER_HEALTH
    
    # Apply game mode multipliers
    player_speed = game_mode.get_player_speed()
    cooldown_frames = game_mode.get_cooldown_frames()
    
    cooldown = 0
    # Track if we clicked a button on end screen
    replay_clicked = False
    quit_clicked = False
    # Toggle for highscores filter (all vs gamemode)
    show_all_highscores = True
    # Clear any pressed keys from previous game, #DEBUGGING issues with automatic movement
    pygame.event.clear(pygame.KEYDOWN)
    pygame.event.clear(pygame.KEYUP)
    
    # Load rooms from data file with game mode multipliers
    Räume = create_rooms_from_data(game_mode)
    current_Raum_Number = 0 #starting room
    current_Raum = Räume[current_Raum_Number]
 
    quit_requested = False

    # Pre-create fonts once (after pygame.init()) using config specs
    font_hud = pygame.font.SysFont(*FONT_HUD_SIZE)
    font_game_over = pygame.font.SysFont(*FONT_GAME_OVER_SIZE)
    font_play_again = pygame.font.SysFont(*FONT_PLAY_AGAIN_SIZE)
    font_quit = pygame.font.SysFont(*FONT_QUIT_SIZE)
    font_name_enter = pygame.font.SysFont(*FONT_NAME_ENTER_SCREEN_SIZE)
    font_name_input = pygame.font.SysFont(*FONT_NAME_INPUT_SIZE)
    font_victory_title = pygame.font.SysFont(*FONT_VICTORY_TITLE_SIZE)
    font_victory_replay = pygame.font.SysFont(*FONT_VICTORY_REPLAY_SIZE)
    font_score = pygame.font.SysFont(*FONT_SCORE_SIZE)
    font_highscores = pygame.font.SysFont(*FONT_HIGHSCORES_SIZE)
    font_highscores_monospace = pygame.font.SysFont(*FONT_HIGHSCORES_MONOSPACE_SIZE)

    """-------------------------------------------- Main Loop ---------------------------------------------------------"""
    """--------------------------------------------- Actions ---------------------------------------------------------"""
    while not done and not quit_requested:
        #Check for events (keyboard, mouse, etc)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #quitting X
                cleanup_quit()
                return False

            # Track mouse button clicks for end screens (winning and loosing)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if leben <= 0:
                    play_again_rect = pygame.Rect(BUTTON_PLAY_AGAIN)
                    quit_rect = pygame.Rect(BUTTON_QUIT)
                    if play_again_rect.collidepoint(pos):
                        replay_clicked = True
                    elif quit_rect.collidepoint(pos):
                        quit_clicked = True
                elif score == 5:
                    win_rect = pygame.Rect(BUTTON_WIN_REPLAY)
                    if win_rect.collidepoint(pos):
                        replay_clicked = True
            
            # Toggle highscores filter with 'T' key during victory
            elif event.type == pygame.KEYDOWN and score == 5:
                if event.key == pygame.K_t:
                    show_all_highscores = not show_all_highscores

            # Track movement keys
            elif event.type == pygame.KEYDOWN:
                # Movement mapping
                movement_keys = {
                    pygame.K_a: (-player_speed, 0),
                    pygame.K_d: (player_speed, 0),
                    pygame.K_w: (0, -player_speed),
                    pygame.K_s: (0, player_speed)
                }
                if event.key in movement_keys:
                    dx, dy = movement_keys[event.key]
                    Spieler.update(dx, dy)
                
                # Shooting mapping
                elif cooldown <= 0:
                    shoot_keys = {
                        pygame.K_UP: "oben",
                        pygame.K_DOWN: "unten",
                        pygame.K_LEFT: "links",
                        pygame.K_RIGHT: "rechts"
                    }
                    if event.key in shoot_keys:
                        direction = shoot_keys[event.key]
                        bullet = Bullet(direction, Spieler.rect.x, Spieler.rect.y, PLAYER_SIZE, BULLET_SIZE, PLAYER_BULLET_SPEED, bullet_list)
                        cooldown = cooldown_frames
 
            # Release movement keys - just negate the velocity
            elif event.type == pygame.KEYUP:
                if event.key in movement_keys:
                    dx, dy = movement_keys[event.key]
                    Spieler.update(-dx, -dy)

        """-------------------------------------------- Room transitions ------------------------------------------------"""
        # check for wall collisions and move player accordingly (disabled during victory/game-over)
        if score < 5 and leben > 0:
            Spieler.move(current_Raum.wall_list)
            current_Raum.enemy_sprites.update()

        # Door logic - dictionary-based transitions
        player_rect = Spieler.rect
        px, py = player_rect.x, player_rect.y
        
        # Check all door transitions
        for door_rect, from_room, to_room, spawn_coords in DOOR_TRANSITIONS:
            if door_rect.collidepoint(px, py) and current_Raum_Number == from_room:
                current_Raum_Number = to_room
                current_Raum = Räume[current_Raum_Number]
                Koordinaten = spawn_coords
                Spieler.set(Koordinaten[0], Koordinaten[1])
                clear_bullets(bullet_list)
                break

        """----------------------------------------------- MAIN ROOM (0) DRAWING ---------------------------------------------------------"""
        #Room creation
        screen.fill(BLACK) #set screen black, to reset whatever happened before and being able to draw the new room        
        
        # Starting room, drawing instructions and labels:
        if current_Raum_Number == 0:
            # Room number labels at doors
            for label, pos in ROOM0_LABELS:
                text = font_hud.render(label, True, GREEN)
                screen.blit(text, pos)

            # Movement instruction arrows
            for arrow in ROOM0_ARROWS:
                pygame.draw.rect(screen, WHITE, arrow["rect"])
                pygame.draw.polygon(screen, WHITE, arrow["polygon"])

            # Movement key labels
            for key, pos in ROOM0_KEY_LABELS:
                text = font_hud.render(key, True, WHITE)
                screen.blit(text, pos)

            # Instruction texts
            shoot_text = font_hud.render("Schießen mit den PFEILTASTEN", True, WHITE)
            screen.blit(shoot_text, ROOM0_SHOOT_TEXT_POS)
            key_text = font_hud.render("Sammle diese Schlüssel", True, WHITE)
            screen.blit(key_text, ROOM0_KEYS_TEXT_POS)

        """--------------------------------------------------- Collisions --------------------------------------------------------"""
        if score < 5 and leben > 0:
            # Collision detection: keys and enemies
            key_hit_list = pygame.sprite.spritecollide(Spieler, current_Raum.key_list, True)
            gegner_hit_list = pygame.sprite.spritecollide(Spieler, current_Raum.enemy_sprites, False)
 
            # Process collisions
            score += len(key_hit_list)
            
            if gegner_hit_list:
                leben -= 1
                Spieler.set(Koordinaten[0], Koordinaten[1])

            # Collision detection: bullets hitting walls or enemies
            for bullet in bullet_list:
                # Check for collision with walls
                if pygame.sprite.spritecollide(bullet, current_Raum.wall_list, False):
                    bullet_list.remove(bullet)
                    continue

                # Check for collision with enemies
                enemy_hit_list = pygame.sprite.spritecollide(bullet, current_Raum.enemy_sprites, False)
                if enemy_hit_list:
                    bullet_list.remove(bullet)
                    for enemy in enemy_hit_list:
                        enemy.gesundheit -= 1
                        if enemy.gesundheit <= 0:
                            current_Raum.enemy_sprites.remove(enemy)

        """------------------------------------------------------ HUD --------------------------------------------------------------"""
        # HUD and rendering (Heads up display)
        hud_items = [
            (f"Schlüssel: {score}", (1000, 30)),
            (f"Leben: {leben}", (1000, 55)),
            (f"Time: {frames_to_time_string(frame_count)}", (1000, 80))
        ]
        for text_str, pos in hud_items:
            text = font_hud.render(text_str, True, GREEN)
            screen.blit(text, pos)
 
        # Draw all sprites
        all_sprites_list.draw(screen)
        bullet_list.update()
        bullet_list.draw(screen)
        current_Raum.wall_list.draw(screen)
        current_Raum.key_list.draw(screen)
        current_Raum.enemy_sprites.draw(screen)
            
        """---------------------------------------------------- End of game ------------------------------------------------------"""
        # End screens: Game Over or Victory

        if leben <= 0:  # GAME OVER
            pygame.mouse.set_visible(True)
            Spieler.change_x = 0
            Spieler.change_y = 0
            
            screen.fill(BLACK)
            
            screen.blit(font_game_over.render("GAME OVER", True, RED), GAME_OVER_TEXT_POS)
            # Play Again button (outer + inner with 1px border)
            pygame.draw.rect(screen, WHITE, BUTTON_PLAY_AGAIN)
            pygame.draw.rect(screen, BLUE, (BUTTON_PLAY_AGAIN[0] + 1, BUTTON_PLAY_AGAIN[1] + 1, 
                                            BUTTON_PLAY_AGAIN[2] - 2, BUTTON_PLAY_AGAIN[3] - 2))
            screen.blit(font_play_again.render("PLAY AGAIN!", True, WHITE), PLAY_AGAIN_TEXT_POS)

            # Quit button (outer + inner with 2px border)
            pygame.draw.rect(screen, WHITE, BUTTON_QUIT)
            pygame.draw.rect(screen, RED, (BUTTON_QUIT[0] + 2, BUTTON_QUIT[1] + 2, 
                                           BUTTON_QUIT[2] - 4, BUTTON_QUIT[3] - 4))
            screen.blit(font_quit.render("QUIT", True, WHITE), QUIT_TEXT_POS)

            if replay_clicked:
                all_sprites_list.remove(Spieler)
                bullet_list.empty()
                return True
            if quit_clicked:
                cleanup_quit()
                return False

        elif score == 5:  # VICTORY
            if Daten == False:  # Save highscore once
                Punktzahl = int((36000 - frame_count + 3000 * leben) * game_mode.get_score_multiplier())
                Daten = True
                Zeit = frames_to_time_string(frame_count)
                
                # Username input loop
                username = "Player"
                input_prompt = True
                input_text = ""
                
                while input_prompt:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cleanup_quit()
                            return False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                username = input_text.strip() or "Player"
                                input_prompt = False
                            elif event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                            elif len(input_text) < 15:
                                input_text += event.unicode
                    
                    screen.fill(BLACK)              
                    screen.blit(font_name_enter.render("Enter your name:", True, WHITE), NAME_ENTER_SCREEN_POS)
                    screen.blit(font_name_input.render(input_text + "_", True, GREEN), NAME_INPUT_POS)
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                if quit_requested:
                    return False
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                highscores = add_highscore(username, Punktzahl, current_date, frame_count, game_mode.name)

            Spieler.change_x = 0
            Spieler.change_y = 0
            pygame.mouse.set_visible(True)

            screen.fill(BLACK)

            # Replay button (outer + inner with 1px border)
            pygame.draw.rect(screen, WHITE, BUTTON_WIN_REPLAY)
            pygame.draw.rect(screen, YELLOW, (BUTTON_WIN_REPLAY[0] + 1, BUTTON_WIN_REPLAY[1] + 1,
                                              BUTTON_WIN_REPLAY[2] - 2, BUTTON_WIN_REPLAY[3] - 2))
            
            # Title and button text
            screen.blit(font_victory_title.render("Gewonnen!", True, GREEN), VICTORY_TITLE_POS)
            screen.blit(font_victory_replay.render("Nochmal?", True, BLACK), VICTORY_REPLAY_TEXT_POS)

            # Score information
            score_items = [
                (f"Deine Punktzahl: {Punktzahl}", SCORE_BLOCK_Y),
                (f"Zeit: {Zeit}", SCORE_BLOCK_Y + SCORE_LINE_SPACING),
                (f"Leben: {leben}", SCORE_BLOCK_Y + 2 * SCORE_LINE_SPACING)
            ]
            for text_str, y in score_items:
                screen.blit(font_score.render(text_str, True, WHITE), (SCORE_BLOCK_X, y))

            # Highscores display
            screen.blit(font_highscores.render("TOP 10 HIGHSCORES:", True, YELLOW), HIGHSCORES_TITLE_POS)
            
            # Filter highscores based on toggle
            if show_all_highscores:
                display_scores = highscores[:MAX_HIGHSCORES]
                filter_text = "All Modes"
            else:
                display_scores = [e for e in highscores if e.get('mode', 'NORMAL') == game_mode.name][:MAX_HIGHSCORES]
                filter_text = f"{game_mode.name} Mode"
            
            # Calculate max lengths for minimal spacing
            max_username_len = max((len(entry['username']) for entry in display_scores), default=10)
            max_mode_len = max((len(entry.get('mode', 'NORMAL')) for entry in display_scores), default=6)
            
            # Display filter text and toggle hint
            filter_display = font_hud.render(f"[T] Filter: {filter_text}", True, WHITE)
            screen.blit(filter_display, (SCORE_BLOCK_X, HIGHSCORES_TITLE_POS[1] - 30))
            
            for i, entry in enumerate(display_scores[:10], 1):
                mode_label = entry.get('mode', 'NORMAL')
                #same spacing for all entries using monospace font with calculated minimum spacing
                score_line = f"{i}.".ljust(3) + f" {entry['username'].ljust(max_username_len)}: {entry['score']} -- {entry['time']} -- {mode_label.ljust(max_mode_len)} -- ({entry['date']})"
                color = RED if (entry['username'] == username and entry['score'] == Punktzahl and entry['date'] == current_date) else GREEN
                screen.blit(font_highscores_monospace.render(score_line, True, color), (SCORE_BLOCK_X, HIGHSCORES_LIST_Y_START + (i - 1) * HIGHSCORES_LINE_SPACING))

            if replay_clicked:
                all_sprites_list.remove(Spieler)
                bullet_list.empty()
                return True

        """-----------------------------------------------ENDING CONDITIONS OF LOOP----------------------------------------------------"""
        # Erhöhen des timers/bildanzahl
        frame_count += 1
        if cooldown > 0:
            cooldown -= 1
        if quit_requested or done:
            break
        clock.tick(FRAME_RATE)  
        # Alles gezeichnete darstellen.
        pygame.display.flip()
 
    # Cleanup and exit
    cleanup_quit()
    # No replay requested, exit normally
    return False

if __name__ == "__main__":
    # Loop to support in-app restarts without recursion
    while True:
        replay = run_game()
        if not replay:
            break
    # Ensure process exits cleanly (force exit to avoid lingering processes)
    cleanup_quit()
    os._exit(0)
