import sys
from collections import namedtuple

Galaxy = namedtuple('Galaxy', ['y', 'x'])


def distance(a: Galaxy, b: Galaxy, empty_rows: list[int], empty_cols: list[int]) -> int:
    return (abs(a.x - b.x)
            + abs(a.y - b.y)
            + sum(1 for row in empty_rows if min(a.y, b.y) < row < max(a.y, b.y))
            + sum(1 for col in empty_cols if min(a.x, b.x) < col < max(a.x, b.x))
            )


grid = [line.strip() for line in sys.stdin]
galaxies = []

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x] == '#':
            galaxies.append(Galaxy(y=y, x=x))

empty_rows = [y for y in range(len(grid)) if y not in map(lambda galaxy: galaxy.y, galaxies)]
empty_cols = [x for x in range(len(grid[0])) if x not in map(lambda galaxy: galaxy.x, galaxies)]

total_distance = 0

for i in range(len(galaxies) - 1):
    for j in range(i + 1, len(galaxies)):
        assert i != j

        total_distance += distance(galaxies[i], galaxies[j], empty_rows=empty_rows, empty_cols=empty_cols)

# TODO FIXME something is off
print(total_distance)
