from pylab import *

import argparse
import configparser
import operator
import os
import sys
import pickle
import traceback

import neat
import pygame
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import gamerun
import plot_utils
import visualize

from gp_train import AgentSimulator, if_then_else, Output, A, B, C, D, E, F


def simulate_game(show_game, name="", net=None, program=None, routine=None):
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
        pygame.display.set_caption(name)

    else:
        win = None

    gamerun.frames = 0
    gamerun.totaltestseconds = 0

    gamerun.shootloop = 0
    gamerun.alienkills = 0
    gamerun.level = 1
    gamerun.spaceshipkills = 0
    gamerun.colorcounter = 0
    gamerun.timee = ''
    gamerun.ru = True
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
    gamerun.keys = {
        gamerun.K_LEFT: False,
        gamerun.K_RIGHT: False,
        gamerun.K_SPACE: False
    }
    gamerun.battleship_healths = []
    gamerun.aliens_x = [0, 0, 0]
    gamerun.laser_x = [0, 0, 0, 0, 0, 0]
    gamerun.laser_y = [0, 0, 0, 0, 0, 0]
    gamerun.enemy_spaceships_x = [0]

    game = True
    while game:
        result = gamerun.run(win, net=net, program=program, routine=routine)
        if result == 0:
            game = False

    if gamerun.show_game:
        pygame.quit()

    # if gamerun.level > s.readlevel():
    #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)
    # elif gamerun.totaltestseconds > s.readseconds() and gamerun.level == s.readlevel():
    #     s.save(gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.timee, gamerun.totaltestseconds)

    # TODO find the best fitness based on gamerun.level, gamerun.alienkills, gamerun.spaceshipkills, gamerun.frame
    # fitness = (gamerun.level - 1) * 100 + gamerun.alienkills * 10 + gamerun.spaceshipkills * 50 # - gamerun.frames // 100000
    
    # health_fitness = 0
    # h_prec = gamerun.battleship_healths[0]
    # for i, h in enumerate(gamerun.battleship_healths[1:]):
    #     health_fitness += (h_prec - h)**2
    # health_fitness += gamerun.battleship_healths[-1]**2
    # health_fitness /= 10.0

    fitness = gamerun.alienkills * 10 + gamerun.spaceshipkills * 50 + gamerun.battleship_healths[-1]/10.0
    # fitness = gamerun.alienkills * 100 + gamerun.spaceshipkills * 500 - gamerun.frames / 10000.0 - health_fitness
    # fitness = gamerun.frames

    print(f"{fitness} -> {gamerun.level} {gamerun.alienkills} {gamerun.spaceshipkills} {gamerun.frames} {gamerun.battleship_healths}")
    # TODO valutare se rimuove il numero di frame dal fitness? (kind of penalty for escaping?)
    # TODO magari valutare i colpi dati ai nemici (da massimizzare) e minimizzare quelli andati a vuoto?
    # TODO magari valutare i colpi presi dai nemici (da minimizzare, i.e., subirli più avanti in livelli più complessi)?
    # TODO reason if makes sense to have a stopping criterion related to time (and not only death) --> this will be translated in find the best score for the considered max time
    return fitness


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulate_game(show_game=False, net=net)


def evalArtificialAgent(individual):
    # Transform the tree expression to functionnal Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    return simulate_game(show_game=False, program=agent, routine=routine),


def load_best_neat():
    genome, network = None, None
    path = 'runs/NEAT/best/'
    if os.path.isdir(path):
        for filename in os.listdir('runs/NEAT/best/'):
            if 'network' in filename:
                network = pickle.load(open(os.path.join(path, filename), "rb"))
            elif 'genome' in filename:
                genome = pickle.load(open(os.path.join(path, filename), "rb"))

    return genome, network


def save_best_neat(genome, network, config, stats):
    now = f"{datetime.datetime.now().isoformat()}".replace(':', '.')
    dirname = f"runs/NEAT/{now}_fitness_{genome.fitness}"
    os.mkdir(dirname)
    pickle.dump(genome, open(os.path.join(dirname, 'genome.pkl'), "wb"))
    pickle.dump(network, open(os.path.join(dirname, 'network.pkl'), "wb"))
    visualize.draw_net(config, genome, filename=f"{dirname}/representation", view=False)
    visualize.plot_stats(stats, view=True, filename=f"{dirname}/avg_fitness.png")
    visualize.plot_species(stats, view=True, filename=f"{dirname}/speciation.png")

    best_genome, _ = load_best_neat()
    if best_genome is None or best_genome.fitness < genome.fitness:
        path = 'runs/NEAT/best/'
        if not os.path.isdir(path):
            os.mkdir(path)

        pickle.dump(genome, open(os.path.join(path, 'genome.pkl'), "wb"))
        pickle.dump(network, open(os.path.join(path, 'network.pkl'), "wb"))
        visualize.draw_net(config, genome, filename=f"{path}representation", view=False)
        visualize.plot_stats(stats, view=True, filename=f"{path}avg_fitness.png")
        visualize.plot_species(stats, view=True, filename=f"{path}speciation.png")


