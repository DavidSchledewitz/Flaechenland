#!/usr/bin/python3

#Flächenland - Ein Softwareprojekt von David, Marius, Milena und Lasse, Q2a 2017
import pygame
import json
import os
from datetime import datetime
# import random
import sys

 
# Ein paar Farben definieren
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

bullet_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# Core configuration
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
PLAYER_SIZE = 50
PLAYER_START = (575, 325)
PLAYER_SPEED = 5
PLAYER_HEALTH = 5
BULLET_SIZE = 4
PLAYER_BULLET_SPEED = 12
BULLET_COOLDOWN_FRAMES = 5
FRAME_RATE = 60

# UI rectangles
BUTTON_PLAY_RECT = pygame.Rect(300, 480, 600, 130) #(to remember: x, y, width, height), x, y is top-left corner
BUTTON_QUIT_RECT = pygame.Rect(50, 560, 200, 80)
BUTTON_WIN_RECT = pygame.Rect(700, 400, 400, 250)

FONT_FAMILY = "Calibri"

# Doors (use rectangles instead of raw ranges)
START_DOOR_TOP = pygame.Rect(550, 0, 51, 21)
START_DOOR_BOTTOM = pygame.Rect(550, 629, 51, 71)
START_DOOR_LEFT = pygame.Rect(0, 300, 21, 51)
START_DOOR_RIGHT = pygame.Rect(1129, 300, 71, 51)

def cleanup_quit():
    try:
        bullet_list.empty()
        all_sprites_list.empty()
    except Exception:
        pass
    try:
        pygame.display.quit()
    except Exception:
        pass
    try:
        pygame.quit()
    except Exception:
        pass


"""-----------------------------------------------------------------------------"""

#Grund Klasse für Spieler und Gegner

class Block(pygame.sprite.Sprite):
    """
    Diese Klasse erzeugt ein Rechteck.
    Sie erbt von der "Sprite" Klasse in Pygame.
    """
 
    def __init__(self, color, width, height):
        
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse für den bewegbaren Spieler

class Player(Block):
    """
    Diese Klasse erstellt die Spielfigur.
    Sie erbt von der Blockklasse
    """

    def __init__(self, x, y):  #Konstruktor, erstellt die Figur

        super().__init__(BLUE, PLAYER_SIZE, PLAYER_SIZE)

        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        all_sprites_list.add(self)

    

    def update(self,x,y):  #Funktion, die die Geschwindigkeit des Spielers ändert
        self.change_x += x
        self.change_y += y

    def set(self,x,y): #Funktion, die die Figur auf eine bestimmte Stelle setzt
        self.rect.x = x
        self.rect.y = y

    def move(self,Wände):  #kümmert sich um die Bewegung, arbeitet mit Kollisionen

        #links/rechts Bewegung
        self.rect.x += self.change_x

        #Kollisionsabfrage
        block_hit_list = pygame.sprite.spritecollide(self,Wände,False)
        for block in block_hit_list:
            
            if self.change_x > 0: #bei Treffen von rechts, an links Kante setzen
                self.rect.right = block.rect.left

            elif self.change_x < 0: #ei Treffen von links, an rechts Kante setzen
                self.rect.left = block.rect.right

        #oben/unten Bewegung
        self.rect.y += self.change_y

        #Kollisionsabfrage
        block_hit_list = pygame.sprite.spritecollide(self,Wände,False)
        for block in block_hit_list:

            if self.change_y > 0: #bei Treffern von oben, an obere Kante setzen
                self.rect.bottom = block.rect.top 

            elif self.change_y < 0: #bei Treffern von unten, an untere Kante setzen
                self.rect.top = block.rect.bottom

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""


class Gegner(Block):
    """
    Diese Klasse erzeugt sich bewegende Gegner.
    Sie erbt von der Block-Klasse.
    """

    def __init__(self, x, y, rect_speed_x, rect_speed_y, links,rechts,oben,unten):
    
        super().__init__(RED, 50, 50)

        self.rect.x = x
        self.rect.y = y

        self.gesundheit = 5

        self.change_x = rect_speed_x
        self.change_y = rect_speed_y

        self.left_boundary = links
        self.right_boundary = rechts
        self.top_boundary = oben
        self.bottom_boundary = unten
              

    def update(self):
        
        if self.rect.right >= self.right_boundary or self.rect.left <= self.left_boundary:
            self.change_x *= -1
        if self.rect.bottom >= self.bottom_boundary or self.rect.top <= self.top_boundary:
            self.change_y *= -1
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        

