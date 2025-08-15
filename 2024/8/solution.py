import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, factor: int) -> 'Vector':
        return Vector(x=self.x * factor, y=self.y * factor)


def nodes_in_grid(grid: list[list[str]], antinodes: set[Vector]) -> set[Vector]:
    return {
        antinode
        for antinode in antinodes
        if 0 <= antinode.x < len(grid[0]) and 0 <= antinode.y < len(grid)
    }


def main():
    grid = [list(line.strip()) for line in sys.stdin if line.strip() != '']
    grid_size = max(len(grid), len(grid[0]))

    antennas = defaultdict(set)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '.':
                antennas[cell].add(Vector(y=y, x=x))

    antinodes_close, antinodes_all = set(), set()

    for antenna_set in antennas.values():
        for a, b in combinations(antenna_set, 2):
            offset = a - b
            antinodes_close.add(a + offset)
            antinodes_close.add(b - offset)

            for k in range(-1 * grid_size, grid_size):
                antinodes_all.add(a + offset * k)

    print(len(nodes_in_grid(grid, antinodes_close)))
    print(len(nodes_in_grid(grid, antinodes_all)))


if __name__ == '__main__':
    main()
