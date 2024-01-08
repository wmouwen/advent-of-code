import random
import sys

from networkx import DiGraph, minimum_cut

graph = DiGraph()

for line in sys.stdin:
    source, destinations = line.strip().split(': ')

    for destination in destinations.split():
        graph.add_edge(source, destination, capacity=1)
        graph.add_edge(destination, source, capacity=1)

while True:
    source, destination = random.sample(list(graph.nodes), 2)

    cut_size, (group_source, group_destination) = minimum_cut(graph, source, destination)
    if cut_size == 3:
        print(len(group_source) * len(group_destination))
        break
