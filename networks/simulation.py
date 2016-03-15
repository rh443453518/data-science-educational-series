import matplotlib
matplotlib.use('TkAgg')
from pylab import *
from helpers import *

def initialize():
    global sim 
    graph = FileIO.read_dolphins();
    sim = SimulatorAsync(graph, Epidemic.randomized_infection(0.1), 
                     Epidemic.randomized_update(0.2, 0.4));

def observe():
    global sim
    cla()
    nx.draw(sim.graph, pos = sim.pos, nodelist=sim.graph.nodes(), vmin = 0, vmax = 1,
        node_color=[sim.graph.node[i]['state'] for i in sim.graph.nodes()], 
        node_size=200, cmap=plt.cm.plasma, alpha = 0.8)

def update():
    global sim
    sim.simulate_step();

import pycxsimulator
pycxsimulator.GUI().start(func = [initialize, observe, update]);




