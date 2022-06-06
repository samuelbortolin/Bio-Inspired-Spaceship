def start():
    import gamerun
    import save as s

    if gamerun.show_game:
        import pygame
        pygame.init()

        screen_width = 700
        screen_height = 550
        win = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('NEAT Spaceship!')
    else:
        win = None

    game = True

    while game:
        num = gamerun.run(win)
        if num == 0:
            game = False

    if gamerun.level > s.readlevel():
        s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)
    elif gamerun.totaltestseconds > s.readseconds() and gamerun.level == s.readlevel():
        s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)

    if gamerun.show_game:
        pygame.quit()


if __name__ == '__main__':
    start()
