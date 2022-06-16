from __future__ import print_function
from fileinput import filename

from pylab import *

import os
import pickle

import neat
import pygame

import gamerun
import visualize

import argparse
import traceback


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
    # gamerun.pausebutton = False
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

    # TODO find the best fitness based on gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frame
    print(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills)  # , gamerun.frames)  # TODO valutare se rimuove il numero di frame dal fitness? (kind of penalty for escaping?)
    # TODO magari valutare i colpi dati ai nemici (da massimizzare) e minimizzare quelli andati a vuoto?
    # TODO magari valutare i colpi presi dai nemici (da minimizzare, i.e., subirli più avanti in livelli più complessi)?
    return (gamerun.level - 1) * 100 + gamerun.alienkills * 10 + gamerun.spaceshipkills * 50  # + gamerun.frames // 1000


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulate_game(show_game=False, net=net)

def load_best():
    genome, network = None, None
    if os.path.isdir('runs/best/'):
        for filename in os.listdir('runs/best/'):
            if 'network' in filename:
                network = pickle.load(open(f"runs/best/{filename}", "rb"))
            elif 'genome' in filename:
                genome = pickle.load(open(f"runs/best/{filename}", "rb"))

    return genome, network

def save_best(genome, network):
    now = datetime.datetime.now().isoformat()
    dirname = f"runs/{now}_fitness_{genome.fitness}"
    os.mkdir(dirname)
    pickle.dump(genome, open(f"{dirname}/genome.pkl", "wb"))
    pickle.dump(network, open(f"{dirname}/network.pkl", "wb"))
    visualize.draw_net(config, genome, filename=f"{dirname}/representation", view=False)

    best_genome, _ = load_best()
    if best_genome is None or best_genome.fitness < genome.fitness:
        if not os.path.isdir('runs/best/'):
            os.mkdir('runs/best/')

        pickle.dump(genome, open(f"runs/best/genome.pkl", "wb"))
        pickle.dump(network, open(f"runs/best/network.pkl", "wb"))
        visualize.draw_net(config, genome, filename=f"runs/best/representation", view=False)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NEAT Spaceship")
    parser.add_argument("--run_best", action="store_true", help="Run the best individual found")
    parser.add_argument("--neat", action="store_true", help="Run the NEAT algorithm for training of the NN")
    parser.add_argument("--config_file", type=str, default="config.txt", help="Run the NEAT algorithm for training of the NN")
    parser.add_argument("--num_runs", type=int, default=1, help="The number of runs")
    parser.add_argument("--num_generations", type=int, default=10, help="The number of generations for each run")
    args = parser.parse_args()

    # TODO we should also test GP and compare it with NEAT

    # Load configuration.
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, args.config_file)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    if args.neat:
        if args.num_runs == 1:
            # Create the population.
            p = neat.Population(config)

            # Add a stdout reporter to show progress in the terminal.
            stats = neat.StatisticsReporter()
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(stats)

            # Run NEAT for num_generations.
            try:
                genome = p.run(eval_genomes, args.num_generations)
            except Exception as e:
                traceback.print_exc()
                genome = p.best_genome
            except KeyboardInterrupt:
                genome = p.best_genome

            # Display the winning genome.
            print(f"\nBest genome:\n{genome}")

            # Create the winning network.
            network = neat.nn.FeedForwardNetwork.create(genome, config)

            # Simulate the game with the winning network and showing it.
            show_game = True
            best_fitness = simulate_game(show_game=show_game, net=network)
            print(f"\nBest fitness simulation:\n{best_fitness}")

            save_best(genome, network)
            if show_game:
                pygame.quit()

        else:
            results = []
            best_fitnesses = []
            try:
                for i in range(args.num_runs):
                    print(f"run {i + 1}/{args.num_runs}")

                    # Create the population.
                    p = neat.Population(config)

                    # Add a stdout reporter to show progress in the terminal.
                    stats = neat.StatisticsReporter()
                    p.add_reporter(neat.StdOutReporter(True))
                    p.add_reporter(stats)

                    # Run NEAT for num_generations.
                    genome = p.run(eval_genomes, args.num_generations)

                    # Display the winning genome.
                    print(f"\nBest genome:\n{genome}")

                    # Store best fitness for statistical analysis.
                    best_fitnesses.append(genome.fitness)

                    # Create the winning network.
                    network = neat.nn.FeedForwardNetwork.create(genome, config)

                    save_best(genome, network)

            except Exception as e:
                print(e)

            results.append(best_fitnesses)
            fig = figure("NEAT-Spaceship")
            ax = fig.gca()
            ax.boxplot(results)
            ax.set_ylabel("Best fitness")
            show()

    elif args.run_best:
        genome, network = load_best()
        if network is None:
            print("network not present")
        else:
            best_fitness = simulate_game(show_game=True, net=network)
            print(f"\nBest fitness simulation:\n{best_fitness}")
            pygame.quit()