"""-----------------------------------------------------------------------------"""

# Klasse für die Geschosse

class Bullet(Block):
    """
    Diese Klasse erzeugt die Geschosse.
    Sie erbt von der Klasse Block.
    """

    def __init__(self, dic,x,y):
        super().__init__(WHITE, BULLET_SIZE, BULLET_SIZE)


        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        direct = dic

        center_offset = (PLAYER_SIZE - BULLET_SIZE) // 2

        if direct == "oben":
            self.rect.x = x + center_offset
            self.change_y = -PLAYER_BULLET_SPEED
        elif direct == "unten":
            self.rect.x = x + center_offset
            self.rect.y = y + PLAYER_SIZE - BULLET_SIZE
            self.change_y = PLAYER_BULLET_SPEED
        elif direct == "links":
            self.rect.y = y + center_offset
            self.change_x = -PLAYER_BULLET_SPEED
        elif direct == "rechts":
            self.rect.x = x + PLAYER_SIZE - BULLET_SIZE
            self.rect.y = y + center_offset
            self.change_x = PLAYER_BULLET_SPEED

        bullet_list.add(self)

    def update(self):
        
        self.rect.x += self.change_x
        self.rect.y += self.change_y

"""-----------------------------------------------------------------------------"""
            
        

"""-----------------------------------------------------------------------------"""

# Klasse aller Schlüssel

class Schluessel(pygame.sprite.Sprite):
    """
    Diese Klasse stellt die Schlüssel dar.
    """
 
    def __init__(self, x, y):
 
        super().__init__()
        #relative path to image, located in the Flächenland folder
        self.image = pygame.image.load("key-icon.png").convert()
        #adjust image size
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
 
"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Hauptklasse aller Räume 

class Raum(object):
    """
    Leert die Objekt-/Spritelisten und legt für jeweiligen Raum neue Objektgruppe an.
    """

    wall_list = None
    enemy_sprites = None
    key_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse zum erstellen der Wände

