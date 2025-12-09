import sys
from itertools import combinations
from typing import Self, NamedTuple


class Tile(NamedTuple):
    x: int
    y: int

    def area(self, other: Self) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


def main():
    boxes = [Tile(*map(int, line.strip().split(','))) for line in sys.stdin]

    print(max(a.area(b) for a, b in combinations(boxes, 2)))


if __name__ == '__main__':
    main()
