import sys
from collections import namedtuple
from itertools import combinations

Vector = namedtuple('Vector', 'y x')


def main():
    grid = [list(line.strip()) for line in sys.stdin if line.strip() != '']
    y_max, x_max = len(grid) - 1, len(grid[0]) - 1

    antennas: dict[str, set[Vector]] = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '.':
                continue
            if cell not in antennas:
                antennas[cell] = set()
            antennas[cell].add(Vector(y=y, x=x))

    antinodes_close: set[Vector] = set()
    antinodes_all: set[Vector] = set()

    for antenna_set in antennas.values():
        for combination in combinations(antenna_set, 2):
            y_offset, x_offset = (
                combination[0].y - combination[1].y,
                combination[0].x - combination[1].x,
            )

            antinodes_close.add(
                Vector(y=combination[0].y + y_offset, x=combination[0].x + x_offset)
            )
            antinodes_close.add(
                Vector(y=combination[1].y - y_offset, x=combination[1].x - x_offset)
            )

            for k in range(-1 * max(y_max, x_max), max(y_max, x_max)):
                antinodes_all.add(
                    Vector(
                        y=combination[0].y + y_offset * k,
                        x=combination[0].x + x_offset * k,
                    )
                )

    print(
        len(
            list(
                filter(
                    lambda antinode: 0 <= antinode.x <= x_max
                    and 0 <= antinode.y <= y_max,
                    antinodes_close,
                )
            )
        )
    )
    print(
        len(
            list(
                filter(
                    lambda antinode: 0 <= antinode.x <= x_max
                    and 0 <= antinode.y <= y_max,
                    antinodes_all,
                )
            )
        )
    )


if __name__ == '__main__':
    main()