def load_best_gp():
    program = None
    path = 'runs/GP/best/'
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if 'program' in filename:
                program = pickle.load(open(os.path.join(path, filename), "rb"))

    return program


def save_best_gp(program):
    now = f"{datetime.datetime.now().isoformat()}".replace(':', '.')
    dirname = f"runs/GP/{now}_fitness_{program.fitness.values[0]}"
    os.mkdir(dirname)
    pickle.dump(program, open(os.path.join(dirname, 'program.pkl'), "wb"))
    nodes, edges, labels = gp.graph(program)
    plot_utils.plotTree(nodes, edges, labels, "best", dirname)
    plot_utils.plotTrends(logbook, "best", dirname)

    best_program = load_best_gp()
    if best_program is None or best_program.fitness.values[0] < program.fitness.values[0]:
        path = 'runs/GP/best/'
        if not os.path.isdir(path):
            os.mkdir(path)

        pickle.dump(program, open(os.path.join(path, 'program.pkl'), "wb"))
        plot_utils.plotTree(nodes, edges, labels, "best", path)
        plot_utils.plotTrends(logbook, "best", path)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="NEAT Spaceship")
    parser.add_argument("--run_best_neat", action="store_true", help="Run the best individual found using NEAT")
    parser.add_argument("--run_best_gp", action="store_true", help="Run the best individual found using GP")
    parser.add_argument("--neat", action="store_true", help="Run the NEAT algorithm for training of the NN")
    parser.add_argument("--gp", action="store_true", help="Run the GP algorithm for finding a program")
    parser.add_argument("--config_file", type=str, default=None, help="Configuration file")
    parser.add_argument("--num_runs", type=int, default=1, help="The number of runs")
    parser.add_argument("--num_generations", type=int, default=10, help="The number of generations for each run")
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.neat:
        # Load configuration.
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, args.config_file) if args.config_file else 'configNEAT.txt'
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

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
                print(e)
                traceback.print_exc()
                genome = p.best_genome

            # Display the winning genome.
            print(f"\nBest genome:\n{genome}")

            # Create the winning network.
            network = neat.nn.FeedForwardNetwork.create(genome, config)

            # Simulate the game with the winning network and showing it.
            best_fitness = simulate_game(show_game=True, name="NEAT Spaceship!", net=network)
            print(f"\nBest fitness simulation:\n{best_fitness}")

            save_best_neat(genome, network, config, stats)

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

                    # Create the winning network.
                    network = neat.nn.FeedForwardNetwork.create(genome, config)

                    save_best_neat(genome, network, config, stats)

                    # Store best fitness for statistical analysis.
                    best_fitnesses.append(genome.fitness)

            except Exception as e:
                print(e)
                traceback.print_exc()

            results.append(best_fitnesses)
            fig = figure("NEAT-Spaceship")
            ax = fig.gca()
            ax.boxplot(results)
            ax.set_ylabel("Best fitness")
            show()

    if args.run_best_neat:
        genome, network = load_best_neat()
        if network is None:
            print("network not present")
        else:
            simulate_game(show_game=True, name="NEAT Spaceship!", net=network)


    if args.gp or args.run_best_gp:
        agent = AgentSimulator()

        pset = gp.PrimitiveSetTyped("MAIN", [float] * 11, Output)
        pset.addPrimitive(if_then_else, [bool, float, float], float)
        pset.addPrimitive(if_then_else, [bool, Output, Output], Output)
        # pset.addPrimitive(operator.add, 2)
        # pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(operator.gt, [float, float], bool)
        pset.addPrimitive(operator.eq, [float, float], bool)
        pset.addPrimitive(operator.and_, [bool, bool], bool)
        pset.addPrimitive(operator.or_, [bool, bool], bool)
        pset.addPrimitive(operator.neg, [bool], bool)
        pset.addPrimitive(operator.add, [float, float], float)
        pset.addPrimitive(operator.sub, [float, float], float)
        pset.addPrimitive(operator.mul, [float, float], float)

        # pset.addPrimitive(eval_function, [dict], float)
        # pset.addPrimitive(exec2, 2)
        # pset.addPrimitive(exec3, 3)
        # pset.addPrimitive(exec_while, 2)
        # pset.addTerminal(agent.action_left)
        # pset.addTerminal(agent.action_left_and_fire)
        # pset.addTerminal(agent.action_still)
        # pset.addTerminal(agent.action_still_and_fire)
        # pset.addTerminal(agent.action_right)
        # pset.addTerminal(agent.action_right_and_fire)
        # pset.addTerminal(laser_distance, dict)
        pset.addTerminal(5.0, float)
        pset.addTerminal(10.0, float)
        pset.addTerminal(15.0, float)
        pset.addTerminal(20.0, float)
        pset.addTerminal(25.0, float)
        pset.addTerminal(30.0, float)
        pset.addTerminal(A, Output)
        pset.addTerminal(B, Output)
        pset.addTerminal(C, Output)
        pset.addTerminal(D, Output)
        pset.addTerminal(E, Output)
        pset.addTerminal(F, Output)
        pset.addTerminal(True, bool)
        pset.addTerminal(False, bool)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

        if args.gp:
            config_file = args.config_file if args.config_file else 'configGP.txt'
            config = configparser.ConfigParser() # TODO: decide where to put num_runs and num_generations
            config.read(config_file)
            num_runs = int(config['GP']['num_runs'])
            num_generations = int(config['GP']['num_generations'])
            pop_size = int(config['GP']['pop_size'])
            mating_prob = float(config['GP']['mating_prob'])
            mutation_prob = float(config['GP']['mutation_prob'])
            tournament_size = int(config['GP']['tournament_size'])
            hof_size = int(config['GP']['hof_size'])

            toolbox = base.Toolbox()

            # Attribute generator
            toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=3)
            # Structure initializers
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            toolbox.register("evaluate", evalArtificialAgent)
            toolbox.register("select", tools.selTournament, tournsize=tournament_size)
            toolbox.register("mate", gp.cxOnePoint)
            toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

            if num_runs == 1:
                pop = toolbox.population(n=pop_size)
                hof = tools.HallOfFame(hof_size)
                stats = tools.Statistics(lambda ind: ind.fitness.values)
                stats.register("avg", numpy.mean)
                stats.register("std", numpy.std)
                stats.register("min", numpy.min)
                stats.register("max", numpy.max)

                try:
                    final_pop, logbook = algorithms.eaSimple(pop, toolbox, mating_prob, mutation_prob, num_generations, stats, halloffame=hof)
                except Exception as e:
                    print(e)
                    traceback.print_exc()

                print("Best individual GP is: %s, with fitness: %s" % (hof[0], hof[0].fitness.values[0]))
                save_best_gp(hof[0])  # TODO control the size of the tree

                # Run the best routine
                routine = gp.compile(hof[0], pset)
                simulate_game(show_game=True, name="GP Spaceship!", program=agent, routine=routine)

            else:
                results = []
                best_fitnesses = []
                try:
                    for i in range(num_runs):
                        print(f"run {i + 1}/{num_runs}")

                        pop = toolbox.population(n=pop_size)
                        hof = tools.HallOfFame(hof_size)
                        stats = tools.Statistics(lambda ind: ind.fitness.values)
                        stats.register("avg", numpy.mean)
                        stats.register("std", numpy.std)
                        stats.register("min", numpy.min)
                        stats.register("max", numpy.max)

                        final_pop, logbook = algorithms.eaSimple(pop, toolbox, mating_prob, mutation_prob, num_generations, stats, halloffame=hof)
                        print("Best individual GP is: %s, with fitness: %s" % (hof[0], hof[0].fitness.values[0]))

                        save_best_gp(hof[0])

                        # Store best fitness for statistical analysis.
                        best_fitnesses.append(hof[0].fitness.values[0])

                except Exception as e:
                    print(e)
                    traceback.print_exc()

                results.append(best_fitnesses)
                fig = figure("GP-Spaceship")
                ax = fig.gca()
                ax.boxplot(results)
                ax.set_ylabel("Best fitness")
                show()

        if args.run_best_gp:
            # Run the best routine
            program = load_best_gp()
            if program is None:
                print("program not present")
            else:
                routine = gp.compile(program, pset)  # TODO store only the routine and avoid to compile it
                simulate_game(show_game=True, name="GP Spaceship!", program=agent, routine=routine)
