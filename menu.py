import pygame
import tutorial as t
import save as s

pygame.init()
clock = pygame.time.Clock()

yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
green = (0, 222, 0)

screenbreite = 700
screenhoehe = 550

mushelp = False
soundhelp = False
laser = pygame.mixer.Sound('data/laser.wav')

soundvol = 0.5
musicvol = 0.5


class VolumeBar:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vollevel = 50
        self.volume = 0.5
        self.maxvol = 100
        self.minvol = 0
        self.soundplay = False

    def calcvolume(self):
        return self.vollevel / 100

    def drawchest(self, win, x, msg, fill, col):
        pygame.draw.rect(win, yellow, (x, self.y, 35, 35), fill)
        font2 = pygame.font.SysFont('comicsansms', 30)
        text = font2.render(msg, 1, col)
        win.blit(text, (round(x + (35 / 2 - text.get_width() / 2)), round(self.y + (35 / 2 - text.get_height() / 2))))

    def checkchest(self, win):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + 35 and self.y < mouse[1] < self.y + 35:
            self.drawchest(win, self.x, '-', 0, black)
            if click[0] == 1 and self.minvol < self.vollevel <= self.maxvol:
                self.soundplay = True
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                self.vollevel -= 5
                self.volume = self.calcvolume()

        else:
            self.drawchest(win, self.x, '-', 1, yellow)

        if self.x + 255 < mouse[0] < self.x + 290 and self.y < mouse[1] < self.y + 35:
            self.drawchest(win, self.x + 255, '+', 0, black)
            if click[0] == 1 and self.minvol <= self.vollevel < self.maxvol:
                self.soundplay = True
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                self.vollevel += 5
                self.volume = self.calcvolume()
        else:
            self.drawchest(win, self.x + 255, '+', 1, yellow)

    def draw(self, win):
        if self.vollevel != 0:
            pygame.draw.rect(win, yellow, (self.x + 45, self.y + 17, 2 * self.vollevel, 5))
        self.checkchest(win)

    def get_Volume(self):
        return self.volume


class ChooseButton:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tof = True

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + 120 and self.y < mouse[1] < self.y + 30:
            if not self.tof and click[0] == 1:
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                    self.tof = True

        if self.x + 170 < mouse[0] < self.x + 270 and self.y < mouse[1] < self.y + 30:
            if self.tof and click[0] == 1:
                loop = True
                while loop:
                    e = False
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            e = True
                    if e:
                        break
                    self.tof = False

    def draw(self, win):

        if self.tof:
            colortext1 = black
            colortext2 = yellow
            c1 = 0
            c2 = 1
        else:
            colortext1 = yellow
            colortext2 = black
            c1 = 1
            c2 = 0

        pygame.draw.rect(win, yellow, (self.x, self.y, 120, 30), c1)
        font1 = pygame.font.SysFont('comicsansms', 20)
        text = font1.render('ON', 1, colortext1)
        win.blit(text, (round(self.x + (120 / 2 - text.get_width() / 2)), round(self.y + (30 / 2 - text.get_height() / 2))))

        pygame.draw.rect(win, yellow, (self.x + 170, self.y, 120, 30), c2)
        font1 = pygame.font.SysFont('comicsansms', 20)
        text = font1.render('OFF', 1, colortext2)
        win.blit(text, (round(self.x + 170 + (120 / 2 - text.get_width() / 2)), round(self.y + (30 / 2 - text.get_height() / 2))))

        self.check()

    def get_tof(self):
        if self.tof:
            return True
        return False


musicchoose = ChooseButton(370, 140)
musicbar = VolumeBar(370, 205)
soundchoose = ChooseButton(370, 300)
soundbar = VolumeBar(370, 365)


def drawMenuLayout(win):
    win.fill((0, 0, 0))
    font1 = pygame.font.SysFont('comicsansms', 80)
    text = font1.render('Yellow Spaceship!', 1, yellow)
    win.blit(text, (20, 10))
    font2 = pygame.font.SysFont('comicsansms', 15)
    text2 = font2.render('v.1.0.0', 1, white)
    win.blit(text2, (screenbreite - text2.get_width() - 20, screenhoehe - text2.get_height() - 5))

    t.drawtutorialship(win, 50, 400)
    pygame.draw.rect(win, grey, (90, 150, 70, 50))
    pygame.draw.rect(win, green, (160, 150, 20, 35))
    pygame.draw.rect(win, green, (70, 150, 20, 35))
    pygame.draw.rect(win, white, (120, 200, 10, 20))

    pygame.draw.rect(win, green, (122, 260, 3, 30))
    pygame.draw.rect(win, yellow, (104, 340, 3, 30))


