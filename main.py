from pylab import *

import argparse
import configparser
import operator
import sys
import traceback

import neat
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from gp_train import if_then_else, Output, A, B, C, D, E, F
from utils import eval_genomes, simulate_game, save_best_neat, load_best_neat, eval_program, save_best_gp, load_best_gp


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

            save_best_neat(genome, network, config, stats)

            # Simulate the game with the winning network and showing it.
            best_fitness = simulate_game(show_game=True, name="NEAT Spaceship!", net=network)
            print(f"\nBest fitness simulation:\n{best_fitness}")

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
        primitive_set = gp.PrimitiveSetTyped("MAIN", [float] * 9, Output)
        primitive_set.addPrimitive(if_then_else, [bool, float, float], float)
        primitive_set.addPrimitive(if_then_else, [bool, Output, Output], Output)
        primitive_set.addPrimitive(operator.gt, [float, float], bool)
        primitive_set.addPrimitive(operator.eq, [float, float], bool)
        primitive_set.addPrimitive(operator.and_, [bool, bool], bool)
        primitive_set.addPrimitive(operator.or_, [bool, bool], bool)
        primitive_set.addPrimitive(operator.neg, [bool], bool)
        primitive_set.addPrimitive(operator.add, [float, float], float)
        primitive_set.addPrimitive(operator.sub, [float, float], float)
        primitive_set.addPrimitive(operator.mul, [float, float], float)

        primitive_set.addTerminal(5.0, float)
        primitive_set.addTerminal(10.0, float)
        primitive_set.addTerminal(15.0, float)
        primitive_set.addTerminal(20.0, float)
        primitive_set.addTerminal(25.0, float)
        primitive_set.addTerminal(30.0, float)
        primitive_set.addTerminal(A, Output)
        primitive_set.addTerminal(B, Output)
        primitive_set.addTerminal(C, Output)
        primitive_set.addTerminal(D, Output)
        primitive_set.addTerminal(E, Output)
        primitive_set.addTerminal(F, Output)
        primitive_set.addTerminal(True, bool)
        primitive_set.addTerminal(False, bool)

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
            max_tree_height = int(config['GP']['max_tree_height'])

            toolbox = base.Toolbox()

            # Attribute generator
            toolbox.register("expr_init", gp.genFull, pset=primitive_set, min_=1, max_=3)

            # Structure initializers
            toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            toolbox.register("evaluate", eval_program, primitive_set=primitive_set)
            toolbox.register("select", tools.selDoubleTournament, fitness_size=tournament_size, parsimony_size=1.0, fitness_first=True)
            toolbox.register("mate", gp.cxOnePoint)
            toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
            toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=primitive_set)

            # BLOAT control
            toolbox.decorate("mate", gp.staticLimit(len, max_tree_size))
            toolbox.decorate("mutate", gp.staticLimit(len, max_tree_size))
            toolbox.decorate("mate", gp.staticLimit(operator.attrgetter("height"), max_tree_height))
            toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter("height"), max_tree_height))

            if num_runs == 1:
                pop = toolbox.population(n=pop_size)
                hof = tools.HallOfFame(hof_size)
                stats = tools.Statistics(lambda ind: ind.fitness.values)
                stats.register("avg", numpy.mean)
                stats.register("std", numpy.std)
                stats.register("min", numpy.min)
                stats.register("max", numpy.max)

                try:
                    final_pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, pop_size, pop_size, crossover_prob, mutation_prob, num_generations, stats, halloffame=hof)
                except (Exception, KeyboardInterrupt) as e:
                    print(e)
                    traceback.print_exc()
                    logbook = None

                print("Best individual GP is: %s, with fitness: %s" % (hof[0], hof[0].fitness.values[0]))
                save_best_gp(hof[0], logbook)

                # Run the best routine
                routine = gp.compile(hof[0], primitive_set)
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
                routine = gp.compile(program, primitive_set)
                simulate_game(show_game=True, name="GP Spaceship!", routine=routine)
