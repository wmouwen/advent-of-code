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
    nodes = []

    for line in sys.stdin:
        if match := re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%', line.strip()):
            nodes.append(Node(*map(int, match.groups())))

    print(sum(a != b and 0 < a.used <= b.available for a in nodes for b in nodes))


if __name__ == '__main__':
    main()
