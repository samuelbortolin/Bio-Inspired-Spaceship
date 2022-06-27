import pygame
import time
import numpy as np

from gp_train import A, B, D, E, F

show_game = False
clock = pygame.time.Clock()
frames = 0

game_background = None
screen_width = 700
screen_height = 550
shoot_loop = 0
alien_kills = 0
level = 1
spaceship_kills = 0
show1 = True
spawn_aliens = True
add_alien = False

alien_number = 2
alien_health = 10
alien_laser_damage = 1

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
        self.width = 110
        self.height = 50
        self.health = 50
        self.hit_box = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        if show_game:
            pygame.draw.rect(win, grey, (self.x + 20, self.y, 70, 50))
            pygame.draw.rect(win, yellow, (self.x + 90, self.y + 15, 20, 35))
            pygame.draw.rect(win, yellow, (self.x, self.y + 15, 20, 35))
            pygame.draw.rect(win, white, (self.x + round(self.width / 2) - 5, self.y - 20, 10, 20))

        self.hit_box = (self.x, self.y, self.width, self.height)

    def fire(self):
        lasers.append(Laser(self.x + round(self.width / 2) - 1, 470, yellow))

    def draw_health_bar(self, win):
        font1 = pygame.font.SysFont('comicsans', 30)
        text = font1.render('Health:', 1, white)
        win.blit(text, (5, 5))
        textb = font1.render(str(self.health), 1, white)
        win.blit(textb, (210, 5))
        if self.health > 0:
            pygame.draw.rect(win, red, (15 + text.get_width(), round(text.get_height() / 2), round(self.health * 1.5), 10))

    def hit(self):
        global alien_laser_damage
        self.health -= alien_laser_damage


class EnemyAlien:

    walkRight = [pygame.image.load('data/R1E.png'),
                 pygame.image.load('data/R2E.png'),
                 pygame.image.load('data/R3E.png'),
                 pygame.image.load('data/R4E.png'),
                 pygame.image.load('data/R5E.png'),
                 pygame.image.load('data/R6E.png'),
                 pygame.image.load('data/R7E.png'),
                 pygame.image.load('data/R8E.png'),
                 pygame.image.load('data/R9E.png'),
                 pygame.image.load('data/R10E.png'),
                 pygame.image.load('data/R11E.png')]

    walkLeft = [pygame.image.load('data/L1E.png'),
                pygame.image.load('data/L2E.png'),
                pygame.image.load('data/L3E.png'),
                pygame.image.load('data/L4E.png'),
                pygame.image.load('data/L5E.png'),
                pygame.image.load('data/L6E.png'),
                pygame.image.load('data/L7E.png'),
                pygame.image.load('data/L8E.png'),
                pygame.image.load('data/L9E.png'),
                pygame.image.load('data/L10E.png'),
                pygame.image.load('data/L11E.png')]

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.path = [64, 634]
        self.walkCount = 0
        self.hit_box = (self.x + 17, self.y + 2, 31, 57)
        self.width = self.hit_box[2]
        self.vel = 1.3
        self.laser_count = 0

    def move(self):
        if self.vel > 0:
            e = self.vel
            if self.x + self.vel < self.path[1] - self.hit_box[2]:
                self.x += e
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            e = self.vel
            if self.x - self.vel > self.path[0]:
                self.x += e
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def draw(self, win):
        self.move()

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
            self.hit_box = (self.x + 14, self.y + 2, 31, 57)
        else:
            self.hit_box = (self.x + 23, self.y + 2, 31, 57)

        if show_game:
            self.draw_health_bar(win)

        self.fire()

    def draw_health_bar(self, win):
        y = self.hit_box[1] - 10
        health_font = pygame.font.SysFont('arial', 20)
        text = health_font.render(str(self.health), 1, red)
        win.blit(text, (self.hit_box[0] + (self.hit_box[2] / 2), y))

    def fire(self):
        if self.laser_count == 0:
            enemy_lasers.append(Laser(self.x + round(self.width / 2) + 15, self.y + 8, green))
            self.laser_count = 1
        else:
            self.laser_count += 1
            if self.laser_count > 66:
                self.laser_count = 0

    def hit(self):
        self.health -= 1


