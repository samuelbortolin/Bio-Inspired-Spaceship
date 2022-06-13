from __future__ import print_function

from pylab import *

import os
import pickle

import neat
import pygame

import gamerun
import visualize


def simulate_game(show_game, net):
    gamerun.show_game = show_game
    if gamerun.show_game:
        pygame.init()
        # gamerun.clock = pygame.time.Clock()
        gamerun.gamebg = pygame.image.load('data/bg.jpg')
        gamerun.lasersound = pygame.mixer.Sound('data/laser.wav')
        gamerun.hitsound = pygame.mixer.Sound('data/hit.wav')

        screen_width = 700
        screen_height = 550
        win = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('NEAT Spaceship!')

    else:
        win = None

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
    gamerun.holdingpowerup = False
    gamerun.usepowerup = False
    gamerun.poweruploop = 0

    gamerun.aliennumber = 2
    gamerun.alienhealth = 10
    gamerun.alienlaserdamage = 1
    gamerun.alienvelocity = 1.3

    gamerun.battleship = gamerun.Spaceship()
    gamerun.lasers = []
    gamerun.enemy_lasers = []
    gamerun.aliens = []
    gamerun.enemy_spaceships = []

    game = True
    while game:
        result = gamerun.run(win, net)
        if result == 0:
            game = False

    # if gamerun.level > s.readlevel():
    #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)
    # elif gamerun.totaltestseconds > s.readseconds() and gamerun.level == s.readlevel():
    #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)

    # TODO define a fitness based on gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frame
    print(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frames)
    return (gamerun.level - 1) * 100 + gamerun.alienkills * 10 + gamerun.spaceshipkills * 50 + gamerun.frames // 1000


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulate_game(show_game=False, net=net)


num_generations = 50
num_runs = 1

config_file = "config.txt"
run_best = True


if __name__ == "__main__":

    # TODO we should also test GP and compare it with NEAT

    # Load configuration.
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, config_file)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    if not run_best:
        if num_runs == 1:
            # Create the population.
            p = neat.Population(config)

            # Add a stdout reporter to show progress in the terminal.
            stats = neat.StatisticsReporter()
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(stats)

            # Run NEAT for num_generations.
            winner = p.run(eval_genomes, num_generations)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Create the winning network.
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            # Simulate the game with the winning network and showing it.
            show_game = True
            best_fitness = simulate_game(show_game=show_game, net=winner_net)
            print(f"\nBest fitness simulation:\n{best_fitness}")

            # TODO dump and store image only if it has a better fitness.
            pickle.dump(winner, open(f"winner_{datetime.datetime.now().isoformat()}_fitness_{best_fitness}.pkl", "wb"))
            pickle.dump(winner_net, open(f"winner_net_{datetime.datetime.now().isoformat()}_fitness_{best_fitness}.pkl", "wb"))
            visualize.draw_net(config, winner, filename=f"winner_net_{datetime.datetime.now().isoformat()}_fitness_{best_fitness}", view=True)
            if show_game:
                pygame.quit()

        else:
            results = []
            best_fitnesses = []
            for i in range(num_runs):
                print(f"run {i + 1}/{num_runs}")

                # Create the population.
                p = neat.Population(config)

                # Add a stdout reporter to show progress in the terminal.
                stats = neat.StatisticsReporter()
                p.add_reporter(neat.StdOutReporter(True))
                p.add_reporter(stats)

                # Run NEAT for num_generations.
                winner = p.run(eval_genomes, num_generations)

                # Display the winning genome.
                print(f"\nBest genome:\n{winner}")

                # Store best fitness for statistical analysis.
                best_fitnesses.append(winner.fitness)

                # Create the winning network.
                winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

                # TODO dump and store image only if it has a better fitness.
                pickle.dump(winner, open(f"winner_{datetime.datetime.now().isoformat()}_fitness_{winner.fitness}.pkl", "wb"))
                pickle.dump(winner_net, open(f"winner_net_{datetime.datetime.now().isoformat()}_fitness_{winner.fitness}.pkl", "wb"))
                visualize.draw_net(config, winner, filename=f"winner_net_{datetime.datetime.now().isoformat()}_fitness_{winner.fitness}", view=True)

            results.append(best_fitnesses)

            fig = figure('NEAT')
            ax = fig.gca()
            ax.boxplot(results)
            ax.set_ylabel('Best fitness')
            show()

    else:
        # TODO load the one with better fitness
        winner = pickle.load(open("winner2022-06-13T10:27:19.283603.pkl", "rb"))
        winner_net = pickle.load(open("winner_net2022-06-13T10:27:20.859471.pkl", "rb"))

        show_game = True
        best_fitness = simulate_game(show_game=show_game, net=winner_net)
        print(f"\nBest fitness simulation:\n{best_fitness}")
        if show_game:
            pygame.quit()
