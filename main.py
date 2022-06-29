import shutil

from pylab import *

import argparse
import configparser
import operator
import os
import sys
import pickle
import traceback

import pygame
import neat
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import gamerun
import plot_utils
import visualize

from gp_train import if_then_else, Output, A, B, C, D, E, F


def simulate_game(show_game, name="", net=None, routine=None):
    win = gamerun.initialize(show_game, name)

    game = True
    while game:
        result = gamerun.run(win, net=net, routine=routine)
        if result == 0:
            game = False

    if gamerun.show_game:
        pygame.quit()

    fitness = gamerun.alien_kills * 10 + gamerun.spaceship_kills * 50 + gamerun.battleship_healths[-1]/10.0

    print(f"{fitness} -> {gamerun.level} {gamerun.alien_kills} {gamerun.spaceship_kills} {gamerun.frames} {gamerun.battleship_healths}")
    # TODO valutare se rimuove il numero di frame dal fitness? (kind of penalty for escaping?)
    # TODO magari valutare i colpi dati ai nemici (da massimizzare) e minimizzare quelli andati a vuoto?
    # TODO magari valutare i colpi presi dai nemici (da minimizzare, i.e., subirli più avanti in livelli più complessi)?
    return fitness


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulate_game(show_game=False, net=net)


def eval_program(program):
    # Transform the tree expression to functionnal Python code
    routine = gp.compile(program, pset)
    # Run the generated routine
    return simulate_game(show_game=False, routine=routine),


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
        best_dirname = 'runs/NEAT/best/'
        if not os.path.isdir(best_dirname):
            os.mkdir(best_dirname)

        shutil.copytree(dirname, best_dirname)


def load_best_gp():
    program = None
    path = 'runs/GP/best/'
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if 'program' in filename:
                program = pickle.load(open(os.path.join(path, filename), "rb"))

    return program


