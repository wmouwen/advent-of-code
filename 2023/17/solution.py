import sys
from queue import PriorityQueue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    x: int
    y: int
    direction: str
    consecutive: int


movements = {
    'R': Vector(x=1, y=0),
    'D': Vector(x=0, y=1),
    'L': Vector(x=-1, y=0),
    'U': Vector(x=0, y=-1)
}
turns = {
    'R': ['U', 'D'],
    'D': ['L', 'R'],
    'L': ['U', 'D'],
    'U': ['L', 'R'],
}


def min_heat_loss(grid: list[list[int]],
                  min_consecutive: int,
                  max_consecutive: int) -> int:
    best = [[[
        {direction: sys.maxsize for direction in movements.keys()}
        for _ in range(0, max_consecutive + 1)]
        for field in row]
        for row in grid]

    queue = PriorityQueue()
    queue.put((0, Move(x=0, y=0, direction='R', consecutive=0)))
    queue.put((0, Move(x=0, y=0, direction='D', consecutive=0)))

    while not queue.empty():
        heat_loss, move = queue.get()

        directions = []
        if move.consecutive < max_consecutive:
            directions.append(move.direction)
        if move.consecutive >= min_consecutive:
            directions.extend(turns[move.direction])

        for direction in directions:
            x, y = (move.x + movements[direction].x, move.y + movements[direction].y)

            if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
                new_move = Move(
                    x=x,
                    y=y,
                    direction=direction,
                    consecutive=move.consecutive + 1 if move.direction == direction else 1
                )
                new_heat_loss = heat_loss + grid[new_move.y][new_move.x]

                if new_heat_loss < best[new_move.y][new_move.x][new_move.consecutive][new_move.direction]:
                    best[new_move.y][new_move.x][new_move.consecutive][new_move.direction] = new_heat_loss
                    queue.put((new_heat_loss, new_move))

    return min(map(lambda d: min(d.values()), best[-1][-1][min_consecutive:]))


grid = [[int(field) for field in line.strip()] for line in sys.stdin]

print(min_heat_loss(grid=grid, min_consecutive=0, max_consecutive=3))
print(min_heat_loss(grid=grid, min_consecutive=4, max_consecutive=10))
