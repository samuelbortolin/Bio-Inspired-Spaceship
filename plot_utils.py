from __future__ import print_function

import matplotlib.pyplot as plt
import importlib
import imp
import os

import copy
import warnings

import graphviz
import numpy as np


def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.png'):
    """ Plots the population's average and best fitness. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    fig = plt.figure("NEAT (Population's average/std. dev and best fitness)")

    plt.plot(generation, avg_fitness, 'b-', label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")

    # plt.title("Population's average/std. dev and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    plt.savefig(filename)
    if view:
        plt.show()
    else:
        plt.close(fig)


def plot_species(statistics, view=False, filename='speciation.png'):
    """ Visualizes speciation throughout evolution. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig = plt.figure("NEAT (speciation)")
    ax = fig.add_subplot(111)
    ax.stackplot(range(num_generations), *curves)

    # plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.savefig(filename)

    if view:
        plt.show()
        fig = None
    else:
        plt.close(fig)

    return fig


def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False, node_colors=None, fmt='png'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    # Attributes for network nodes.
    if graphviz is None:
        warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
        return

    if node_names is None:
        node_names = {}

    assert type(node_names) is dict

    if node_colors is None:
        node_colors = {}

    assert type(node_colors) is dict

    node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'}

    dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled', 'shape': 'box', 'fillcolor': node_colors.get(k, 'lightgray')}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'lightblue')}
        dot.node(name, _attributes=node_attrs)

    if prune_unused:
        connections = set()
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                connections.add((cg.in_node_id, cg.out_node_id))

        used_nodes = copy.copy(outputs)
        pending = copy.copy(outputs)
        while pending:
            new_pending = set()
            for a, b in connections:
                if b in pending and a not in used_nodes:
                    new_pending.add(a)
                    used_nodes.add(a)
            pending = new_pending
    else:
        used_nodes = set(genome.nodes.keys())

    for n in used_nodes:
        if n in inputs or n in outputs:
            continue

        attrs = {'style': 'filled', 'fillcolor': node_colors.get(n, 'white')}
        dot.node(str(n), _attributes=attrs)

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            # if cg.input not in used_nodes or cg.output not in used_nodes:
            #     continue
            input_key, output_key = cg.key
            a = node_names.get(input_key, str(input_key))
            b = node_names.get(output_key, str(output_key))
            style = 'solid' if cg.enabled else 'dotted'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    dot.render(filename, view=view)
    return dot


def plot_trends(logbook, name, view=False, folder=None):
    gen = logbook.select("gen")
    fit_min = logbook.select("min")
    fit_max = logbook.select("max")
    fit_avg = logbook.select("avg")
    fit_std = logbook.select("std")

    # plt.title("Genetic Programming (fitness trend)")
    fig = plt.figure("Genetic Programming (fitness trend)")
    ax1 = fig.add_subplot(111)
    ax1.plot(gen, fit_min, label="Min")
    ax1.plot(gen, fit_max, label="Max")
    ax1.errorbar(gen, fit_avg, yerr=fit_std, label="Avg")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.set_xlim(0, len(gen) - 1)
    ax1.legend()
    plt.savefig(folder + '/' + 'trends_' + name + '.png')

    if view:
        plt.show()
    else:
        plt.close(fig)


def plot_tree(nodes, edges, labels, name, view=False, folder=None):
    if folder is not None and not os.path.exists(folder):
        os.makedirs(folder)

    if import_module('pygraphviz'):
        import pygraphviz as pgv
        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog='dot')
        for i in nodes:
            n = g.get_node(i)
            n.attr['label'] = labels[i]
        g.draw(folder + '/' + 'tree_' + name + '.pdf')

    if import_module('networkx'):
        import networkx as nx
        fig = plt.figure("GP (best tree)")
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        pos = nx.nx_agraph.graphviz_layout(g, prog='dot')
        nx.draw_networkx_nodes(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos, labels)
        plt.savefig(folder + '/' + 'tree_' + name + '.png')

        if view:
            plt.show()
        else:
            plt.close(fig)


def import_module(module):
    try:
        imp.find_module(module)
        found = True
        importlib.import_module(module)
    except ImportError:
        found = False
    return found
