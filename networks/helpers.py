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