def drawChooseTutorial(win):
    drawMenuLayout(win)
    font1 = pygame.font.SysFont('comicsansms', 30)
    text = font1.render('Do you want to do the tutorial?', 1, white)
    win.blit(text, (230, 170))

    global yesbutton
    global nobutton
    global backbutton
    yesbutton = t.button(win, 'Yes', 270, 280, 150, 50, yellow, black, yellow)
    nobutton = t.button(win, 'No', 470, 280, 150, 50, yellow, black, yellow)
    backbutton = t.button(win, 'Back', 470, 470, 150, 50, yellow, black, yellow)

    pygame.display.update()


def redrawMenuWindow(win):
    drawMenuLayout(win)

    global button1
    global button2
    global button3
    global button4
    global button5
    button1 = t.button(win, 'Play!', 470, 150, 150, 50, yellow, black, yellow)
    button2 = t.button(win, 'Settings', 470, 220, 150, 50, yellow, black, yellow)
    button3 = t.button(win, 'Score', 470, 290, 150, 50, yellow, black, yellow)
    button4 = t.button(win, 'Credits', 470, 360, 150, 50, yellow, black, yellow)
    button5 = t.button(win, 'Quit', 470, 430, 150, 50, yellow, black, yellow)

    pygame.display.update()


def drawSettings(win):
    drawMenuLayout(win)
    global backbutton
    backbutton = t.button(win, 'Back', 470, 470, 150, 50, yellow, black, yellow)

    font1 = pygame.font.SysFont('comicsansms', 20)
    text = font1.render('Music:', 1, white)
    win.blit(text, (300, 140))
    text = font1.render('Sounds:', 1, white)
    win.blit(text, (290, 300))
    global mushelp
    global soundhelp
    musicchoose.draw(win)

    if musicchoose.get_tof() and mushelp:
        mushelp = False
        pygame.mixer.music.play(-1)
    elif not (musicchoose.get_tof()):
        pygame.mixer.music.stop()
        mushelp = True

    if musicchoose.tof:
        text = font1.render('Volume:', 1, white)
        win.blit(text, (round(370 + 290 / 2 - text.get_width() / 2), 180))
        musicbar.draw(win)
        pygame.mixer.music.set_volume(musicbar.get_Volume())

    soundchoose.draw(win)
    if soundchoose.get_tof() and soundhelp:
        soundhelp = False
        laser.play()
    elif not (soundchoose.get_tof()):
        soundhelp = True

    if soundchoose.tof:
        text = font1.render('Volume:', 1, white)
        win.blit(text, (round(370 + 290 / 2 - text.get_width() / 2), 340))
        soundbar.draw(win)
        laser.set_volume(soundbar.get_Volume())
        if soundbar.soundplay:
            laser.play()
            soundbar.soundplay = False

    pygame.display.update()


def drawscorewin(win):
    drawMenuLayout(win)
    global backbutton
    backbutton = t.button(win, 'Back', 470, 470, 150, 50, yellow, black, yellow)

    try:
        scorearray = s.read()

        datefont = pygame.font.SysFont('comicsansms', 30)
        text = datefont.render('Best save with this game file:', 1, white)
        win.blit(text, (250, 130))
        text = datefont.render('Date: ' + scorearray[0], 1, white)
        win.blit(text, (250, 210))
        text = datefont.render('Reached Level: ' + str(scorearray[1]), 1, white)
        win.blit(text, (250, 250))
        text = datefont.render('Aliens killed: ' + scorearray[2], 1, white)
        win.blit(text, (250, 290))
        text = datefont.render('Spaceships destroyed: ' + scorearray[3], 1, white)
        win.blit(text, (250, 330))
        text = datefont.render('Survived time: ' + scorearray[4], 1, white)
        win.blit(text, (250, 370))

    except Exception:
        datefont = pygame.font.SysFont('comicsansms', 20)
        text = datefont.render('You haven´t played a game with this game', 1, white)
        win.blit(text, (250, 130))
        text = datefont.render('file so far.', 1, white)
        win.blit(text, (250, 160))
        text = datefont.render("Just begin your first game by clicking 'Play!'", 1, white)
        win.blit(text, (250, 220))
        text = datefont.render("on the main menu. You can do the tutorial first", 1, white)
        win.blit(text, (250, 250))
        text = datefont.render("if you want to.", 1, white)
        win.blit(text, (250, 280))
        text = datefont.render("Good luck! You´re gonna need it :P", 1, white)
        win.blit(text, (250, 330))

    pygame.display.update()


