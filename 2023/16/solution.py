import sys
from functools import cache
from operator import itemgetter
from queue import Queue
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


@cache
def next_orientations(orientation: int, cell: str) -> set[int]:
    match cell:
        case '.':
            return {orientation}
        case '/':
            return {orientation ^ 1}
        case '\\':
            return {3 - orientation}
        case '|':
            return {0, 2} if orientation & 1 else {orientation}
        case '-':
            return {1, 3} if not orientation & 1 else {orientation}
        case _:
            raise ValueError(f'Unknown cell type: {cell}')


def beam(grid: list[str], start: tuple[Vector, int]) -> set[Vector]:
    queue: Queue[tuple[Vector, int]] = Queue()

    for next_orientation in next_orientations(start[1], grid[start[0].y][start[0].x]):
        queue.put((start[0], next_orientation))

    visited = set()

    while not queue.empty():
        position, orientation = queue.get()

        if (position, orientation) in visited:
            continue
        visited.add((position, orientation))

        next_pos = position + DIRECTIONS[orientation]
        if not (
            0 <= next_pos.y < len(grid) and 0 <= next_pos.x < len(grid[next_pos.y])
        ):
            continue

        cell = grid[next_pos.y][next_pos.x]
        for next_orientation in next_orientations(orientation, cell):
            queue.put((next_pos, next_orientation))

    return set(map(itemgetter(0), visited))


def main():
    grid = [line.strip() for line in sys.stdin]

    print(len(beam(grid, (Vector(x=0, y=0), 1))))

    best = 0
    for x in range(len(grid[0])):
        best = max(best, len(beam(grid, (Vector(x=x, y=0), 2))))
        best = max(best, len(beam(grid, (Vector(x=x, y=len(grid) - 1), 0))))
    for y in range(len(grid)):
        best = max(best, len(beam(grid, (Vector(x=0, y=y), 1))))
        best = max(best, len(beam(grid, (Vector(x=len(grid[y]) - 1, y=y), 3))))
    print(best)


if __name__ == '__main__':
    main()