class Wand(pygame.sprite.Sprite):
    """Diese Klasse erzeugt die Wände"""
    
    def __init__(self, x, y, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

"""-----------------------------------------------------------------------------"""


def build_room_groups(walls, keys, enemies):
    """Helper to create sprite groups for a room from data lists."""
    wall_group = pygame.sprite.Group(*(Wand(*w[:4]) for w in walls))
    key_group = pygame.sprite.Group(*(Schluessel(*k) for k in keys))
    enemy_group = pygame.sprite.Group(*(Gegner(*e) for e in enemies))
    return wall_group, key_group, enemy_group



"""-----------------------------------------------------------------------------"""

# Klasse Raum

class Anfangsraum(Raum):
    """
    Die Klasse erzeugt alle Daten für den Anfangsraum.
    Dazu gehören die Positionen der Wände, Schlüssel und Gegner
    """
    
    def __init__(self):
        super().__init__()

        #Wände erstellen
        walls = [
            [0,0,550,20,WHITE],
            [650,0,550,20,WHITE],
            [0,680,550,20,WHITE],
            [650,680,550,20,WHITE],
            [0,400,20,280,WHITE],
            [0,20,20,280,WHITE],
            [1180,20,20,280,WHITE],
            [1180,400,20,280,WHITE],
            [-20,300,20,100], #unsichtbare sprites als Begrenzung
            [1201,300,20,100],
            [550,-20,100,20],
            [550,701,100,20],
        ]

        keys = [(150, 200)]
        enemies = []

        self.wall_list, self.key_list, self.enemy_sprites = build_room_groups(walls, keys, enemies)

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse Raum

class Raumlinks(Raum):
    """
    Die Klasse erzeugt alle Daten für den Anfangsraum.
    Dazu gehören die Positionen der Wände, Schlüssel und Gegner
    """
    
    def __init__(self):
        super().__init__()

        #Wände erstellen
        walls = [
            [0,0,1200,20],
            [0,680,1200,20],
            [0,20,20,680],
            [1180,20,20,280],
            [1180,400,20,480],
            [160,20,20,480],
            [500,270,20,430],
            [520,270,150,20],
            [790,20,20,480],
            [1201,300,20,100],
        ]

        keys = [(70, 335)]
        enemies = [
            [65,30,0,10,20,1180,20,500],
            [710,270,0,-5,20,1180,270,680],
            [195,40,0,-5,20,1180,40,660],
            [275,195,0,-5,20,1180,40,660],
            [355,350,0,-5,20,1180,40,660],
            [435,505,0,-5,20,1180,40,660],
        ] #to remember (x, y, speed_x, speed_y, left, right, top, bottom), left right etc are boundaries for enemy movement

        self.wall_list, self.key_list, self.enemy_sprites = build_room_groups(walls, keys, enemies)

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse Raum 

class Raumrechts(Raum):
    """
    Die Klasse erzeugt alle Daten für den Anfangsraum.
    Dazu gehören die Positionen der Wände, Schlüssel und Gegner
    """
    
    def __init__(self):
        super().__init__()

        #Wände erstellen
        walls = [
            [0,0,1200,20],
            [0,680,1200,20],
            [1180,20,20,680],
            [0,20,20,280],
            [0,400,20,280],
            [800,410,20,280],
            [800,20,20,270],
            [-20,300,20,100],
        ]

        keys = [(1125, 335)]
        enemies = [
            [200,200,5,-5,20,800,20,680],
            [200,450,5,5,20,800,20,680],
            [920,325,0,5,20,1180,50,650],
        ]

        self.wall_list, self.key_list, self.enemy_sprites = build_room_groups(walls, keys, enemies)

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse Raum 

class Raumunten(Raum):
    """
    Die Klasse erzeugt alle Daten für den Anfangsraum.
    Dazu gehören die Positionen der Wände, Schlüssel und Gegner
    """
    
    def __init__(self):
        super().__init__()

        #Wände erstellen
        walls = [
            [0,680,1200,20],
            [0,20,20,680],
            [1180,20,20,680],
            [0,0,550,20],
            [650,0,550,20],
            [250,20,20,195],
            [360,20,20,195],
            [250,350,20,185],
            [360,350,20,185],
            [270,515,90,20],
            [380,350,440,20],
            [930,20,20,195],
            [820,20,20,195],
            [820,350,20,195],
            [930,350,20,195],
            [840,525,90,20],
            [550,-20,100,20],
        ]

        keys = [(580, 440)]
        enemies = [
            [290,30,0,-5,20,1180,30,505],
            [860,30,0,-5,20,1180,30,505],
            [380,505,-5,5,380,820,370,680],
            [770,505,5,-5,380,820,370,680],
        ]

        self.wall_list, self.key_list, self.enemy_sprites = build_room_groups(walls, keys, enemies)

"""-----------------------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""

# Klasse Raum 

class Raumoben(Raum):
    """
    Die Klasse erzeugt alle Daten für den Anfangsraum.
    Dazu gehören die Positionen der Wände, Schlüssel und Gegner
    """
    
    def __init__(self):
        super().__init__()

        #Wände erstellen
        walls = [
            [0,0,1200,20],
            [0, 20, 20, 660],
            [1180,20,20,660],
            [0,680,550,20],
            [650,680,550,20],
            [220,320,760,20],
            [590,340,20,100],
            [500,20,20,150],
            [680,20,20,150],
            [550,701,100,20],
        ]

        keys = [(580, 35)]
        enemies = [
            [640,360,5,0,630,1160,20,680],
            [510,360,-5,0,40,570,20,680],
            [20,135,-5,5,20,500,20,320],
            [450,135,5,-5,20,500,20,320],
            [700,135,-5,5,700,1180,20,320],
            [1130,135,5,-5,700,1180,20,320],
        ]

        self.wall_list, self.key_list, self.enemy_sprites = build_room_groups(walls, keys, enemies)
        
"""-----------------------------------------------------------------------------"""


def clear():
    for item in bullet_list:
        bullet_list.remove(item)


def load_highscores():
    """Load highscores from JSON file"""
    if os.path.exists("highscores.json"):
        try:
            with open("highscores.json", "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_highscores(highscores):
    """Save highscores to JSON file"""
    with open("highscores.json", "w") as f:
        json.dump(highscores, f, indent=2)


def add_highscore(username, score):
    """Add a new score to the highscore list and return top 10"""
    highscores = load_highscores()
    
    # Add new score
    new_entry = {
        "username": username,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    highscores.append(new_entry)
    
    # Sort by score (descending) and keep top 10
    highscores.sort(key=lambda x: x["score"], reverse=True)
    # in json, save all scores
    save_highscores(highscores)
    
    highscores = highscores[:10]
    
    return highscores


"""-----------------------------------------------------------------------------"""

# Beginn des Hauptprogramms 

def run_game():
    
    # Reset global groups to avoid accumulation across runs
    bullet_list.empty()
    all_sprites_list.empty()

    pygame.init()

    pygame.mouse.set_visible(False) #Verbergen des Mauszeigers

    size = (SCREEN_WIDTH, SCREEN_HEIGHT) #Erstellen des Fensters des Spiels
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Flächenland")

    Spieler = Player(*PLAYER_START) #Erstellung der Spielfigur

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
    
    # Clear any pressed keys from previous game, debugging issues with automatic movement
    pygame.event.clear(pygame.KEYDOWN)
    pygame.event.clear(pygame.KEYUP)
    

    """-------------------------------------------------------------------------"""

    #Erstellen einer Liste, in der die jeweiligen Räume enthalten sind

    Räume = []

    room = Anfangsraum()
    Räume.append(room)

    room = Raumlinks()
    Räume.append(room)

    room = Raumrechts()
    Räume.append(room)

    room = Raumunten()
    Räume.append(room)

    room = Raumoben()
    Räume.append(room)

    current_Raum_Number = 0
    current_Raum = Räume[current_Raum_Number]

    """-------------------------------------------------------------------------"""
 
    quit_requested = False

    # -------- Main Program Loop -----------
    while not done and not quit_requested:


        """---------------------------------------------------------------------"""

        # Tastenabfragen
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                cleanup_quit()
                return False
            
            # Track mouse button clicks for end screens
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if leben <= 0:
                    if BUTTON_PLAY_RECT.collidepoint(pos):
                        replay_clicked = True
                    elif BUTTON_QUIT_RECT.collidepoint(pos):
                        quit_clicked = True
                elif score == 5:
                    if BUTTON_WIN_RECT.collidepoint(pos):
                        replay_clicked = True

            # welche Taste wurde gedrückt, Bewegung anpassen
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_a:
                    Spieler.update(-PLAYER_SPEED,0)
                elif event.key == pygame.K_d:
                    Spieler.update(PLAYER_SPEED,0)
                elif event.key == pygame.K_w:
                    Spieler.update(0,-PLAYER_SPEED)
                elif event.key == pygame.K_s:
                    Spieler.update(0,PLAYER_SPEED)

                #Aufrufen der Bulletfunktion mit den Pfeiltasten ("schießen") schuss geschwindigkeit
                elif event.key == pygame.K_UP and cooldown <= 0:
                    bullet = Bullet("oben",Spieler.rect.x,Spieler.rect.y)
                    cooldown = BULLET_COOLDOWN_FRAMES
                elif event.key == pygame.K_DOWN and cooldown <= 0:
                    bullet = Bullet("unten",Spieler.rect.x,Spieler.rect.y)
                    cooldown = BULLET_COOLDOWN_FRAMES
                elif event.key == pygame.K_LEFT and cooldown <= 0:
                    bullet = Bullet("links",Spieler.rect.x,Spieler.rect.y)
                    cooldown = BULLET_COOLDOWN_FRAMES
                elif event.key == pygame.K_RIGHT and cooldown <= 0:
                    bullet = Bullet("rechts",Spieler.rect.x,Spieler.rect.y)
                    cooldown = BULLET_COOLDOWN_FRAMES

                
                
 
            # welche Taste wurde losgelassen, Bewegung unpassen
            elif event.type == pygame.KEYUP:
                
                if event.key == pygame.K_a:
                    Spieler.update(PLAYER_SPEED,0)
                elif event.key == pygame.K_d:
                    Spieler.update(-PLAYER_SPEED,0)
                elif event.key == pygame.K_w:
                    Spieler.update(0,PLAYER_SPEED)
                elif event.key == pygame.K_s:
                    Spieler.update(0,-PLAYER_SPEED)

        """---------------------------------------------------------------------"""
            


        # eigentlcihe Raumabfrage, testen auf Kollisionen mit Wänden im aktuellen Raum
        Spieler.move(current_Raum.wall_list)

        current_Raum.enemy_sprites.update()

        
        """---------------------------------------------------------------------"""

        # Türenabfrage
        # Prinzip: die neue Klasse als aktiven Raum setzen und den Anfangspunkt definieren
        player_rect = Spieler.rect
        px, py = player_rect.x, player_rect.y
        
        if START_DOOR_TOP.collidepoint(px, py) and current_Raum_Number == 0:
            current_Raum_Number = 4
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,615]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if START_DOOR_BOTTOM.collidepoint(px, py) and current_Raum_Number == 0:
            current_Raum_Number = 3
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,35]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if START_DOOR_LEFT.collidepoint(px, py) and current_Raum_Number == 0:
            current_Raum_Number = 1
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [1115,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if START_DOOR_RIGHT.collidepoint(px, py) and current_Raum_Number == 0:
            current_Raum_Number = 2
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [35,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()



        # Zurück zum Start
        

        if START_DOOR_RIGHT.collidepoint(px, py) and current_Raum_Number == 1:
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [35,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if START_DOOR_LEFT.collidepoint(px, py) and current_Raum_Number == 2:
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [1115,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if START_DOOR_BOTTOM.collidepoint(px, py) and current_Raum_Number == 4:
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,35]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if START_DOOR_TOP.collidepoint(px, py) and current_Raum_Number == 3:
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,615]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            

        """---------------------------------------------------------------------"""



        """---------------------------------------------------------------------"""

        # Beginn des Zeichnens

        screen.fill(BLACK) #Zurücksetzten des Bildschirms in (leere) Ausgangsposition

        
        font = pygame.font.SysFont("Calibri", 25, True, False) #Definition für gedruckten Text

        
        # Hintergrundbeachriftung für Anfangsraum

        if current_Raum_Number == 0:
            #Texte zur Beschriftung des Anfangsraumes
            text1 = font.render("1", True, (0,255,0))
            text2 = font.render("2", True, (0,255,0))
            text3 = font.render("3", True, (0,255,0))
            text4 = font.render("4", True, (0,255,0))
            screen.blit(text2, (595, 35))
            screen.blit(text4, (595, 645))
            screen.blit(text1, (1155, 340))
            screen.blit(text3, (30,340))

            #Texte für die Spielanleitung im Hintergrund
            #Erschaffen der besten Pfeile die Gott jemals kreiert hat, oder so ähnlich
    
            #Pfeile links und rechts
            pygame.draw.rect(screen, WHITE,(635,347,20,6))
            pygame.draw.polygon(screen, WHITE, ((655,342),(655,358),(667,350)))
            pygame.draw.rect(screen, WHITE, (545,347,20,6))
            pygame.draw.polygon(screen, WHITE, ((545,342),(545,358),(533,350)))

            #Pfeile oben und unten
            pygame.draw.rect(screen, WHITE, (597,295,6,20))
            pygame.draw.polygon(screen, WHITE, ((592,295),(608,295),(600,283)))
            pygame.draw.rect(screen, WHITE, (597,385,6,20))
            pygame.draw.polygon(screen, WHITE, ((592,405),(608,405),(600,417)))

            #Beschriften der Pfeile für Bewegungsrichtungen
            textw = font.render("W", True, (255,255,255))
            texts = font.render("S", True, (255,255,255))
            texta = font.render("A", True, (255,255,255))
            textd = font.render("D", True, (255,255,255))
    
            screen.blit(textw, (590,260))
            screen.blit(texts, (595,420))
            screen.blit(textd, (671,339))
            screen.blit(texta, (516,339))

            #Text für betreten der Räume
            #textinfo = font.render("ENTER drücken um die Räume zu betreten", True, WHITE)
            #screen.blit(textinfo, (665, 650))

            textschießen = font.render("Schießen mit den PFEILTASTEN", True, WHITE)
            screen.blit(textschießen, (35,650))

            textinfo2 = font.render("Sammle diese Schlüssel", True, WHITE)
            screen.blit(textinfo2, (55,155))

        """---------------------------------------------------------------------"""



        """---------------------------------------------------------------------"""

        #Abfrage zum treffen auf Gegner oder Schlüssel
    
        key_hit_list = pygame.sprite.spritecollide(Spieler, current_Raum.key_list, True)
        gegner_hit_list = pygame.sprite.spritecollide(Spieler, current_Raum.enemy_sprites, False)
 
        # überprüfen der Kollisonsliste.

        for block in key_hit_list:
            score += 1
        
        for etwas in gegner_hit_list:
            leben -= 1
            Spieler.set(Koordinaten[0],Koordinaten[1])
            

        """---------------------------------------------------------------------"""



        """---------------------------------------------------------------------"""

        #Abfrage der Geschosse auf Treffer

        for bullet in bullet_list:

            #Abfrage nach treffen einer Wand
            wand_hit_list = pygame.sprite.spritecollide(bullet, current_Raum.wall_list, False)

            for wand in wand_hit_list:
                bullet_list.remove(bullet)

            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_Raum.enemy_sprites, False)

            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                enemy.gesundheit -= 1
                if enemy.gesundheit <= 0:
                    current_Raum.enemy_sprites.remove(enemy)
                

        """---------------------------------------------------------------------"""

        
        
        """---------------------------------------------------------------------"""

        # Timer und Sprites werden gezeichnent
        
        # Auswahl des Fonts:Schirftart, size, bold, italics
        font = pygame.font.SysFont('Calibri', 25, True, False)

        # --- Timer going up ---
        # Calculate total seconds
        total_seconds = frame_count // FRAME_RATE
 
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
        
        #TODO: maybe split seconds too?
 
        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 

        schluesselAnzeige = font.render("Schlüssel: " + str(score), True, GREEN)
        lebenAnzeige = font.render("Leben: " + str(leben), True, GREEN)
        zeitAnzeige = font.render(output_string, True, GREEN)
 
        screen.blit(schluesselAnzeige, [1000, 30])
        screen.blit(lebenAnzeige, [1000, 55])
        screen.blit(zeitAnzeige, [1000, 80])
 
        # Draw all the spites

        all_sprites_list.draw(screen)

        bullet_list.update() #die aktuelle Position aller Geschosse updaten
        bullet_list.draw(screen) #die Geschosse zeichenen
        
        current_Raum.wall_list.draw(screen) #die aktuellen Räume zeichnen

        current_Raum.key_list.draw(screen) # Schlüssel zeichnen

        current_Raum.enemy_sprites.draw(screen) # Gegner zeichnen

        """---------------------------------------------------------------------"""



        """---------------------------------------------------------------------"""

        # Abfrage und konstruktion der Endbildschirme. Game Over

        if leben <= 0 and done == False:

            pygame.mouse.set_visible(True)

            Spieler.change_x = 0
            Spieler.change_y = 0
            
            screen.fill(BLACK)
            font = pygame.font.SysFont("Calibri", 200, True, False)
            text = font.render("GAME OVER", True, RED)
            screen.blit(text, (82,150))

            # Play Again button
            pygame.draw.rect(screen,WHITE, [299,479,602,132])
            pygame.draw.rect(screen, BLUE, [300,480,600,130])

            # Quit button
            pygame.draw.rect(screen, WHITE, [50,560,200,80])
            pygame.draw.rect(screen, RED, [52,562,196,76])

            font2 = pygame.font.SysFont("Calibri", 100, True, False)
            text2 = font2.render("PLAY AGAIN!", True, WHITE)
            screen.blit(text2, (330,500))

            font_quit = pygame.font.SysFont("Calibri", 60, True, False)
            text_quit = font_quit.render("QUIT", True, WHITE)
            screen.blit(text_quit, (80,575))

            # Check if replay or quit button was clicked
            if replay_clicked:
                all_sprites_list.remove(Spieler)
                # Clear all bullet velocities
                bullet_list.empty()
                # Replay requested
                return True
            if quit_clicked:
                cleanup_quit()
                return False
                

        ###---------------------------------------------------------------------###

        if score == 5:

            if Daten == False: #einmaliges sichern des Highscores
                Punktzahl = 36000 - frame_count + 3000*leben
                Daten = True
                
                # Ask for username (simple text input)
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
                                if input_text.strip():
                                    username = input_text
                                else:
                                    username = "Player"
                                input_prompt = False
                            elif event.key == pygame.K_BACKSPACE:
                                input_text = input_text[:-1]
                            else:
                                if len(input_text) < 15:
                                    input_text += event.unicode
                    
                    # Draw input screen
                    screen.fill(BLACK)
                    font_large = pygame.font.SysFont("Calibri", 60, True, False)
                    font_input = pygame.font.SysFont("Calibri", 40, False, False)
                    
                    text_prompt = font_large.render("Enter your name:", True, WHITE)
                    text_input = font_input.render(input_text + "_", True, GREEN)
                    
                    screen.blit(text_prompt, (200, 300))
                    screen.blit(text_input, (200, 400))
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                # Save score with username
                if quit_requested:
                    break
                highscores = add_highscore(username, Punktzahl)

            
            Spieler.change_x = 0
            Spieler.change_y = 0
            
            pygame.mouse.set_visible(True)

            screen.fill(BLACK)

            # Replay button
            x_replay = 700
            y_replay = 400
            x_width_replay = 450
            y_width_replay = 250
            pygame.draw.rect(screen, WHITE, [x_replay,y_replay,x_width_replay,y_width_replay])
            pygame.draw.rect(screen, YELLOW, [x_replay+1,y_replay+1,x_width_replay-2,y_width_replay-2])
            
            #Texte
            x_pos = 60

            font = pygame.font.SysFont("Calibri", 220, True, False)
            text = font.render("Gewonnen!", True, GREEN)
            screen.blit(text, (x_pos,-40))

            fontnochmal = pygame.font.SysFont("Calibri", 90, True, False)
            textnochmal = fontnochmal.render("Nochmal?", True, BLACK)
            screen.blit(textnochmal, (x_replay+20, y_replay+80))

            fontscore = pygame.font.SysFont("Calibri", 50, True, True)
            textscore = fontscore.render("Deine Punktzahl: " + str(Punktzahl), True, WHITE)
            lifescore = fontscore.render("Leben: " + str(leben), True, WHITE)
            
            screen.blit(textscore, (x_pos,550))
            screen.blit(lifescore, (x_pos,600))
            
            # Display top 10 highscores
            font_small = pygame.font.SysFont("Calibri", 25, False, False)
            highscores = load_highscores()
            
            y_pos = 200
            title_text = font_small.render("TOP 10 HIGHSCORES:", True, YELLOW)
            screen.blit(title_text, (x_pos, y_pos))
            y_pos += 35
            
            for i, score_entry in enumerate(highscores[:10], 1):
                score_line = f"{i}. {score_entry['username']}: {score_entry['score']} ({score_entry['date']})"
                # mark score of the current run Bright red if it matches
                if score_entry['username'] == username and score_entry['score'] == Punktzahl:
                    text_line = font_small.render(score_line, True, RED)
                else:
                    text_line = font_small.render(score_line, True, GREEN)
                screen.blit(text_line, (x_pos, y_pos))
                y_pos += 30
           
            
            # Check if replay button was clicked
            if replay_clicked:
                all_sprites_list.remove(Spieler)
                # Clear all bullet velocities
                bullet_list.empty()
                # Replay requested
                return True
            
                      
        """---------------------------------------------------------------------"""

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
