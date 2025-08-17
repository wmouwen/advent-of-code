import sys
from functools import cache
from operator import itemgetter
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    @cache
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)


DIRECTIONS = (
    Vector(x=0, y=-1),
    Vector(x=1, y=0),
    Vector(x=0, y=1),
    Vector(x=-1, y=0),
)


def read_input() -> tuple[Vector, set[Vector], Vector]:
    grid = [line.strip() for line in sys.stdin if line.strip()]

    grid_size = Vector(x=len(grid[0]), y=len(grid))
    walls = set(
        Vector(x=x, y=y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == '#'
    )
    start = next(
        Vector(x=x, y=y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == '^'
    )

    return grid_size, walls, start


def path_to_escape(
    grid_size: Vector,
    walls: set[Vector],
    start: tuple[Vector, int],
) -> set[tuple[Vector, int]] | None:
    path = {start}
    position, orientation = start

    while True:
        next_pos = position + DIRECTIONS[orientation]

        while next_pos in walls:
            orientation = (orientation + 1) % len(DIRECTIONS)
            next_pos = position + DIRECTIONS[orientation]

        if not (0 <= next_pos.y < grid_size.y and 0 <= next_pos.x < grid_size.x):
            break

        position = next_pos

        key = (position, orientation)
        if key in path:
            return None

        path.add(key)

    return path


def main():
    grid_size, walls, start = read_input()

    path = path_to_escape(grid_size, walls, (start, 0))
    positions = set(map(itemgetter(0), path))
    print(len(positions))

    loop_options = [
        position
        for position in positions
        if position != start
        and path_to_escape(grid_size, walls | {position}, (start, 0)) is None
    ]
    print(len(loop_options))


if __name__ == '__main__':
    main()