def drawCredits(win):
    drawMenuLayout(win)
    crefont = pygame.font.SysFont('comicsansms', 30)
    text = crefont.render('Credits:', 1, white)
    win.blit(text, (250, 130))
    cfont = pygame.font.SysFont('comicsansms', 20)
    text = cfont.render('Menu music: "Epic" from Bensound.com', 1, white)
    win.blit(text, (250, 170))
    text = cfont.render('Game music: "Evolution" from Bensound.com', 1, white)
    win.blit(text, (250, 200))
    text = cfont.render('Space picture: "Milchstraße" by Felix', 1, white)
    win.blit(text, (250, 230))
    text = cfont.render('Mittermeier on pixabay.com', 1, white)
    win.blit(text, (250, 260))
    text = cfont.render('Version: 1.0.0', 1, white)
    win.blit(text, (250, 320))
    text = cfont.render('made with IDLE 3.8.3 and pygame 1.9.6', 1, white)
    win.blit(text, (250, 350))
    text = cfont.render('.exe-version converted with cx_Freeze 6.1', 1, white)
    win.blit(text, (250, 380))
    global nextbutton
    nextbutton = t.button(win, 'Next', 470, 470, 150, 50, yellow, black, yellow)

    pygame.display.update()


def drawCredits2(win):
    drawMenuLayout(win)
    crefont = pygame.font.SysFont('comicsansms', 30)
    text = crefont.render('Credits:', 1, white)
    win.blit(text, (250, 130))

    cfont = pygame.font.SysFont('comicsansms', 20)
    text = cfont.render('Alien pictures, ingame sounds: Tech with Tims', 1, white)
    win.blit(text, (250, 170))
    text = cfont.render('pygame tutorial (I highy recommend checking', 1, white)
    win.blit(text, (250, 200))
    text = cfont.render('him out he makes awesome tutorials/videos).', 1, white)
    win.blit(text, (250, 230))
    text = cfont.render('If you find any bugs or have suggestions or', 1, white)
    win.blit(text, (250, 290))
    text = cfont.render('ideas feel free to contact me (GitHub:', 1, white)
    win.blit(text, (250, 320))
    text = cfont.render('@ph3nix-cpu or just use the comment section', 1, white)
    win.blit(text, (250, 350))
    text = cfont.render('on pygame.org.', 1, white)
    win.blit(text, (250, 380))
    text = cfont.render('Thank you for playing, I hope you enjoy it!', 1, white)
    win.blit(text, (250, 425))

    global backbutton
    backbutton = t.button(win, 'Back', 470, 470, 150, 50, yellow, black, yellow)

    pygame.display.update()


def drawquit(win):
    drawMenuLayout(win)
    font1 = pygame.font.SysFont('comicsansms', 30)
    text = font1.render('Are you sure you want to quit?', 1, white)
    win.blit(text, (250, 150))

    font2 = pygame.font.SysFont('comicsansms', 30)
    text = font1.render('Your highscore will be saved!', 1, white)
    win.blit(text, (250, 200))

    global yesbutton
    global nobutton
    yesbutton = t.button(win, 'Yes', 250, 280, 150, 50, yellow, black, yellow)
    nobutton = t.button(win, 'No', 450, 280, 150, 50, yellow, black, yellow)

    pygame.display.update()


def menu(win):
    clock.tick(30)
    redrawMenuWindow(win)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
    if button1:
        choosetut = True
        while choosetut:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawChooseTutorial(win)
            if yesbutton:
                tutorial = True
                while tutorial:
                    clock.tick(30)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return 0
                    drawMenuLayout(win)
                    num = t.doTutorial(win)
                    if num == 1:
                        return 1
                    elif num == 2:
                        tutorial = False
                        choosetut = False
            if nobutton:
                return 1
            if backbutton:
                choosetut = False
    if button2:
        settings = True
        while settings:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawSettings(win)
            if backbutton:
                settings = False
    if button3:
        scorewin = True
        while scorewin:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawscorewin(win)
            if backbutton:
                scorewin = False

    if button4:
        credit = True
        while credit:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawCredits(win)
            if nextbutton:
                credit2 = True
                credit = False
        while credit2:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawCredits2(win)
            if backbutton:
                credit2 = False

    if button5:
        quitt = True
        while quitt:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            drawquit(win)
            if yesbutton:
                return 0
            if nobutton:
                quitt = False