def save_best_gp(program, logbook):
    now = f"{datetime.datetime.now().isoformat()}".replace(':', '.')
    dirname = f"runs/GP/{now}_fitness_{program.fitness.values[0]}"
    os.mkdir(dirname)
    pickle.dump(program, open(os.path.join(dirname, 'program.pkl'), "wb"))
    nodes, edges, labels = gp.graph(program)
    plot_utils.plot_tree(nodes, edges, labels, "best", dirname)
    if logbook is not None:
        plot_utils.plot_trends(logbook, "best", dirname)

    best_program = load_best_gp()
    if best_program is None or best_program.fitness.values[0] < program.fitness.values[0]:
        best_dirname = 'runs/GP/best/'
        if not os.path.isdir(best_dirname):
            os.mkdir(best_dirname)

        shutil.copytree(dirname, best_dirname)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Bio Inspired Spaceship")
    parser.add_argument("--run_best_neat", action="store_true", help="Run the best individual found using NEAT")
    parser.add_argument("--run_best_gp", action="store_true", help="Run the best individual found using GP")
    parser.add_argument("--neat", action="store_true", help="Run the NEAT algorithm for training of the NN")
    parser.add_argument("--gp", action="store_true", help="Run the GP algorithm for finding a program")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.neat:
        # Load configuration.
        config_file = 'configNEAT.txt'
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        num_runs = int(config_parser['RUNS']['num_runs'])
        num_generations = int(config_parser['GENERATIONS']['num_generations'])
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

        if num_runs == 1:
            # Create the population.
            p = neat.Population(config)

            # Add a stdout reporter to show progress in the terminal.
            stats = neat.StatisticsReporter()
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(stats)

            # Run NEAT for num_generations.
            try:
                genome = p.run(eval_genomes, num_generations)
            except (Exception, KeyboardInterrupt) as e:
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
                for i in range(num_runs):
                    print(f"run {i + 1}/{num_runs}")

                    # Create the population.
                    p = neat.Population(config)

                    # Add a stdout reporter to show progress in the terminal.
                    stats = neat.StatisticsReporter()
                    p.add_reporter(neat.StdOutReporter(True))
                    p.add_reporter(stats)

                    # Run NEAT for num_generations.
                    genome = p.run(eval_genomes, num_generations)

                    # Display the winning genome.
                    print(f"\nBest genome:\n{genome}")

                    # Create the winning network.
                    network = neat.nn.FeedForwardNetwork.create(genome, config)

                    save_best_neat(genome, network, config, stats)

                    # Store best fitness for statistical analysis.
                    best_fitnesses.append(genome.fitness)

            except (Exception, KeyboardInterrupt) as e:
                print(e)
                traceback.print_exc()

            results.append(best_fitnesses)
            fig = figure("NEAT-Spaceship")
            ax = fig.gca()
            ax.boxplot(results)
            ax.set_ylabel("Best fitness")
            show()

    if args.run_best_neat:
        _, network = load_best_neat()
        if network is None:
            print("network not present")
        else:
            simulate_game(show_game=True, name="NEAT Spaceship!", net=network)

    if args.gp or args.run_best_gp:
        pset = gp.PrimitiveSetTyped("MAIN", [float] * 11, Output)
        pset.addPrimitive(if_then_else, [bool, float, float], float)
        pset.addPrimitive(if_then_else, [bool, Output, Output], Output)
        pset.addPrimitive(operator.gt, [float, float], bool)
        pset.addPrimitive(operator.eq, [float, float], bool)
        pset.addPrimitive(operator.and_, [bool, bool], bool)
        pset.addPrimitive(operator.or_, [bool, bool], bool)
        pset.addPrimitive(operator.neg, [bool], bool)
        pset.addPrimitive(operator.add, [float, float], float)
        pset.addPrimitive(operator.sub, [float, float], float)
        pset.addPrimitive(operator.mul, [float, float], float)

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
            config_file = 'configGP.txt'
            config = configparser.ConfigParser()
            config.read(config_file)
            num_runs = int(config['RUNS']['num_runs'])
            num_generations = int(config['GENERATIONS']['num_generations'])
            pop_size = int(config['GP']['pop_size'])
            crossover_prob = float(config['GP']['crossover_prob'])
            mutation_prob = float(config['GP']['mutation_prob'])
            tournament_size = int(config['GP']['tournament_size'])
            hof_size = int(config['GP']['hof_size'])
            max_tree_size = int(config['GP']['max_tree_size'])

            toolbox = base.Toolbox()

            # Attribute generator
            toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=3)

            # Structure initializers
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            toolbox.register("evaluate", eval_program)
            toolbox.register("select", tools.selTournament, tournsize=tournament_size)
            toolbox.register("mate", gp.cxOnePoint)
            toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

            # BLOAT control
            toolbox.decorate("mate", gp.staticLimit(operator.attrgetter("height"), max_tree_size))
            toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter("height"), max_tree_size))

            if num_runs == 1:
                pop = toolbox.population(n=pop_size)
                hof = tools.HallOfFame(hof_size)
                stats = tools.Statistics(lambda ind: ind.fitness.values)
                stats.register("avg", numpy.mean)
                stats.register("std", numpy.std)
                stats.register("min", numpy.min)
                stats.register("max", numpy.max)

                try:
                    final_pop, logbook = algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, num_generations, stats, halloffame=hof)
                except (Exception, KeyboardInterrupt) as e:
                    print(e)
                    traceback.print_exc()
                    logbook = None

                print("Best individual GP is: %s, with fitness: %s" % (hof[0], hof[0].fitness.values[0]))
                save_best_gp(hof[0], logbook)

                # Run the best routine
                routine = gp.compile(hof[0], pset)
                simulate_game(show_game=True, name="GP Spaceship!", routine=routine)

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

                        final_pop, logbook = algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, num_generations, stats, halloffame=hof)
                        print("Best individual GP is: %s, with fitness: %s" % (hof[0], hof[0].fitness.values[0]))
                        save_best_gp(hof[0], logbook)

                        # Store best fitness for statistical analysis.
                        best_fitnesses.append(hof[0].fitness.values[0])

                except (Exception, KeyboardInterrupt) as e:
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
                routine = gp.compile(program, pset)
                simulate_game(show_game=True, name="GP Spaceship!", routine=routine)
