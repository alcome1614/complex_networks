import pycxsimulator
from pylab import *
import networkx as nx
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prob', action='store', 
    help="shows output")

args = parser.parse_args()

prob = float(args.prob)

def initialize():
    global g, nextg
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes_iter():
        g.node[i]['state'] = 1 if random() < .5 else 0
    nextg = g.copy()
    nextg.pos = g.pos
    
def observe():
    global g, nextg
    cla()
    nx.draw(g, cmap = cm.bwr, vmin = 0, vmax = 1,
            node_color = [g.node[i]['state'] for i in g.nodes_iter()],
            pos = g.pos)

def update():
    global g, nextg
    for i in g.nodes_iter():
        count = g.node[i]['state']
        for j in g.neighbors(i):
            count += g.node[j]['state']
        ratio = count / (g.degree(i) + 1.0)
        state = 1 if ratio > .5 else 0
        if random() < prob:
            state =  0 if state else 1
        nextg.node[i]['state'] = state
    g, nextg = nextg, g

pycxsimulator.GUI().start(func=[initialize, observe, update])