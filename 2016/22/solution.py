import itertools
import re
import sys


class Node:
    def __init__(self, x: int, y: int, size: int, used: int, available: int):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.available = available


def main():
    nodes = {}

    for line in sys.stdin:
        if match := re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%', line.strip()):
            node = Node(*map(int, match.groups()))
            if node.y not in nodes:
                nodes[node.y] = {}
            nodes[node.y][node.x] = node

    all_nodes = set(itertools.chain.from_iterable(map(lambda row: row.values(), nodes.values())))
    print(sum(a != b and 0 < a.used <= b.available for a in all_nodes for b in all_nodes))

    # No node can contain data of two disks combined
    assert all(a.used + b.used > a.size and a.used + b.used > b.size
               for a in all_nodes if a.used > 0
               for b in all_nodes if b.used > 0 and a != b)

    # There is exactly one empty slot
    assert sum(node.used == 0 for node in all_nodes) == 1

    # Required data fits on target disk
    assert nodes[0][len(nodes[0]) - 1].used <= nodes[0][0].size

    # Manual solution for specific input:
    # slot: 7 left, 14 up, 13 right
    # data: 34 steps left
    # slot: 33 circle movements, 4 steps each, around data
    # TODO convert to computed result.
    print(7 + 14 + 14 + 34 + 4 * 33)


if __name__ == '__main__':
    main()
