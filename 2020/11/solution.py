import sys
from copy import deepcopy
from enum import Enum
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


directions = [
    Vector(x=-1, y=-1),
    Vector(x=0, y=-1),
    Vector(x=1, y=-1),
    Vector(x=1, y=0),
    Vector(x=1, y=1),
    Vector(x=0, y=1),
    Vector(x=-1, y=1),
    Vector(x=-1, y=0),
]


class FieldState(Enum):
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'


Grid = list[list[FieldState]]


def evolve(grid: Grid, max_distance: int | None) -> Grid:
    evolution = deepcopy(grid)

    for y, row in enumerate(grid):
        for x, field in enumerate(row):
            if field == FieldState.FLOOR:
                continue

            occupied_neighbors = 0
            for direction in directions:
                dx, dy = direction.x, direction.y

                while 0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y + dy]):
                    if max_distance is not None and (
                        abs(dx) > max_distance or abs(dy) > max_distance
                    ):
                        break

                    occupied_neighbors += grid[y + dy][x + dx] == FieldState.OCCUPIED

                    if grid[y + dy][x + dx] != FieldState.FLOOR:
                        break

                    dx, dy = dx + direction.x, dy + direction.y

            if field == FieldState.EMPTY and occupied_neighbors == 0:
                evolution[y][x] = FieldState.OCCUPIED
            elif field == FieldState.OCCUPIED and occupied_neighbors >= 5 - (
                max_distance is not None
            ):
                evolution[y][x] = FieldState.EMPTY

    return evolution


def grid_hash(grid: Grid) -> str:
    return '\n'.join(
        map(lambda row: ''.join(map(lambda field: field.value, row)), grid)
    )


initial_grid: Grid = [
    [
        FieldState.EMPTY if field == FieldState.EMPTY.value else FieldState.FLOOR
        for field in line
    ]
    for line in sys.stdin
]

grid = deepcopy(initial_grid)
prev_hash = grid_hash(grid)
while True:
    grid = evolve(grid, max_distance=1)
    new_hash = grid_hash(grid)
    if new_hash == prev_hash:
        break
    prev_hash = new_hash

print(sum(1 for line in grid for seat in line if seat == FieldState.OCCUPIED))

grid = deepcopy(initial_grid)
prev_hash = grid_hash(grid)
while True:
    grid = evolve(grid, max_distance=None)
    new_hash = grid_hash(grid)
    if new_hash == prev_hash:
        break
    prev_hash = new_hash

print(sum(1 for line in grid for seat in line if seat == FieldState.OCCUPIED))
