#helpers.py 
import networkx as nx
class FileIO:

    ''' returns a networkx undirected graph object representing the 
        dolphin social network in dolphins.txt'''
    @staticmethod
    def read_dolphins():
        fh = open("dolphins.txt");
        for line in fh:
            if (line.strip() == "*Edges"):
                break;
        graph = nx.Graph();
        for line in fh:
            edge = line.strip().split();
            graph.add_edge(int(edge[0]), int(edge[1]));
        return graph;

import random as rd
import matplotlib.pyplot as plt

''' an indicator variable that returns 1 with probability prob'''
def indicator(prob):
    if (rd.random() <= prob):
        return 1
    else:
        return 0;

class SimulatorAsync:
    '''
    init_func should be a function such that init_func: node -> [0, 1] w/ side 
        effects that manipulate state 
    update_func: a function such that update_func: node x graph -> nodelist
        side effects - state updates performed and nodelist is list of nodes that 
        were changed
    g is a graph
    '''
    def __init__(self, g, init_func, update_func):
        self.graph = g.copy();
        self.update_func = update_func
        self.pos = nx.spring_layout(g);
        self.marked = set();
        for i in self.graph.nodes():
            state = init_func(i, self.graph);
            if state==1:
                self.marked.add(i);


    
    '''
    simulate_step is a helper function that runs an asynchronous local update
        on a randomly selected vertex each time it's called
    '''
    def simulate_step(self):
        #select random vertex:
        node = rd.choice(list(self.marked));
        nodelist = self.update_func(node, self.graph);
        for i in nodelist:
            self.marked.add(i);
        if self.graph.node[node]['state'] == 0:
            self.marked.discard(node);
    
    def run_simulation(self, steps = 500):
        while(steps > 0):
            self.simulate_step();
            steps-=1;



'''Epidemic model class'''
class Epidemic:
    @staticmethod
    def randomized_infection(prob):
        def init_func(i, graph):
            graph.node[i]['state'] = indicator(prob);
            return graph.node[i]['state'];
        return init_func;
    
    @staticmethod
    def randomized_update(transmission_prob, return_prob):
        def update_func(i, graph):
            updatelist = [];
            prev = graph.node[i]['state'];
            if graph.node[i]['state'] == 1:
                graph.node[i]['state'] = indicator(1-return_prob);
                if prev != graph.node[i]['state']:
                    updatelist.append(i); 
            
            if graph.node[i]['state'] == 1:
                for j in graph.neighbors(i):
                    prev = graph.node[j]['state'];
                    graph.node[j]['state'] = indicator(transmission_prob) if graph.node[j]['state'] == 0 else 1;
                    if prev != graph.node[j]['state']:
                        updatelist.append(j);
            return updatelist;
        return update_func;
    