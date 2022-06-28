# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import importlib
import imp
import os


def plot_trends(logbook, name, folder=None):
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
    plt.show()


def plot_tree(nodes, edges, labels, name, folder=None):
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
        plt.figure("GP (best tree)")
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        pos = nx.nx_agraph.graphviz_layout(g, prog='dot')
        nx.draw_networkx_nodes(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos, labels)
        plt.savefig(folder + '/' + 'tree_' + name + '.png')
        plt.show()


def import_module(module):
    try:
        imp.find_module(module)
        found = True
        importlib.import_module(module)
    except ImportError:
        found = False
    return found
