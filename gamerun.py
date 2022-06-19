import random
import pygame
import time
import tutorial as t

import numpy as np

show_game = False
gamebg = None
lasersound = None
hitsound = None
clock = pygame.time.Clock()

frames = 0
totaltestseconds = 0

screenbreite = 700
screenhoehe = 550
shootloop = 0
alienkills = 0
level = 1
spaceshipkills = 0
colorcounter = 0
timee = ''
ru = True
# pausebutton=False
show1 = True
spawnaliens = True
addalien = False

# TODO remove powerups
powerups = [['double shooting ability', False, False, 'allows you to have twice as much lasers as normal on screen'],
            ['half alien velocity', False, False, 'slows down the aliens or the spaceship'],
            ['double laser damage', False, False, 'your lasers do twice as much damage as normal'],
            ['double cannons', False, False, 'allows you to have two cannons on your spaceship'],
            ['Health Boost', False, False, 'replenishes your health by 1/5']]

holdingpowerup = False
usepowerup = False
poweruploop = 0

aliennumber = 2
alienhealth = 10
alienlaserdamage = 1
alienvelocity = 1.3

yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
red = (255, 0, 0)
green = (0, 222, 0)

color = green


class Spaceship:

    def __init__(self):
        self.x = 150
        self.y = 490
        self.vel = 5
        self.breite = 110
        self.hoehe = 50
        self.health = 50
        self.hitbox = (self.x, self.y, self.breite, self.hoehe)
        # self.visible=True

    def draw(self, win):
        global powerups
        global usepowerup

        if powerups[4][2]:
            self.health += 40
            if self.health > 200:
                self.health = 200
            powerups[4][2] = False
            usepowerup = False

        if show_game:
            pygame.draw.rect(win, grey, (self.x + 20, self.y, 70, 50))
            pygame.draw.rect(win, yellow, (self.x + 90, self.y + 15, 20, 35))
            pygame.draw.rect(win, yellow, (self.x, self.y + 15, 20, 35))

            if powerups[3][2]:
                pygame.draw.rect(win, white, (self.x + round(self.breite / 2) + 5, self.y - 20, 10, 20))
                pygame.draw.rect(win, white, (self.x + round(self.breite / 2) - 15, self.y - 20, 10, 20))

            else:
                pygame.draw.rect(win, white, (self.x + round(self.breite / 2) - 5, self.y - 20, 10, 20))

        self.hitbox = (self.x, self.y, self.breite, self.hoehe)

    def fire(self):
        global powerups
        if powerups[0][2]:
            le = 10
        else:
            le = 5
        if len(lasers) < le or True:  # TODO: decide if keep powerups or eliminate them
            # if show_game:
            #
            #     if men.soundchoose.get_tof():
            #         lasersound.set_volume(men.soundbar.get_Volume())
            #         lasersound.play()

            if powerups[3][2]:
                lasers.append(Laser(self.x + round(self.breite / 2) + 9, 470, yellow))
                lasers.append(Laser(self.x + round(self.breite / 2) - 11, 470, yellow))
            else:
                lasers.append(Laser(self.x + round(self.breite / 2) - 1, 470, yellow))

    def drawHealthBar(self, win):
        font1 = pygame.font.SysFont('comicsans', 30)
        text = font1.render('Health:', 1, white)
        win.blit(text, (5, 5))
        textb = font1.render(str(self.health), 1, white)
        win.blit(textb, (210, 5))
        if self.health > 0:
            pygame.draw.rect(win, red, (15 + text.get_width(), round(text.get_height() / 2), round(self.health / 2), 10))

    def hit(self):
        global alienlaserdamage
        self.health -= alienlaserdamage
        if show_game:
            hitsound.play()


