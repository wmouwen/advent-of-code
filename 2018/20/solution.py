import sys
from collections import defaultdict
from queue import Queue


dirs = {'E': 1, 'N': 1j, 'W': -1, 'S': -1j}


def calc_distances(graph):
    distances = {0: 0}
    queue = Queue()
    queue.put(0)

    while not queue.empty():
        v = queue.get()
        for n in graph[v]:
            if n not in distances:
                distances[n] = distances[v] + 1
                queue.put(n)

    return distances


def main():
    graph = defaultdict(set)
    current = {0}
    state_at_depth = []
    starts, ends = current, set()

    for char in sys.stdin.readline().strip():
        if char in 'NESW':
            d = dirs[char]

            for v in current:
                graph[v].add(v + d)
                graph[v + d].add(v)

            current = {v + d for v in current}

        if char == '(':
            state_at_depth.append((starts, ends))
            starts, ends = current, set()

        if char == '|':
            ends.update(current)
            current = starts

        if char == ')':
            current.update(ends)
            starts, ends = state_at_depth.pop()

    distances = calc_distances(graph)

    print(max(distances.values()))
    print(sum(1 for dist in distances.values() if dist >= 1000))


if __name__ == '__main__':
    main()
