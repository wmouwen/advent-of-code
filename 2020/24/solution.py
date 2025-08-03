import re
import sys
from collections import defaultdict
from functools import reduce
from typing import NamedTuple


class V(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return V(x=self.x + other.x, y=self.y + other.y)


directions = {
    'e': V(x=2, y=0),
    'se': V(x=1, y=1),
    'sw': V(x=-1, y=1),
    'w': V(x=-2, y=0),
    'nw': V(x=-1, y=-1),
    'ne': V(x=1, y=-1),
}


def evolve(tiles):
    black_tiles, white_tiles = defaultdict(int), defaultdict(int)

    for tile in tiles:
        for direction in directions.values():
            neighbor = tile + direction

            if neighbor in tiles:
                black_tiles[tile] += 1
            else:
                white_tiles[neighbor] += 1

    return (
        {
            tile
            for tile, active_neighbors in black_tiles.items()
            if 1 <= active_neighbors <= 2
        }
    ).union(
        {
            tile
            for tile, active_neighbors in white_tiles.items()
            if active_neighbors == 2
        }
    )


def main():
    flipped = set()

    for line in sys.stdin:
        tile = reduce(
            lambda carry, move: carry + directions[move],
            re.findall(r'[ns]?[ew]', line.strip()),
            V(0, 0),
        )

        if tile in flipped:
            flipped.remove(tile)
        else:
            flipped.add(tile)

    print(len(flipped))

    for _ in range(100):
        flipped = evolve(flipped)

    print(len(flipped))


if __name__ == '__main__':
    main()
