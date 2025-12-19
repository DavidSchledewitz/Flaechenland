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

"""------------------------------------------------------MAIN PROGRAM------------------------------------------------------------"""
def run_game():
    """--------------------------------------------------Initialization------------------------------------------------------------"""
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
    cooldown = 0
    # Track if we clicked a button on end screen
    replay_clicked = False
    quit_clicked = False
    # Clear any pressed keys from previous game, #DEBUGGING issues with automatic movement
    pygame.event.clear(pygame.KEYDOWN)
    pygame.event.clear(pygame.KEYUP)
    
    # Load rooms from data file
    Räume = create_rooms_from_data()
    current_Raum_Number = 0 #starting room
    current_Raum = Räume[current_Raum_Number]
 
    quit_requested = False

    """-------------------------------------------- Main Loop ---------------------------------------------------------"""
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

            # Track movement keys
            elif event.type == pygame.KEYDOWN:
                # Movement mapping
                movement_keys = {
                    pygame.K_a: (-PLAYER_SPEED, 0),
                    pygame.K_d: (PLAYER_SPEED, 0),
                    pygame.K_w: (0, -PLAYER_SPEED),
                    pygame.K_s: (0, PLAYER_SPEED)
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
                        cooldown = BULLET_COOLDOWN_FRAMES
 
            # Release movement keys - just negate the velocity
            elif event.type == pygame.KEYUP:
                if event.key in movement_keys:
                    dx, dy = movement_keys[event.key]
                    Spieler.update(-dx, -dy)

        """------------------------------------------------------------------------------------------------------------------"""
        # check for wall collisions and move player accordingly
        Spieler.move(current_Raum.wall_list)
        current_Raum.enemy_sprites.update()

        
        # Door logic - dictionary-based transitions
        player_rect = Spieler.rect
        px, py = player_rect.x, player_rect.y
        
        # Define door transitions: list of (door_rect, from_room, to_room, spawn_coords)
        door_transitions = [
            (START_DOOR_TOP, 0, 4, [575, 615]),
            (START_DOOR_BOTTOM, 0, 3, [575, 35]),
            (START_DOOR_LEFT, 0, 1, [1115, 325]),
            (START_DOOR_RIGHT, 0, 2, [35, 325]),
            (START_DOOR_RIGHT, 1, 0, [35, 325]),
            (START_DOOR_LEFT, 2, 0, [1115, 325]),
            (START_DOOR_BOTTOM, 4, 0, [575, 35]),
            (START_DOOR_TOP, 3, 0, [575, 615])
        ]
        
        # Check all door transitions
        for door_rect, from_room, to_room, spawn_coords in door_transitions:
            if door_rect.collidepoint(px, py) and current_Raum_Number == from_room:
                current_Raum_Number = to_room
                current_Raum = Räume[current_Raum_Number]
                Koordinaten = spawn_coords
                Spieler.set(Koordinaten[0], Koordinaten[1])
                clear_bullets(bullet_list)
                break

        """---------------------------------------------------------------------------------------------------------------------"""
        #Room creation
        screen.fill(BLACK) #set screen black, to reset whatever happened before and being able to draw the new room        
        font = pygame.font.SysFont("Calibri", 25, True, False) #Definition für gedruckten Text
        
        # Starting room, drawing instructions and labels:
        if current_Raum_Number == 0:
            # Room number labels at doors
            room_labels = [
                ("1", (1155, 340)),  # Right door
                ("2", (595, 35)),    # Top door
                ("3", (30, 340)),    # Left door
                ("4", (595, 645))    # Bottom door
            ]
            for label, pos in room_labels:
                text = font.render(label, True, GREEN)
                screen.blit(text, pos)

            # Movement instruction arrows
            arrows = [
                # Right arrow
                {"rect": (635, 347, 20, 6), "polygon": ((655, 342), (655, 358), (667, 350))},
                # Left arrow
                {"rect": (545, 347, 20, 6), "polygon": ((545, 342), (545, 358), (533, 350))},
                # Up arrow
                {"rect": (597, 295, 6, 20), "polygon": ((592, 295), (608, 295), (600, 283))},
                # Down arrow
                {"rect": (597, 385, 6, 20), "polygon": ((592, 405), (608, 405), (600, 417))}
            ]
            for arrow in arrows:
                pygame.draw.rect(screen, WHITE, arrow["rect"])
                pygame.draw.polygon(screen, WHITE, arrow["polygon"])

            # Movement key labels
            key_labels = [
                ("W", (590, 260)),
                ("S", (595, 420)),
                ("D", (671, 339)),
                ("A", (516, 339))
            ]
            for key, pos in key_labels:
                text = font.render(key, True, WHITE)
                screen.blit(text, pos)

            # Instruction texts
            shoot_text = font.render("Schießen mit den PFEILTASTEN", True, WHITE)
            screen.blit(shoot_text, (35, 650))
            key_text = font.render("Sammle diese Schlüssel", True, WHITE)
            screen.blit(key_text, (55, 155))

        """-----------------------------------------------------------------------------------------------------------------------"""
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

        """-----------------------------------------------------------------------------------------------------------------------"""
        # HUD and rendering (Heads up display)
        font = pygame.font.SysFont('Calibri', 25, True, False)

        # HUD stats display
        hud_items = [
            (f"Schlüssel: {score}", (1000, 30)),
            (f"Leben: {leben}", (1000, 55)),
            (f"Time: {frames_to_time_string(frame_count)}", (1000, 80))
        ]
        for text_str, pos in hud_items:
            text = font.render(text_str, True, GREEN)
            screen.blit(text, pos)
 
        # Draw all sprites
        all_sprites_list.draw(screen)
        bullet_list.update()
        bullet_list.draw(screen)
        current_Raum.wall_list.draw(screen)
        current_Raum.key_list.draw(screen)
        current_Raum.enemy_sprites.draw(screen)
            
        """-----------------------------------------------------------------------------------------------------------------------"""
        # End screens: Game Over or Victory

        if leben <= 0:  # GAME OVER
            pygame.mouse.set_visible(True)
            Spieler.change_x = 0
            Spieler.change_y = 0
            
            screen.fill(BLACK)
            font_large = pygame.font.SysFont("Calibri", 200, True, False)
            font_button = pygame.font.SysFont("Calibri", 100, True, False)
            font_quit = pygame.font.SysFont("Calibri", 60, True, False)
            
            screen.blit(font_large.render("GAME OVER", True, RED), (82, 150))

            # Play Again button (outer + inner with 1px border)
            pygame.draw.rect(screen, WHITE, BUTTON_PLAY_AGAIN)
            pygame.draw.rect(screen, BLUE, (BUTTON_PLAY_AGAIN[0] + 1, BUTTON_PLAY_AGAIN[1] + 1, 
                                            BUTTON_PLAY_AGAIN[2] - 2, BUTTON_PLAY_AGAIN[3] - 2))
            screen.blit(font_button.render("PLAY AGAIN!", True, WHITE), (330, 500))

            # Quit button (outer + inner with 2px border)
            pygame.draw.rect(screen, WHITE, BUTTON_QUIT)
            pygame.draw.rect(screen, RED, (BUTTON_QUIT[0] + 2, BUTTON_QUIT[1] + 2, 
                                           BUTTON_QUIT[2] - 4, BUTTON_QUIT[3] - 4))
            screen.blit(font_quit.render("QUIT", True, WHITE), (80, 575))

            if replay_clicked:
                all_sprites_list.remove(Spieler)
                bullet_list.empty()
                return True
            if quit_clicked:
                cleanup_quit()
                return False

        elif score == 5:  # VICTORY
            if Daten == False:  # Save highscore once
                Punktzahl = 36000 - frame_count + 3000 * leben
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
                    font_large = pygame.font.SysFont("Calibri", 60, True, False)
                    font_input = pygame.font.SysFont("Calibri", 40, False, False)
                    
                    screen.blit(font_large.render("Enter your name:", True, WHITE), (200, 300))
                    screen.blit(font_input.render(input_text + "_", True, GREEN), (200, 400))
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                if quit_requested:
                    return False
                highscores = add_highscore(username, Punktzahl, frame_count)

            Spieler.change_x = 0
            Spieler.change_y = 0
            pygame.mouse.set_visible(True)

            screen.fill(BLACK)

            # Victory screen layout
            x_pos = 60
            score_y_pos = 550

            # Replay button (outer + inner with 1px border)
            pygame.draw.rect(screen, WHITE, BUTTON_WIN_REPLAY)
            pygame.draw.rect(screen, YELLOW, (BUTTON_WIN_REPLAY[0] + 1, BUTTON_WIN_REPLAY[1] + 1,
                                              BUTTON_WIN_REPLAY[2] - 2, BUTTON_WIN_REPLAY[3] - 2))

            # Fonts for victory screen
            font_title = pygame.font.SysFont("Calibri", 220, True, False)
            font_replay = pygame.font.SysFont("Calibri", 90, True, False)
            font_score = pygame.font.SysFont("Calibri", 50, True, True)
            font_highscores = pygame.font.SysFont("Calibri", 25, False, False)

            # Title and button text
            screen.blit(font_title.render("Gewonnen!", True, GREEN), (x_pos, -40))
            screen.blit(font_replay.render("Nochmal?", True, BLACK), (BUTTON_WIN_REPLAY[0] + 20, BUTTON_WIN_REPLAY[1] + 80))

            # Score information
            score_items = [
                (f"Deine Punktzahl: {Punktzahl}", score_y_pos),
                (f"Zeit: {Zeit}", score_y_pos + 45),
                (f"Leben: {leben}", score_y_pos + 90)
            ]
            for text_str, y in score_items:
                screen.blit(font_score.render(text_str, True, WHITE), (x_pos, y))

            # Highscores display
            highscores = load_highscores()
            screen.blit(font_highscores.render("TOP 10 HIGHSCORES:", True, YELLOW), (x_pos, 200))
            
            y_pos = 235
            for i, entry in enumerate(highscores[:10], 1):
                score_line = f"{i}. {entry['username']}: {entry['score']} -- {entry['time']} -- ({entry['date']})"
                color = RED if (entry['username'] == username and entry['score'] == Punktzahl) else GREEN
                screen.blit(font_highscores.render(score_line, True, color), (x_pos, y_pos))
                y_pos += 30

            if replay_clicked:
                all_sprites_list.remove(Spieler)
                bullet_list.empty()
                return True

        """-----------------------------------------------ENDING CONDITIONS OF LOOP----------------------------------------------------"""
        # Erhöhen des timers/bildanzahl
        frame_count += 1
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
