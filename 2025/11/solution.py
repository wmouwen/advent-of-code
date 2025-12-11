import re
import sys
from collections import defaultdict
from queue import Queue


def find_paths(edges: dict[str, set[str]], source: str, sink: str) -> list[list[str]]:
    paths = []

    queue = Queue()
    queue.put((source, [source]))

    while not queue.empty():
        node, path = queue.get()

        print(queue.qsize())

        for neighbor in edges[node]:
            if neighbor == sink:
                paths.append(path + [sink])
            elif neighbor not in path:
                queue.put((neighbor, path + [neighbor]))

    return paths


def main():
    edges = defaultdict(set)

    for line in sys.stdin:
        if match := re.match(r'(\w+): ([\w ]+)', line):
            edges[match[1]] = set(match[2].split())

    print(len(find_paths(edges, 'you', 'out')))


if __name__ == '__main__':
    main()