class Laser:

    def __init__(self, x, y, laser_color):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 30
        self.color = laser_color
        self.vel = 4

    def draw(self, win):
        if show_game:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class EnemySpaceship:

    def __init__(self):
        self.x = 150
        self.y = 70
        self.width = 110
        self.vel = 3
        self.height = 50
        self.health = 50
        self.path = [64, 634]
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.laser_count = 0

    def draw(self, win):
        global color
        color = green
        if show_game:
            pygame.draw.rect(win, grey, (self.x + 20, self.y, 70, 50))
            pygame.draw.rect(win, color, (self.x + 90, self.y, 20, 35))
            pygame.draw.rect(win, color, (self.x, self.y, 20, 35))
            pygame.draw.rect(win, white, (self.x + round(self.width / 2) - 5, self.y + 50, 10, 20))

        self.hit_box = (self.x, self.y, self.width, self.height)

        if show_game:
            self.draw_health_bar(win)

        self.move()
        self.fire()

    def move(self):
        if self.vel > 0:
            self.vel = 3
            if self.x + self.vel < self.path[1] - self.hit_box[2]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            self.vel = -3
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

    def fire(self):
        if self.laser_count == 0:
            if self.vel > 0:
                enemy_lasers.append(Laser(self.x + round(self.width / 2) + 13, self.y + 8, green))
            else:
                enemy_lasers.append(Laser(self.x + round(self.width / 2) - 13, self.y + 8, green))

            self.laser_count = 1

        else:
            self.laser_count += 1
            if self.laser_count > 33:
                self.laser_count = 0

    def hit(self):
        self.health -= 1

    def draw_health_bar(self, win):
        y = self.hit_box[1] - 10
        health_font = pygame.font.SysFont('arial', 20)
        text = health_font.render(str(self.health), 1, red)
        win.blit(text, (round((self.hit_box[0] + (self.hit_box[2] / 2)) - round(text.get_width() / 2)), y - 10))


battleship = Spaceship()
lasers = []
enemy_lasers = []
aliens = []
enemy_spaceships = []
K_LEFT, K_RIGHT, K_SPACE = 1073741904, 1073741903, 32
keys = {
    K_LEFT: False,
    K_RIGHT: False,
    K_SPACE: False
}
battleship_healths = []


def show_level(win, level, msg):
    lvlfont = pygame.font.SysFont('comicsans', 50)
    text = lvlfont.render('Level: ' + str(level), 1, white)
    win.blit(text, (350 - round(text.get_width() / 2), 275))

    msgfont = pygame.font.SysFont('comicsans', 30)
    text = msgfont.render(msg, 1, white)
    win.blit(text, (350 - round(text.get_width() / 2), 315))

    pygame.display.update()
    time.sleep(2)


def generate_level(win):
    global add_alien
    global level
    global alien_number
    global alien_health
    global alien_laser_damage
    global spawn_aliens
    global alien_kills
    global spaceship_kills
    global battleship

    if (level % 5) == 2:
        alien_health += 2
        if show_game:
            show_level(win, level + 1, 'Alien health +2')
    elif (level % 5) == 3:
        alien_laser_damage += 1
        if show_game:
            show_level(win, level + 1, 'Alien laser damage +1')
    elif (level % 5) == 4:
        alien_health += 2
        alien_laser_damage += 1
        if show_game:
            show_level(win, level + 1, 'Alien health +2 and Alien laser damage +1')
    elif (level % 5) == 0:
        if show_game:
            show_level(win, level + 1, 'Enemy spaceship attacks')
        spawn_aliens = False
    elif (level % 5) == 1:
        redraw_game_window(win)
        if add_alien:
            if alien_number < 3:
                alien_number += 1
            if show_game:
                show_level(win, level + 1, 'Alien number +1')
            add_alien = False
        else:
            alien_laser_damage += 2
            if show_game:
                show_level(win, level + 1, 'Alien laser damage +2')
            add_alien = True

    if spawn_aliens:
        for e in range(alien_number):
            if e == 1:
                aliens.append(EnemyAlien(64, 70, alien_health))
            elif e == 2:
                aliens.append(EnemyAlien(634, 70, alien_health))
            else:
                aliens.append(EnemyAlien(349, 70, alien_health))

    else:
        enemy_spaceships.append(EnemySpaceship())
        spawn_aliens = True

    level += 1


