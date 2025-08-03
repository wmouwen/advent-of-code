import sys
from collections import namedtuple

Galaxy = namedtuple('Galaxy', 'x y')


def dist(
    a: Galaxy, b: Galaxy, empty_rows: list[int], empty_cols: list[int], multiplier: int
) -> int:
    return (
        abs(a.x - b.x)
        + abs(a.y - b.y)
        + sum(
            multiplier - 1 for row in empty_rows if min(a.y, b.y) < row < max(a.y, b.y)
        )
        + sum(
            multiplier - 1 for col in empty_cols if min(a.x, b.x) < col < max(a.x, b.x)
        )
    )


grid = [line.strip() for line in sys.stdin]
galaxies = [
    Galaxy(x=x, y=y)
    for y, row in enumerate(grid)
    for x, cell in enumerate(row)
    if cell == '#'
]
empty_rows = [y for y, row in enumerate(grid) if all(cell != '#' for cell in row)]
empty_cols = [x for x, col in enumerate(zip(*grid)) if all(cell != '#' for cell in col)]

print(
    sum(
        dist(a, b, empty_rows, empty_cols, 2)
        for i, a in enumerate(galaxies)
        for b in galaxies[:i]
    )
)
print(
    sum(
        dist(a, b, empty_rows, empty_cols, 1000000)
        for i, a in enumerate(galaxies)
        for b in galaxies[:i]
    )
)
