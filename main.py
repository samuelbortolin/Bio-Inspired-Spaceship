def start():
    import gamerun
    import pygame
    import menu as men
    import save as s
    pygame.init()

    screenbreite=700
    screenhoehe=550
    win=pygame.display.set_mode((screenbreite,screenhoehe))
    pygame.display.set_caption('Yellow Spaceship!')
    clock=pygame.time.Clock()

    game=True
    menu=True
    run=False

    yellow=(255,255,0)
    black=(0,0,0)
    white=(255,255,255)
    grey=(150,150,150)

    while game:
        pygame.mixer.music.load('data/bensound-epic.mp3')
        pygame.mixer.music.set_volume(men.musicbar.get_Volume())
        pygame.mixer.music.play(-1)
    
        while menu:
            number=men.menu(win)
            if number==0:
                menu=False
                game=False
            elif number==1:
                run=True
                menu=False
    
        pygame.mixer.music.stop()       
        if men.musicchoose.get_tof():
            pygame.mixer.music.load('data/bensound-evolution.mp3')
            pygame.mixer.music.set_volume(men.musicbar.get_Volume())
            pygame.mixer.music.play(-1)

        while run:
            num=gamerun.run(win)
            if num==0:
                run=False
                game=False
            if num==1:
                run=False
                menu=True
                
    if gamerun.level>s.readlevel():
        s.save(gamerun.level,gamerun.alienkills,gamerun.spaceshipkills,gamerun.timee,gamerun.totaltestseconds)
    elif gamerun.totaltestseconds>s.readseconds() and gamerun.level==s.readlevel():
        s.save(gamerun.level,gamerun.alienkills,gamerun.spaceshipkills,gamerun.timee,gamerun.totaltestseconds)
    pygame.quit()

if __name__=='__main__':
    start()