def redraw_game_window(win):
    global battleship
    global alien_kills
    global spaceship_kills

    if show_game:
        win.blit(game_background, (0, 0))

        lvlfont = pygame.font.SysFont('comicsans', 30)
        text = lvlfont.render('Level: ' + str(level), 1, white)
        win.blit(text, (350 - round(text.get_width() / 2), 5))

    for laser in lasers:
        laser.draw(win)

    for laser in enemy_lasers:
        laser.draw(win)

    for alien in aliens:
        if alien.health > 0:
            alien.draw(win)

    for v in enemy_spaceships:
        if v.health > 0:
            v.draw(win)

    battleship.draw(win)
    if show_game:
        battleship.draw_health_bar(win)

        pygame.display.update()


def initialize(show, win_caption):
    global show_game
    global screen_width
    global screen_height
    global game_background
    global frames
    global shoot_loop
    global alien_kills
    global level
    global spaceship_kills
    global show1
    global spawn_aliens
    global add_alien
    global alien_number
    global alien_health
    global alien_laser_damage
    global battleship
    global lasers
    global enemy_lasers
    global aliens
    global enemy_spaceships
    global keys
    global battleship_healths

    show_game = show
    if show_game:
        pygame.init()
        game_background = pygame.image.load('data/bg.jpg')
        win = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(win_caption)

    else:
        win = None

    frames = 0

    shoot_loop = 0
    alien_kills = 0
    level = 1
    spaceship_kills = 0
    show1 = True
    spawn_aliens = True
    add_alien = False
    alien_number = 2
    alien_health = 10
    alien_laser_damage = 1

    battleship = Spaceship()
    lasers = []
    enemy_lasers = []
    aliens = []
    enemy_spaceships = []
    keys = {
        K_LEFT: False,
        K_RIGHT: False,
        K_SPACE: False
    }
    battleship_healths = []
    return win


