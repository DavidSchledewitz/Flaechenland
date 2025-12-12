#!/usr/bin/python3

#Flächenland - Ein Softwareprojekt von David, Marius, Milena und Lasse, Q2a 2017
import pygame
import random

 
# Ein paar Farben definieren
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

bullet_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


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

        super().__init__(BLUE, 50, 50)

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
        super().__init__(WHITE, 4, 4)


        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        direct = dic

        if direct == "oben":
            self.rect.x = x + 23
            self.change_y = -12
        elif direct == "unten":
            self.rect.x = x + 23
            self.rect.y = y + 46
            self.change_y = 12
        elif direct == "links":
            self.rect.y =y + 23
            self.change_x = -12
        elif direct == "rechts":
            self.rect.x = x + 46
            self.rect.y = y + 23
            self.change_x = 12

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
        self.image = pygame.image.load("Kleiner_Key.png").convert()
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
        walls = [[0,0,550,20,WHITE],
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
                 [550,701,100,20]]

        for item in walls:
            wall = Wand(item[0],item[1],item[2],item[3])#,item[4])
            self.wall_list.add(wall)
        
        #Schlüssel erstellen
        KeyA = Schluessel(150,200)
        self.key_list.add(KeyA)

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
        walls = [[0,0,1200,20],
                 [0,680,1200,20],
                 [0,20,20,680],
                 [1180,20,20,280],
                 [1180,400,20,480],
                 [160,20,20,480],
                 [500,270,20,430],
                 [520,270,150,20],
                 [790,20,20,480],
                 [1201,300,20,100]]

        for item in walls:
            wall = Wand(item[0],item[1],item[2],item[3])
            self.wall_list.add(wall)

        #Schlüssel erstellen
        KeyL = Schluessel(70,335)
        self.key_list.add(KeyL)

        #Gegner erstellen
        Feinde = [[65,30,0,10,20,1180,20,500],
                  [710,270,0,-5,20,1180,270,680],
                  [195,40,0,-5,20,1180,40,660],
                  [275,195,0,-5,20,1180,40,660],
                  [355,350,0,-5,20,1180,40,660],
                  [435,505,0,-5,20,1180,40,660]]

        for item in Feinde:
            enemy = Gegner(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.enemy_sprites.add(enemy)

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
        walls = [[0,0,1200,20],
                 [0,680,1200,20],
                 [1180,20,20,680],
                 [0,20,20,280],
                 [0,400,20,280],
                 [800,410,20,280],
                 [800,20,20,270],
                 [-20,300,20,100]]

        for item in walls:
            wall = Wand(item[0],item[1],item[2],item[3])
            self.wall_list.add(wall)

        #Schlüssel erstellen
        KeyR = Schluessel(1125,335)
        self.key_list.add(KeyR)

        #Gegner erstellen
        Feinde = [[200,200,5,-5,20,800,20,680],
                  [200,450,5,5,20,800,20,680],
                  [920,325,0,5,20,1180,50,650]]

        for item in Feinde:
            enemy = Gegner(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.enemy_sprites.add(enemy)

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
        walls = [[0,680,1200,20],
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
                 [550,-20,100,20]]

        for item in walls:
            wall = Wand(item[0],item[1],item[2],item[3])
            self.wall_list.add(wall)

        #Schlüssel erstellen
        KeyU = Schluessel(580,440)
        self.key_list.add(KeyU)

        #Gegner erstellen
        Feinde = [[290,30,0,-5,20,1180,30,505],
                  [860,30,0,-5,20,1180,30,505],
                  [380,505,-5,5,380,820,370,680],
                  [770,505,5,-5,380,820,370,680]]
        
        for item in Feinde:
            enemy = Gegner(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.enemy_sprites.add(enemy)

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
        walls = [[0,0,1200,20],
                 [0, 20, 20, 660],
                 [1180,20,20,660],
                 [0,680,550,20],
                 [650,680,550,20],
                 [220,320,760,20],
                 [590,340,20,100],
                 [500,20,20,150],
                 [680,20,20,150],
                 [550,701,100,20]]

        for item in walls:
            wall = Wand(item[0],item[1],item[2],item[3])
            self.wall_list.add(wall)

        #Schlüssel erstellen
        KeyO = Schluessel(580,35)
        self.key_list.add(KeyO)

        #Gegner erstellen
        Feinde = [[640,360,5,0,630,1160,20,680],
                  [510,360,-5,0,40,570,20,680],
                  [20,135,-5,5,20,500,20,320],
                  [450,135,5,-5,20,500,20,320],
                  [700,135,-5,5,700,1180,20,320],
                  [1130,135,5,-5,700,1180,20,320]]

        for item in Feinde:
            enemy = Gegner(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
            self.enemy_sprites.add(enemy)
        
"""-----------------------------------------------------------------------------"""


def clear():
    for item in bullet_list:
        bullet_list.remove(item)


"""-----------------------------------------------------------------------------"""

# Beginn des Hauptprogramms 

def main():
    
    pygame.init()

    pygame.mouse.set_visible(False) #Verbergen des Mauszeigers

    size = (1200, 700) #Erstellen des Fensters des Spiels
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Flächenland")

    Spieler = Player(575, 325) #Erstellung der Spielfigur

    Koordinaten = [575,325] # Anfangskoordinaten

    Punktzahl = 0 # erstellen einer Variablen für die Punktzahl
    Daten = False # benötigt, damit highscore nur eunmal abgerufen wird

    # Loop until the user clicks the close button.
    done = False
 
    # Bildanzahl pro Sekunde festlegen
    clock = pygame.time.Clock()
    frame_count = 0
    frame_rate = 60
 
    score = 0
    leben = 5
    cooldown = 0
    

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
 
    # -------- Main Program Loop -----------
    while not done:


        """---------------------------------------------------------------------"""

        # Tastenabfragen
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                done = True

            # welche Taste wurde gedrückt, Bewegung anpassen
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_a:
                    Spieler.update(-5,0)
                elif event.key == pygame.K_d:
                    Spieler.update(5,0)
                elif event.key == pygame.K_w:
                    Spieler.update(0,-5)
                elif event.key == pygame.K_s:
                    Spieler.update(0,5)

                #Aufrufen der Bulletfunktion mit den Pfeiltasten ("schießen") schuss geschwindigkeit
                elif event.key == pygame.K_UP and cooldown <= 0:
                    bullet = Bullet("oben",Spieler.rect.x,Spieler.rect.y)
                    cooldown = 5
                elif event.key == pygame.K_DOWN and cooldown <= 0:
                    bullet = Bullet("unten",Spieler.rect.x,Spieler.rect.y)
                    cooldown = 5
                elif event.key == pygame.K_LEFT and cooldown <= 0:
                    bullet = Bullet("links",Spieler.rect.x,Spieler.rect.y)
                    cooldown = 5
                elif event.key == pygame.K_RIGHT and cooldown <= 0:
                    bullet = Bullet("rechts",Spieler.rect.x,Spieler.rect.y)
                    cooldown = 5

                
                
 
            # welche Taste wurde losgelassen, Bewegung unpassen
            elif event.type == pygame.KEYUP:
                
                if event.key == pygame.K_a:
                    Spieler.update(5,0)
                elif event.key == pygame.K_d:
                    Spieler.update(-5,0)
                elif event.key == pygame.K_w:
                    Spieler.update(0,5)
                elif event.key == pygame.K_s:
                    Spieler.update(0,-5)

        """---------------------------------------------------------------------"""
            


        # eigentlcihe Raumabfrage, testen auf Kollisionen mit Wänden im aktuellen Raum
        Spieler.move(current_Raum.wall_list)

        current_Raum.enemy_sprites.update()

        
        """---------------------------------------------------------------------"""

        # Türenabfrage
        # Prinzip: die neue Klasse als aktiven Raum setzen und den Anfangspunkt definieren
        # Abfrage für Entertaste im Bereich der Tür
        
        if Spieler.rect.x in range(550,601) and Spieler.rect.y in range(0,21) and current_Raum_Number == 0:# and event.key == pygame.K_RETURN: # Obenbeteten
            current_Raum_Number = 4
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,615]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if Spieler.rect.x in range(550,601) and Spieler.rect.y in range(629,700) and current_Raum_Number == 0:# and event.key == pygame.K_RETURN: # Untenbetreten
            current_Raum_Number = 3
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,35]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if Spieler.rect.x in range(0,21) and Spieler.rect.y in range(300,351) and current_Raum_Number == 0:# and event.key == pygame.K_RETURN: # Linksbetreten
            current_Raum_Number = 1
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [1115,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()
            
        if Spieler.rect.x in range(1129,1200) and Spieler.rect.y in range(300,351) and current_Raum_Number == 0:# and event.key == pygame.K_RETURN: # Rechtsbetreten
            current_Raum_Number = 2
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [35,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()



        # Zurück zum Start
        

        if Spieler.rect.x in range(1129,1200) and Spieler.rect.y in range(300,351) and current_Raum_Number == 1:# and event.key == pygame.K_RETURN: #von links zurück
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [35,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if Spieler.rect.x in range(0,21) and Spieler.rect.y in range(300,351) and current_Raum_Number == 2:# and event.key == pygame.K_RETURN: #von rechts zurück
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [1115,325]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if Spieler.rect.x in range(550,601) and Spieler.rect.y in range(629,700) and current_Raum_Number == 4:# and event.key == pygame.K_RETURN: #von oben zurück
            current_Raum_Number = 0
            current_Raum = Räume[current_Raum_Number]
            Koordinaten = [575,35]
            Spieler.set(Koordinaten[0],Koordinaten[1])
            clear()

        if Spieler.rect.x in range(550,601) and Spieler.rect.y in range(0,21) and current_Raum_Number == 3:# and event.key == pygame.K_RETURN: #von unten zurück
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
        total_seconds = frame_count // frame_rate
 
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
 
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

            pygame.draw.rect(screen,WHITE, [299,479,602,132])
            pygame.draw.rect(screen, BLUE, [300,480,600,130])

            font2 = pygame.font.SysFont("Calibri", 100, True, False)
            text2 = font2.render("PLAY AGAIN!", True, WHITE)
            screen.blit(text2, (330,500))

            #Funkton zum Neustart bei derAuswahl der Schaltfläche
            pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if pos[0] in range (299,901) and pos[1] in range (479,611) and mouse[0] == True:
                all_sprites_list.remove(Spieler)
                #pygame.quit()
                done = True
                main()
                

        ###---------------------------------------------------------------------###

        if score == 5:

            if Daten == False: #einmaliges sichern des Highscores
                Punktzahl = 36000 - frame_count + 3000*leben
                Daten = True

                # Abrufen des bisherigen Highscores
                high_score_file = open("highscore.txt", "r")
                highscore = int(high_score_file.read())
                high_score_file.close

            
            Spieler.change_x = 0
            Spieler.change_y = 0
            
            pygame.mouse.set_visible(True)

            screen.fill(BLACK)

            #Replaybutton
            pygame.draw.rect(screen, WHITE, [699,399,402,252])
            pygame.draw.rect(screen, YELLOW, [700,400,400,250])
            
            #Texte
            font = pygame.font.SysFont("Calibri", 220, True, False)
            text = font.render("Gewonnen!", True, GREEN)
            screen.blit(text, (60,100))

            fontnochmal = pygame.font.SysFont("Calibri", 90, True, False)
            textnochmal = fontnochmal.render("Nochmal?", True, WHITE)
            screen.blit(textnochmal, (720,490))

            fontscore = pygame.font.SysFont("Calibri", 70, True, True)
            textscore = fontscore.render("Punktzahl: " + str(Punktzahl), True, WHITE)
            texthighscore = fontscore.render("Highscore: " + str(highscore), True, WHITE)
            lifescore = fontscore.render("Leben: " + str(leben), True, WHITE)
            textneu = fontscore.render("Neuer Highscore!!!", True, WHITE)
            
            screen.blit(textscore, (60,500))
            screen.blit(texthighscore, (60,400))
            screen.blit(lifescore, (60,300))
            if Punktzahl > highscore:
                screen.blit(textneu, (60, 600))

                # Speichern des neuen Highscores
                file = open("highscore.txt","w")
                file.truncate()
                file.write(str(Punktzahl))
                file.close()
           
            
            #Funkton zum Neustart bei derAuswahl der Schaltfläche
            pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if pos[0] in range (699,1001) and pos[1] in range (399,651) and mouse[0] == True:
                all_sprites_list.remove(Spieler)
                #pygame.quit()
                done = True
                main()
                      
        """---------------------------------------------------------------------"""

        # Erhöhen des timers/bildanzahl
        frame_count += 1
        cooldown -= 1
        clock.tick(60)
    
        # Alles gezeichnete darstellen.
        pygame.display.flip()
 
    
 
    pygame.quit()




if __name__ == "__main__":
    main()