class EnemyAlien:

    walkRight = [pygame.image.load('data/R1E.png'), pygame.image.load('data/R2E.png'),
                 pygame.image.load('data/R3E.png'), pygame.image.load('data/R4E.png'),
                 pygame.image.load('data/R5E.png'),
                 pygame.image.load('data/R6E.png'), pygame.image.load('data/R7E.png'),
                 pygame.image.load('data/R8E.png'), pygame.image.load('data/R9E.png'),
                 pygame.image.load('data/R10E.png'),
                 pygame.image.load('data/R11E.png')]

    walkLeft = [pygame.image.load('data/L1E.png'), pygame.image.load('data/L2E.png'),
                pygame.image.load('data/L3E.png'), pygame.image.load('data/L4E.png'),
                pygame.image.load('data/L5E.png'),
                pygame.image.load('data/L6E.png'), pygame.image.load('data/L7E.png'),
                pygame.image.load('data/L8E.png'), pygame.image.load('data/L9E.png'),
                pygame.image.load('data/L10E.png'), pygame.image.load('data/L11E.png')]

    def __init__(self, x, y, health, vel):
        self.x = x
        self.y = y
        self.health = health
        self.path = [64, 634]
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.breite = self.hitbox[2]
        self.vel = vel
        # self.visible=True
        self.lasercount = 0

    def move(self):
        global powerups

        if self.vel > 0:
            if powerups[1][2]:
                e = self.vel / 2
            else:
                e = self.vel
            if self.x + self.vel < self.path[1] - self.hitbox[2]:
                self.x += e
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if powerups[1][2]:
                e = self.vel / 2
            else:
                e = self.vel
            if self.x - self.vel > self.path[0]:
                self.x += e
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def draw(self, win):
        self.move()
        # if self.visible:
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            if show_game:
                win.blit(self.walkRight[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1
        else:
            if show_game:
                win.blit(self.walkLeft[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1

        if self.vel > 0:
            self.hitbox = (self.x + 14, self.y + 2, 31, 57)
        else:
            self.hitbox = (self.x + 23, self.y + 2, 31, 57)
        if show_game:
            self.drawHealthBar(win)

        self.fire()

    def drawHealthBar(self, win):
        y = self.hitbox[1] - 10
        healthfont = pygame.font.SysFont('arial', 20)
        text = healthfont.render(str(self.health), 1, red)
        win.blit(text, (self.hitbox[0] + (self.hitbox[2] / 2), y))

    def fire(self):
        if self.lasercount == 0:
            # if show_game:
            #     if men.soundchoose.get_tof():
            #         lasersound.set_volume(men.soundbar.get_Volume())
            #         lasersound.play()
            enemy_lasers.append(Laser(self.x + round(self.breite / 2) + 15, self.y + 8, green))
            self.lasercount = 1

        else:
            self.lasercount += 1
            if self.lasercount > 66:
                self.lasercount = 0

    def hit(self):
        if show_game:
            hitsound.play()

        global powerups
        if powerups[2][2]:
            self.health -= 2
        else:
            self.health -= 1


class Laser:

    def __init__(self, x, y, laser_color):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 30
        self.color = laser_color
        self.vel = 4
        # self.visible=True

    def draw(self, win):
        if show_game:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class EnemySpaceship:

    def __init__(self):
        self.x = 150
        self.y = 70
        self.breite = 110
        self.vel = 3
        self.hoehe = 50
        self.health = 50
        self.path = [64, 634]
        self.hitbox = (self.x, self.y, self.breite, self.hoehe)
        self.lasercount = 0
        self.showrage = True

    def draw(self, win):
        global colorcounter
        global color

        if self.health < 26:
            colorcounter += 1
            if colorcounter > 30:
                colorcounter = 0
                if color == green:
                    color = red
                else:
                    color = green

        else:
            color = green

        if show_game:
            pygame.draw.rect(win, grey, (self.x + 20, self.y, 70, 50))
            # if color == red:
            #     ef = pygame.font.SysFont('comicsansms', 35)
            #     text = ef.render('2x', 1, red)
            #     win.blit(text, (self.x + 33, self.y - 2))
            pygame.draw.rect(win, color, (self.x + 90, self.y, 20, 35))
            pygame.draw.rect(win, color, (self.x, self.y, 20, 35))
            pygame.draw.rect(win, white, (self.x + round(self.breite / 2) - 5, self.y + 50, 10, 20))

        self.hitbox = (self.x, self.y, self.breite, self.hoehe)

        if show_game:
            self.drawHealthBar(win)
        self.move()
        self.fire()

    def move(self):
        if self.vel > 0:
            if powerups[1][2]:
                self.vel = 1.5
            else:
                self.vel = 3
            if self.x + self.vel < self.path[1] - self.hitbox[2]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if powerups[1][2]:
                self.vel = -1.5
            else:
                self.vel = -3
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

    def fire(self):
        # if self.health > 25:
        #     seq = 66
        # else:
        #     seq = 33
        seq = 33
        if self.lasercount == 0:
            # if show_game:
            #     if men.soundchoose.get_tof():
            #         lasersound.set_volume(men.soundbar.get_Volume())
            #         lasersound.play()

            if self.vel > 0:
                laserx = self.x + round(self.breite / 2) + 13
            else:
                laserx = self.x + round(self.breite / 2) - 13
            enemy_lasers.append(Laser(laserx, self.y + 8, green))
            self.lasercount = 1

        else:
            self.lasercount += 1
            if self.lasercount > seq:
                self.lasercount = 0

    def hit(self):
        if show_game:
            hitsound.play()
        self.health -= 1

    def drawHealthBar(self, win):
        y = self.hitbox[1] - 10
        healthfont = pygame.font.SysFont('arial', 20)
        text = healthfont.render(str(self.health), 1, red)
        win.blit(text, (round((self.hitbox[0] + (self.hitbox[2] / 2)) - round(text.get_width() / 2)), y - 10))


###########################################################################################
###########################################################################################

def showLevel(win, level, msg):
    lvlfont = pygame.font.SysFont('comicsans', 50)
    text = lvlfont.render('Level: ' + str(level), 1, white)
    win.blit(text, (350 - round(text.get_width() / 2), 275))

    msgfont = pygame.font.SysFont('comicsans', 30)
    text = msgfont.render(msg, 1, white)
    win.blit(text, (350 - round(text.get_width() / 2), 315))

    pygame.display.update()
    time.sleep(2)


def generateLevel(win, number):
    global powerups
    global addalien
    global level
    global aliennumber
    global alienhealth
    global alienlaserdamage
    global alienvelocity
    global spawnaliens
    global alienkills
    global spaceshipkills
    # global seccount
    global totaltestseconds

    global levelcounter

    if number == 1:
        global level
        level = 0
        alienkills = 0
        spaceshipkills = 0
        levelcounter = 1
        global battleship
        global show1
        show1 = True
        battleship = Spaceship()
        global addalien
        addalien = False
        aliennumber = 2
        alienhealth = 10
        alienlaserdamage = 2
        alienvelocity = 1.3

    if levelcounter == 2:  # TODO maybe all'inizio semplificare i livelli?
        alienhealth += 2
        if show_game:
            showLevel(win, level + 1, 'Alien health +2')
    elif levelcounter == 3:
        alienlaserdamage += 1
        if show_game:
            showLevel(win, level + 1, 'Alien laser damage +1')
    elif levelcounter == 4:
        alienhealth += 2
        alienlaserdamage += 1
        # alienvelocity += 0.1
        if show_game:
            showLevel(win, level + 1, 'Alien health +2 and Alien laser damage +1')
    elif levelcounter == 5:
        if show_game:
            showLevel(win, level + 1, 'Enemy spaceship attacks')
        levelcounter = 0
        spawnaliens = False
    elif levelcounter == 1 and number != 1:
        for p in powerups:
            if p[1]:
                p[1] = False
        a = random.randint(0, len(powerups) - 1)
        powerups[a][1] = True

        if show_game:
            newpfont = pygame.font.SysFont('comicsans', 50)
            newtext = newpfont.render('New Powerup: ' + powerups[a][0], 1, white)
            win.blit(newtext, (350 - round(newtext.get_width() / 2), 225))

            exfont = pygame.font.SysFont('comicsans', 30)
            textex = exfont.render(powerups[a][3], 1, white)
            win.blit(textex, (350 - round(textex.get_width() / 2), 295))

            pygame.display.update()
            # print("sleep")
            # time.sleep(3)
        redrawGameWindow(win)

        if addalien:
            # aliennumber += 1 # TODO: removed temporarily
            if show_game:
                showLevel(win, level + 1, 'Alien number +1')
            addalien = False
        else:
            alienlaserdamage += 2
            if show_game:
                showLevel(win, level + 1, 'Alien laser damage +2')
            addalien = True

    if spawnaliens:
        alieny = 70
        alienx = 64
        for e in range(aliennumber):
            aliens.append(EnemyAlien(alienx, alieny, alienhealth, alienvelocity))
            # alieny += 72 # TODO: removed temporarily
            if alienx == 64:
                alienx = 634
            elif alienx == 634:
                alienx = 349
            else:
                alienx = 64

    else:
        enemy_spaceships.append(EnemySpaceship())
        spawnaliens = True
    levelcounter += 1
    level += 1


###########################################################################################
###########################################################################################

# def gameover(win):
#     global alienkills
#     global spaceshipkills
#     global totaltestseconds
#     global level
#     global aliens
#     global lasers
#     global enemy_lasers
#     global timee
#     pygame.mixer.music.stop()
#     helplevel=level

#     ptime=calculateTime()
#     if int(ptime[1])<10:
#         timee=ptime[0]+':0'+ptime[1]
#     else:
#         timee=ptime[0]+':'+ptime[1]

#     generateLevel(win,1)
#     print(str(helplevel))
#     print(str(s.readlevel()))
#     if helplevel>s.readlevel():
#         s.save(helplevel,alienkills,spaceshipkills,timee,totaltestseconds)
#         highscoreloop=True
#         hslo=0
#         ybutton=370
#     elif helplevel==s.readlevel() and totaltestseconds>s.readseconds():
#         s.save(helplevel,alienkills,spaceshipkills,timee,totaltestseconds)
#         highscoreloop=True
#         hslo=0
#         ybutton=370
#     else:
#         highscoreloop=False
#         ybutton=350

#     f=True
#     g=True
#     h=True
#     while f:
#         try:
#             aliens.pop()
#         except:
#             f=False
#     while g:
#         try:
#             lasers.pop()
#         except:
#             g=False
#     while h:
#         try:
#             enemylasers.pop()
#         except:
#             h=False

#     gaov=True
#     while gaov:
#         clock.tick(30)
#         for event in pygame.event.get():
#             if event.type==pygame.QUIT:
#                 ptime=calculateTime()
#                 if int(ptime[1])<10:
#                     timee=ptime[0]+':0'+ptime[1]
#                 else:
#                     timee=ptime[0]+':'+ptime[1]
#                 return 0
#         pygame.draw.rect(win,yellow,(50,75,600,400))
#         pygame.draw.rect(win,black,(60,85,580,380))

#         gameoverfont=pygame.font.SysFont('comicsansms',50)
#         text=gameoverfont.render('Game Over!',1,yellow)
#         win.blit(text,(350-round(text.get_width()/2),80))

#         statfont=pygame.font.SysFont('comicsans',30)

#         text=statfont.render('Level: '+str(helplevel),1,white)
#         win.blit(text,(350-round(text.get_width()/2),160))

#         text=statfont.render('Aliens killed: '+str(alienkills),1,white)
#         win.blit(text,(350-round(text.get_width()/2),190))

#         text=statfont.render('Enemy spaceships destroyed: '+str(spaceshipkills),1,white)
#         win.blit(text,(350-round(text.get_width()/2),220))

#         if highscoreloop:
#             hslo+=1
#             if hslo<15:
#                 highfont=pygame.font.SysFont('comicsansms',40)
#                 text=highfont.render('New Highscore!',1,yellow)
#                 win.blit(text,(350-round(text.get_width()/2),290))
#             elif hslo==30:
#                 hslo=0

#         text=statfont.render('Survived time: '+timee,1,white)
#         win.blit(text,(350-round(text.get_width()/2),250))

#         exbutton=t.button(win,'Main Menu',250,ybutton,200,50,yellow,black,yellow)
#         if exbutton:
#             return 1

#         pygame.display.update()

def calculateTime():
    global totaltestseconds
    minutes = totaltestseconds // 60
    seconds = totaltestseconds % 60

    return [str(minutes), str(seconds)]


# def pause(win):
#     global timee
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             ptime=calculateTime()
#             if int(ptime[1])<10:
#                 timee=ptime[0]+':0'+ptime[1]
#             else:
#                 timee=ptime[0]+':'+ptime[1]
#             return 0

#     pygame.draw.rect(win,yellow,(150,115,400,320))
#     pygame.draw.rect(win,black,(160,125,380,300))

#     paufont=pygame.font.SysFont('comicsansms',50)
#     text=paufont.render('Paused',1,yellow)
#     win.blit(text,(350-round(text.get_width()/2),120))

#     notefont=pygame.font.SysFont('comicsansms',15)
#     text=notefont.render('NOTE: if you quit, you can go back to the current',1,yellow)
#     win.blit(text,(170,320))
#     text=notefont.render('save by just starting the game via the main menu.',1,yellow)
#     win.blit(text,(170,340))
#     text=notefont.render('If you close the whole game with an unfinished save,',1,yellow)
#     win.blit(text,(170,360))
#     text=notefont.render('it will be saved regularly but you wont be able to',1,yellow)
#     win.blit(text,(170,380))
#     text=notefont.render('finish it.',1,yellow)
#     win.blit(text,(170,400))

#     resumebutton=t.button(win,'Resume',250,200,200,50,yellow,black,yellow)
#     if resumebutton:
#         return 1

#     quitbutton=t.button(win,'Quit',250,260,200,50,yellow,black,yellow)
#     if quitbutton:
#         ptime=calculateTime()
#         if int(ptime[1])<10:
#             timee=ptime[0]+':0'+ptime[1]
#         else:
#             timee=ptime[0]+':'+ptime[1]
#         return 0

#     pygame.display.update()

###########################################################################################
###########################################################################################

def redrawGameWindow(win):
    global powerups
    global battleship
    global alienkills
    global spaceshipkills
    # global pausebutton
    global holdingpowerup
    global usepowerup
    global poweruploop

    if show_game:
        win.blit(gamebg, (0, 0))

        lvlfont = pygame.font.SysFont('comicsans', 30)
        text = lvlfont.render('Level: ' + str(level), 1, white)
        win.blit(text, (350 - round(text.get_width() / 2), 5))

        text = lvlfont.render('Powerups: ', 1, white)
        win.blit(text, (5, 25))

        for powerup in powerups:
            if powerup[1]:
                textp = lvlfont.render(powerup[0], 1, white)
                win.blit(textp, (text.get_width() + 5, 25))
                holdingpowerup = True

        if holdingpowerup:
            usebutton = t.button(win, 'Use', 5 + text.get_width() + textp.get_width() + 20, 25, 45, 20, yellow, black, yellow)
            if usebutton:
                holdingpowerup = False
                usepowerup = True

        if usepowerup:
            for powerup in powerups:
                if powerup[1]:
                    powerup[1] = False
                    powerup[2] = True

        for powerup in powerups:
            if powerup[2]:
                textp = lvlfont.render(powerup[0], 1, white)
                win.blit(textp, (text.get_width() + 5, 25))
                poweruploop += 1
                if poweruploop == 720:
                    poweruploop = 0
                    powerup[2] = False
                    usepowerup = False

        if not holdingpowerup and not usepowerup:
            textp = lvlfont.render('None', 1, white)
            win.blit(textp, (text.get_width() + 5, 25))

    # pausebutton=t.button(win,'Pause',625,10,65,30,yellow,black,yellow)

    # keys=pygame.key.get_pressed()
    # if pausebutton or keys[pygame.K_ESCAPE]:
    #     pause(win)

    for laser in lasers:
        laser.draw(win)

    for laser in enemy_lasers:
        laser.draw(win)

    for alien in aliens:
        if alien.health > 0:
            alien.draw(win)
        # else:
        #     # print("pop aliens")
        #     aliens.pop(aliens.index(alien)) # TODO: why pop aliens here?
        #     alienkills+=1

    for v in enemy_spaceships:
        if v.health > 0:
            v.draw(win)
        # else:
        #     # print("pop enemyspaceships")
        #     enemyspaceships.pop()
        #     spaceshipkills+=1

    # if battleship.visible:    
    battleship.draw(win)
    if show_game:
        battleship.drawHealthBar(win)

        pygame.display.update()


battleship = Spaceship()
lasers = []
enemy_lasers = []
aliens = []
enemy_spaceships = []
tick_time = time.time()
K_LEFT, K_RIGHT, K_SPACE = 1073741904, 1073741903, 32
battleship_healths = []

def run(win, net):
    global alienkills
    global spaceshipkills
    global battleship
    global enemy_spaceships
    global aliens
    global lasers
    global enemy_lasers
    global ru
    # global seccount
    # global pausebutton
    global frames
    global totaltestseconds
    global timee
    global keys
    global battleship_healths

    frames += 1

    if frames > 1000000:
        print("game stopped")
        return 0 # stop the game, prevent training get stuck


    if show_game:
        clock.tick(200)

    # seccount+=1
    # if seccount==60:
    #     totaltestseconds+=1
    #     seccount=0

    redrawGameWindow(win)

    global show1
    if show1:
        battleship_healths.append(battleship.health)
        alienkills = 0
        spaceshipkills = 0
        generateLevel(win, 1)
        if show_game:
            showLevel(win, level, '')
        totaltestseconds = 0
        # seccount=1
        show1 = False

    global shootloop
    if show_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ptime = calculateTime()
                if int(ptime[1]) < 10:
                    timee = ptime[0] + ':0' + ptime[1]
                else:
                    timee = ptime[0] + ':' + ptime[1]
                return 0

    if frames % 10 == 0:
        # aliens_xy = [(999999999, 999999999), (999999999, 999999999)]
        # for i, alien in enumerate(aliens):
        #     aliens_xy[i] = (alien.x, alien.y)

        # threat_lasers = [(999999999, 999999999), (999999999, 999999999)]
        # i = 0
        # for laser in enemy_lasers:
        #     if battleship.hitbox[0]-10 < laser.x < battleship.hitbox[0] + battleship.hitbox[2] + 10:
        #         if len(threat_lasers) == i:
        #             threat_lasers.append((999999999, 999999999))
        #         threat_lasers[i] = [battleship.y - (laser.y + laser.height), battleship.x - laser.x]
        #         i += 1
        # threat_lasers.sort(key=lambda x: x[0])

        # enemy_spaceships_xy = [(999999999, 999999999)]
        # for i, enemy_spaceship in enumerate(enemy_spaceships):
        #     enemy_spaceships_xy[i] = (enemy_spaceship.x, enemy_spaceship.y)


        # outputs = net.activate((battleship.health,
        #                         battleship.x, screenbreite - battleship.breite - battleship.x,
        #                         # aliens_xy[0][0]-battleship.x, aliens_xy[0][1]-battleship.y, 
        #                         # aliens_xy[1][0]-battleship.x, aliens_xy[1][1]-battleship.y, 
        #                         # enemy_spaceships_xy[0][0]-battleship.x, enemy_spaceships_xy[0][1]-battleship.y,
        #                         threat_lasers[0][0], threat_lasers[0][1],
        #                         threat_lasers[1][0], threat_lasers[1][1],
        #                         ))

        # keys = {
        #     K_LEFT: outputs[0]>0.5,
        #     K_RIGHT: outputs[0]<=0.5,
        #     K_SPACE: True
        # }


        aliens_x = [0, 0, 0]
        for a, alien in enumerate(aliens):
            if a < 3:
                aliens_x[a] = alien.x

        laser_x = [0, 0, 0, 0, 0, 0]
        laser_y = [0, 0, 0, 0, 0, 0]
        # Give as input the 5 closer enemy lasers
        enemy_lasers_with_distance = [(laser, pow(pow(laser.x - battleship.x, 2) + pow(laser.y - battleship.y, 2), 1/2)) for laser in enemy_lasers]
        enemy_lasers_with_distance.sort(key=lambda x: x[1])
        for e, enemy_laser_with_distance in enumerate(enemy_lasers_with_distance):
            if e < 6:
                laser_x[e] = enemy_laser_with_distance[0].x
                laser_y[e] = enemy_laser_with_distance[0].y

        enemy_spaceships_x = [0]
        for s, enemy_spaceship in enumerate(enemy_spaceships):
            if s < 1:
                enemy_spaceships_x[s] = enemy_spaceship.x

        # TODO pass to the network relevant information as input
        outputs = net.activate((battleship.x, battleship.vel, battleship.health,
                                aliens_x[0], aliens_x[1],
                                laser_x[0], laser_y[0],
                                laser_x[1], laser_y[1],
                                laser_x[2], laser_y[2],
                                laser_x[3], laser_y[3],
                                laser_x[4], laser_y[4],
                                laser_x[5], laser_y[5],
                                enemy_spaceships_x[0]))

        i = np.argmax(np.array(outputs))
        keys = {
            K_LEFT: i == 0 or i == 1,
            K_RIGHT: i == 4 or i == 5,
            K_SPACE: i == 1 or i == 3 or i == 5
        }

    if keys[K_LEFT]:
        if battleship.x > battleship.vel:
            battleship.x -= battleship.vel

    if keys[K_RIGHT]:
        if battleship.x < screenbreite - battleship.breite - battleship.vel:
            battleship.x += battleship.vel

    if keys[K_SPACE]:
        if shootloop == 0:
            battleship.fire()
            shootloop = 1

    if shootloop > 0:
        shootloop += 1
    if shootloop > 14:
        shootloop = 0

    for laser in lasers:
        if laser.y > 40:
            laser.y -= laser.vel

        else:
            lasers.pop(lasers.index(laser))

        for e in enemy_lasers:
            xx = e.x - laser.x
            yy = e.y - laser.y

            if 5 > xx > -5 and 5 > yy > -5:
                enemy_lasers.pop(enemy_lasers.index(e))
                lasers.pop(lasers.index(laser))

    for alien in aliens:
        # print("alien:", alien.x, alien.y, alien.health)
        # if alien.visible:
        for laser in lasers:
            if alien.hitbox[1] + alien.hitbox[3] > laser.y > alien.hitbox[1]:
                if alien.hitbox[0] < laser.x < alien.hitbox[0] + alien.hitbox[2]:
                    alien.hit()
                    lasers.pop(lasers.index(laser))
                    # print("hit alien")
            elif alien.hitbox[1] + alien.hitbox[3] > laser.y + laser.height > alien.hitbox[1]:
                if alien.hitbox[0] < laser.x < alien.hitbox[0] + alien.hitbox[2]:
                    alien.hit()
                    lasers.pop(lasers.index(laser))
                    # print("hit alien")

    for v in enemy_spaceships:
        # print("enemy spaceships:", v.x, v.y, v.health)
        for laser in lasers:
            if v.hitbox[1] + v.hitbox[3] > laser.y > v.hitbox[1]:
                if v.hitbox[0] < laser.x < v.hitbox[0] + v.hitbox[2]:
                    v.hit()
                    lasers.pop(lasers.index(laser))
                    # print("hit enemy spaceship")
            elif v.hitbox[1] + v.hitbox[3] > laser.y + laser.height > v.hitbox[1]:
                if v.hitbox[0] < laser.x < v.hitbox[0] + v.hitbox[2]:
                    v.hit()
                    lasers.pop(lasers.index(laser))
                    # print("hit enemy spaceship")

    for laser in enemy_lasers:
        if battleship.hitbox[1] + battleship.hitbox[3] > laser.y + laser.height > battleship.hitbox[1]:
            if battleship.hitbox[0] < laser.x < battleship.hitbox[0] + battleship.hitbox[2]:
                battleship.hit()
                enemy_lasers.pop(enemy_lasers.index(laser))
                # print("hit battleship")

    for laser in enemy_lasers:
        if laser.y < 470:
            laser.y += laser.vel
        else:
            enemy_lasers.pop(enemy_lasers.index(laser))

    for alien in aliens:
        if alien.health <= 0:
            # print("alien killed")
            aliens.pop(aliens.index(alien))
            alienkills += 1

    for v in enemy_spaceships:
        if v.health <= 0:
            # print("enemy spaceship killed")
            enemy_spaceships.pop()
            spaceshipkills += 1

    # print("battleship:", battleship.x, battleship.y, battleship.health)
    if battleship.health <= 0:
        # if not ru:
        #     go = gameover(win)
        #     if go == 0 or go == 1:
        #         ru = True
        #         return go
        # ru = False
        # print("game over")
        return 0

    if len(aliens) == 0 and len(enemy_spaceships) == 0:
        lasers = []
        enemy_lasers = []
        battleship.x = 150

        # if levelcounter == 4: 
        #     if battleship.health == 50:
        #         print("-----------------------------------------------------------")
        #     return 0
        redrawGameWindow(win)
        generateLevel(win, 0)
        battleship_healths.append(battleship.health)


    # keys=pygame.key.get_pressed()
    # if pausebutton or keys[pygame.K_ESCAPE]:
    #     pausebutton=False
    #     pau=True
    #     while pau:
    #         g=pause(win)
    #         if g==1:
    #             pau=False
    #         elif g==0:
    #             pau=False
    #             return 1

    return 1