def run(win, net=None, routine=None):
    global alien_kills
    global spaceship_kills
    global battleship
    global enemy_spaceships
    global aliens
    global lasers
    global enemy_lasers
    global frames
    global keys
    global battleship_healths
    global show1
    global shoot_loop

    frames += 1

    if frames > 1000000:
        print("game stopped")
        return 0  # stop the game, prevent training get stuck

    if show_game:
        clock.tick(120)

    redraw_game_window(win)

    if show1:
        battleship_healths.append(battleship.health)
        alien_kills = 0
        spaceship_kills = 0
        generate_level(win)
        if show_game:
            show_level(win, level, '')
        show1 = False

    if show_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

    if frames % 10 == 0:
        aliens_x = [0, 0, 0]
        for a, alien in enumerate(aliens):
            if a < 3:
                aliens_x[a] = alien.x

        laser_x = [0, 0, 0, 0, 0, 0]
        laser_y = [0, 0, 0, 0, 0, 0]
        # Give as input the 5 closer enemy lasers
        enemy_lasers_with_distance = [(laser, pow(pow(laser.x - battleship.x, 2) + pow(laser.y - battleship.y, 2), 1 / 2)) for laser in enemy_lasers]
        enemy_lasers_with_distance.sort(key=lambda x: x[1])
        for e, enemy_laser_with_distance in enumerate(enemy_lasers_with_distance):
            if e < 6:
                laser_x[e] = enemy_laser_with_distance[0].x
                laser_y[e] = enemy_laser_with_distance[0].y

        enemy_spaceships_x = [0]
        for s, enemy_spaceship in enumerate(enemy_spaceships):
            if s < 1:
                enemy_spaceships_x[s] = enemy_spaceship.x

        if net:  # TODO pass to the network relevant information as input
            outputs = net.activate((battleship.x,
                                    battleship.vel,
                                    aliens_x[0],
                                    aliens_x[1],
                                    aliens_x[2],
                                    laser_x[0],
                                    laser_y[0],
                                    laser_x[1],
                                    laser_y[1],
                                    laser_x[2],
                                    laser_y[2],
                                    laser_x[3],
                                    laser_y[3],
                                    laser_x[4],
                                    laser_y[4],
                                    laser_x[5],
                                    laser_y[5],
                                    enemy_spaceships_x[0]))
            i = np.argmax(np.array(outputs))
            keys = {
                K_LEFT: i == 0 or i == 1,
                K_RIGHT: i == 4 or i == 5,
                K_SPACE: i == 1 or i == 3 or i == 5
            }

        if routine:  # TODO pass to the program relevant information as input
            output = routine(battleship.x,
                             battleship.vel,
                             aliens_x[0],
                             aliens_x[1],
                             aliens_x[2],
                             laser_x[0],
                             laser_y[0],
                             laser_x[1],
                             laser_y[1],
                             laser_x[2],
                             laser_y[2],
                             laser_x[3],
                             laser_y[3],
                             laser_x[4],
                             laser_y[4],
                             laser_x[5],
                             laser_y[5],
                             enemy_spaceships_x[0])
            keys = {
                K_LEFT: output == A or output == B,
                K_RIGHT: output == E or output == F,
                K_SPACE: output == B or output == D or output == F
            }

    if keys[K_LEFT]:
        if battleship.x > battleship.vel:
            battleship.x -= battleship.vel

    if keys[K_RIGHT]:
        if battleship.x < screen_width - battleship.width - battleship.vel:
            battleship.x += battleship.vel

    if keys[K_SPACE]:
        if shoot_loop == 0:
            battleship.fire()
            shoot_loop = 1

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 14:
        shoot_loop = 0

    lasers_to_pop = set()
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
                lasers_to_pop.add(laser)

    for laser in lasers_to_pop:
        lasers.pop(lasers.index(laser))

    for alien in aliens:
        for laser in lasers:
            if alien.hit_box[1] + alien.hit_box[3] > laser.y > alien.hit_box[1]:
                if alien.hit_box[0] < laser.x < alien.hit_box[0] + alien.hit_box[2]:
                    alien.hit()
                    lasers.pop(lasers.index(laser))
            elif alien.hit_box[1] + alien.hit_box[3] > laser.y + laser.height > alien.hit_box[1]:
                if alien.hit_box[0] < laser.x < alien.hit_box[0] + alien.hit_box[2]:
                    alien.hit()
                    lasers.pop(lasers.index(laser))

    for v in enemy_spaceships:
        for laser in lasers:
            if v.hit_box[1] + v.hit_box[3] > laser.y > v.hit_box[1]:
                if v.hit_box[0] < laser.x < v.hit_box[0] + v.hit_box[2]:
                    v.hit()
                    lasers.pop(lasers.index(laser))
            elif v.hit_box[1] + v.hit_box[3] > laser.y + laser.height > v.hit_box[1]:
                if v.hit_box[0] < laser.x < v.hit_box[0] + v.hit_box[2]:
                    v.hit()
                    lasers.pop(lasers.index(laser))

    for laser in enemy_lasers:
        if battleship.hit_box[1] + battleship.hit_box[3] > laser.y + laser.height > battleship.hit_box[1]:
            if battleship.hit_box[0] < laser.x < battleship.hit_box[0] + battleship.hit_box[2]:
                battleship.hit()
                enemy_lasers.pop(enemy_lasers.index(laser))

    for laser in enemy_lasers:
        if laser.y < 470:
            laser.y += laser.vel
        else:
            enemy_lasers.pop(enemy_lasers.index(laser))

    for alien in aliens:
        if alien.health <= 0:
            aliens.pop(aliens.index(alien))
            alien_kills += 1

    for v in enemy_spaceships:
        if v.health <= 0:
            enemy_spaceships.pop()
            spaceship_kills += 1

    if battleship.health <= 0:
        return 0

    if len(aliens) == 0 and len(enemy_spaceships) == 0:
        lasers = []
        enemy_lasers = []
        battleship.x = 150
        redraw_game_window(win)
        generate_level(win)
        battleship_healths.append(battleship.health)

    return 1
