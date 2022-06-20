from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from functools import partial

import time, random

#---------------------------------------------------------------------------------------------
GP_POP_SIZE = 500               # population size for GP
GP_NGEN = 60                    # number of generations for GP
GP_CXPB, GP_MUTPB = 0.5, 0.2    # crossover and mutation probability for GP
GP_TRNMT_SIZE = 7               # tournament size for GP
GP_HOF_SIZE = 2                 # size of the Hall-of-Fame for GP
#---------------------------------------------------------------------------------------------

K_LEFT, K_RIGHT, K_SPACE = 1073741904, 1073741903, 32

class AgentSimulator(object):
    def __init__(self, max_moves):
        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.keys = {
            K_LEFT: False,
            K_RIGHT: False,
            K_SPACE: False
        }
            
    def left(self): 
        if self.moves < self.max_moves:
            self.keys[K_LEFT] = True

    def right(self):
        if self.moves < self.max_moves:
            self.keys[K_RIGHT] = True
        
    def fire(self):
        if self.moves < self.max_moves:
            self.keys[K_SPACE] = True

    def if_laser_threat(self, out1, out2):
        pass


    def run(self,routine):
        self._reset()
        while self.moves < self.max_moves:
            routine()
            

def exec2(f1, f2):
    f1()
    f2()

def exec3(f1, f2, f3):
    f1()
    f2()
    f3()

def exec_while(condition, f):
    while(condition()):
        f()

agent = AgentSimulator(100000)

pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(agent.if_laser_threat, 2)
pset.addPrimitive(exec2, 2)
pset.addPrimitive(exec3, 3)
pset.addPrimitive(exec_while, 2)
pset.addTerminal(agent.fire)
pset.addTerminal(agent.left)
pset.addTerminal(agent.right)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalArtificialAgent(individual):
    # Transform the tree expression to functionnal Python code
    routine = gp.compile(individual, pset)
    # Run the generated routine
    agent.run(routine)
    return agent.eaten,

toolbox.register("evaluate", evalArtificialAgent)
toolbox.register("select", tools.selTournament, tournsize=GP_TRNMT_SIZE)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    seed = int(time.time())
    random.seed(seed)
    
    pop = toolbox.population(n=GP_POP_SIZE)
    hof = tools.HallOfFame(GP_HOF_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    final_pop,logbook=algorithms.eaSimple(pop, toolbox, GP_CXPB, GP_MUTPB, GP_NGEN, \
                                          stats, halloffame=hof)

    #--------------------------------------------------------------------

    # plot GP tree
    import plot_utils as plot_utils
    nodes, edges, labels = gp.graph(hof[0])
    plot_utils.plotTree(nodes,edges,labels,sys.argv[0][0:-3]+'_'+str(seed),'results')

    # plot fitness trends
    plot_utils.plotTrends(logbook,sys.argv[0][0:-3]+'_'+str(seed),'results')
    
    #--------------------------------------------------------------------

    print("Best individual GP is %s, %s" % (hof[0], hof[0].fitness.values))


if __name__ == "__main__":
    main()