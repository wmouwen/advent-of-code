import sys
import networkx as nx
from networkx.algorithms.clique import enumerate_all_cliques


def main():
    graph = nx.Graph()

    for line in sys.stdin:
        if line.strip() == '':
            break
        graph.add_edge(*line.strip().split('-'))

    chief_candidate_count = 0
    lan_party = None

    for clique in enumerate_all_cliques(graph):
        lan_party = clique

        if len(clique) == 3 and any(node[0] == 't' for node in clique):
            chief_candidate_count += 1

    print(chief_candidate_count)
    print(','.join(sorted(lan_party)))


if __name__ == '__main__':
    main()
