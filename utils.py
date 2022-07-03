from pylab import *

import os
import pickle
import shutil

import pygame
import neat

from deap import gp

import plot_utils
import run_game


def simulate_game(show_game, name="", net=None, routine=None):
    win = run_game.initialize(show_game, name)

    game = True
    while game:
        result = run_game.run(win, net=net, routine=routine)
        if result == 0:
            game = False

    if run_game.show_game:
        pygame.quit()

    fitness = run_game.alien_kills * 10 + \
        run_game.spaceship_kills * 50 + \
        sum([health / 50 for health in run_game.battleship_healths]) + \
        sum([((run_game.alien_health - alien.health) / run_game.alien_health) * 10 for alien in run_game.aliens]) + \
        sum([50 - enemy_spaceship.health for enemy_spaceship in run_game.enemy_spaceships])

    print(f"{fitness} -> {run_game.level} {run_game.alien_kills} {run_game.spaceship_kills} {run_game.frames} {run_game.battleship_healths} {sum([health / 50 for health in run_game.battleship_healths])} {sum([((run_game.alien_health - alien.health) / run_game.alien_health) * 10 for alien in run_game.aliens])} {sum([50 - enemy_spaceship.health for enemy_spaceship in run_game.enemy_spaceships])}")
    return fitness


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = simulate_game(show_game=False, net=net)


def eval_program(program, primitive_set):
    # Transform the tree expression to functional Python code
    routine = gp.compile(program, primitive_set)
    # Run the generated routine
    return simulate_game(show_game=False, routine=routine),


def load_best_neat():
    genome, network = None, None
    best_neat_path = 'runs/NEAT/best/'
    if os.path.isdir(best_neat_path):
        for filename in os.listdir('runs/NEAT/best/'):
            if 'network' in filename:
                network = pickle.load(open(os.path.join(best_neat_path, filename), "rb"))
            elif 'genome' in filename:
                genome = pickle.load(open(os.path.join(best_neat_path, filename), "rb"))

    return genome, network


def save_best_neat(genome, network, config, stats):
    now = f"{datetime.datetime.now().isoformat()}".replace(':', '.')
    dirname = f"runs/NEAT/{now}_fitness_{genome.fitness}"
    os.mkdir(dirname)
    pickle.dump(genome, open(os.path.join(dirname, 'genome.pkl'), "wb"))
    pickle.dump(network, open(os.path.join(dirname, 'network.pkl'), "wb"))
    plot_utils.draw_net(config, genome, filename=f"{dirname}/representation", view=False)
    plot_utils.plot_stats(stats, view=True, filename=f"{dirname}/avg_fitness.png")
    plot_utils.plot_species(stats, view=True, filename=f"{dirname}/speciation.png")
    pickle.dump(stats, open(os.path.join(dirname, 'stats.pkl'), "wb"))

    best_genome, _ = load_best_neat()
    if best_genome is None or best_genome.fitness < genome.fitness:
        best_dirname = 'runs/NEAT/best/'
        if not os.path.isdir(best_dirname):
            os.mkdir(best_dirname)

        shutil.copytree(dirname, best_dirname, dirs_exist_ok=True)


def load_best_gp():
    program = None
    best_gp_path = 'runs/GP/best/'
    if os.path.isdir(best_gp_path):
        for filename in os.listdir(best_gp_path):
            if 'program' in filename:
                program = pickle.load(open(os.path.join(best_gp_path, filename), "rb"))

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
        pickle.dump(logbook, open(os.path.join(dirname, 'logbook.pkl'), "wb"))

    best_program = load_best_gp()
    if best_program is None or best_program.fitness.values[0] < program.fitness.values[0]:
        best_dirname = 'runs/GP/best/'
        if not os.path.isdir(best_dirname):
            os.mkdir(best_dirname)

        shutil.copytree(dirname, best_dirname, dirs_exist_ok=True)
