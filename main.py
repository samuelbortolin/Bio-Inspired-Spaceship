from __future__ import print_function

import neat

import gamerun
import pygame
import os
import pickle

import visualize

from pylab import *


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        gamerun.frames = 0
        gamerun.seccount = 0
        gamerun.totaltestseconds = 0

        gamerun.shootloop = 0
        gamerun.alienkills = 0
        gamerun.level = 1
        gamerun.spaceshipkills = 0
        gamerun.colorcounter = 0
        gamerun.timee = ''
        gamerun.ru = True
        gamerun.pausebutton = False
        gamerun.show1 = True
        gamerun.spawnaliens = True
        gamerun.addalien = False
        gamerun.show_game = False
        gamerun.holdingpowerup = False
        gamerun.usepowerup = False
        gamerun.poweruploop = 0

        gamerun.aliennumber = 2
        gamerun.alienhealth = 1
        gamerun.alienlaserdamage = 1
        gamerun.alienvelocity = 1.3

        gamerun.battleship = gamerun.spaceship()
        gamerun.lasers = []
        gamerun.enemylasers = []
        gamerun.aliens = []
        gamerun.enemyspaceships = []

        game = True
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        if gamerun.show_game:
            pygame.init()

            screen_width = 700
            screen_height = 550
            win = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption('NEAT Spaceship!')
        else:
            win = None

        while game:
            num = gamerun.run(win, net)
            if num == 0:
                game = False

        # if gamerun.level > s.readlevel():
        #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)
        # elif gamerun.totaltestseconds > s.readseconds() and gamerun.level == s.readlevel():
        #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)

        # TODO compute fitness based on gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frame
        print(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frames)
        genome.fitness = (gamerun.level - 1) * 100 + gamerun.alienkills * 10 + gamerun.spaceshipkills * 50 + gamerun.frames // 1000


num_generations = 10
num_runs = 1

config_file = "config.txt"
run_best = False

if __name__=='__main__':
    local_dir = os.path.dirname(__file__)

    # Load configuration.
    config_file = os.path.join(local_dir, config_file)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    if not run_best:
        if num_runs == 1:
            # Create the population, which is the top-level object for a NEAT run.
            p = neat.Population(config)

            # Add a stdout reporter to show progress in the terminal.
            stats = neat.StatisticsReporter()
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(stats)

            # run NEAT for num_generations
            pygame.init()
            screenbreite = 700
            screenhoehe = 550
            yellow = (255, 255, 0)
            black = (0, 0, 0)
            white = (255, 255, 255)
            grey = (150, 150, 150)
            red = (255, 0, 0)
            green = (0, 222, 0)
            win = pygame.display.set_mode((screenbreite, screenhoehe))
            pygame.display.set_caption('Yellow Spaceship!')
            clock = pygame.time.Clock()
            winner = p.run(eval_genomes, num_generations)
            pickle.dump(winner, open(f"winner{datetime.datetime.now().isoformat()}.pkl", "wb"))

            # Display the winning genome.
            print('\nBest genome:\n{!s}'.format(winner))
            visualize.draw_net(config, winner, filename='spaceship', view=True)

            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
            pickle.dump(winner_net, open(f"winner_net{datetime.datetime.now().isoformat()}.pkl", "wb"))

            gamerun.frames = 0
            gamerun.seccount = 0
            gamerun.totaltestseconds = 0

            gamerun.shootloop = 0
            gamerun.alienkills = 0
            gamerun.level = 1
            gamerun.spaceshipkills = 0
            gamerun.colorcounter = 0
            gamerun.timee = ''
            gamerun.ru = True
            gamerun.pausebutton = False
            gamerun.show1 = True
            gamerun.spawnaliens = True
            gamerun.clock = pygame.time.Clock()
            gamerun.addalien = False
            gamerun.show_game = True

            if gamerun.show_game:
                import pygame

                pygame.init()
                gamerun.gamebg = pygame.image.load('data/bg.jpg')
                gamerun.lasersound = pygame.mixer.Sound('data/laser.wav')
                gamerun.hitsound = pygame.mixer.Sound('data/hit.wav')


            gamerun.holdingpowerup = False
            gamerun.usepowerup = False
            gamerun.poweruploop = 0

            gamerun.aliennumber = 2
            gamerun.alienhealth = 1
            gamerun.alienlaserdamage = 1
            gamerun.alienvelocity = 1.3

            gamerun.battleship = gamerun.spaceship()
            gamerun.lasers = []
            gamerun.enemylasers = []
            gamerun.aliens = []
            gamerun.enemyspaceships = []

            game = True

            if gamerun.show_game:
                pygame.init()

                screen_width = 700
                screen_height = 550
                win = pygame.display.set_mode((screen_width, screen_height))
                pygame.display.set_caption('NEAT Spaceship!')
            else:
                win = None

            while game:
                num = gamerun.run(win, winner_net)
                if num == 0:
                    game = False

            if gamerun.show_game:
                pygame.quit()

        else:
            results = []
            best_fitnesses = []
            for i in range(num_runs):
                print('{0}/{1}'.format(i + 1, num_runs))
                p = neat.Population(config)
                winner = p.run(eval_genomes, num_generations)
                best_fitnesses.append(winner.fitness)
            results.append(best_fitnesses)

            fig = figure('NEAT')
            ax = fig.gca()
            ax.boxplot(results)
            # ax.set_xticklabels(['Without elitism', 'With elitism'])
            # ax.set_yscale('log')
            # ax.set_xlabel('Condition')
            ax.set_ylabel('Best fitness')
            show()

    else:
        winner = pickle.load(open("winner2022-06-06T17:52:05.808753.pkl", "rb"))
        winner_net = pickle.load(open("winner_net2022-06-06T17:52:06.246884.pkl", "rb"))

        gamerun.frames = 0
        gamerun.seccount = 0
        gamerun.totaltestseconds = 0

        gamerun.shootloop = 0
        gamerun.alienkills = 0
        gamerun.level = 1
        gamerun.spaceshipkills = 0
        gamerun.colorcounter = 0
        gamerun.timee = ''
        gamerun.ru = True
        gamerun.pausebutton = False
        gamerun.show1 = True
        gamerun.spawnaliens = True
        gamerun.clock = pygame.time.Clock()
        gamerun.addalien = False
        gamerun.show_game = True

        if gamerun.show_game:
            import pygame

            pygame.init()
            gamerun.gamebg = pygame.image.load('data/bg.jpg')
            gamerun.lasersound = pygame.mixer.Sound('data/laser.wav')
            gamerun.hitsound = pygame.mixer.Sound('data/hit.wav')


        gamerun.holdingpowerup = False
        gamerun.usepowerup = False
        gamerun.poweruploop = 0

        gamerun.aliennumber = 2
        gamerun.alienhealth = 1
        gamerun.alienlaserdamage = 1
        gamerun.alienvelocity = 1.3

        gamerun.battleship = gamerun.spaceship()
        gamerun.lasers = []
        gamerun.enemylasers = []
        gamerun.aliens = []
        gamerun.enemyspaceships = []

        game = True

        if gamerun.show_game:
            pygame.init()

            screen_width = 700
            screen_height = 550
            win = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption('NEAT Spaceship!')
        else:
            win = None

        while game:
            num = gamerun.run(win, winner_net)
            if num == 0:
                game = False

        if gamerun.show_game:
            pygame.quit()
