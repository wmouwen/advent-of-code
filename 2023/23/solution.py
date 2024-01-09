import sys
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


allowed_moves = {
    '>': [Vector(x=1, y=0)],
    'v': [Vector(x=0, y=1)],
    '<': [Vector(x=-1, y=0)],
    '^': [Vector(x=0, y=-1)],
    '.': [Vector(x=1, y=0), Vector(x=0, y=1), Vector(x=-1, y=0), Vector(x=0, y=-1)]
}


def find_longest(grid: tuple, start: Vector, goal: Vector, slippery: bool) -> int:
    longest = 0

    queue = Queue()
    queue.put((start, {start}))

    while not queue.empty():
        current, visited = queue.get()

        if current == goal:
            longest = max(longest, len(visited) - 1)
            continue

        for move in allowed_moves[grid[current.y][current.x] if slippery else '.']:
            next = Vector(x=current.x + move.x, y=current.y + move.y)

            if not 0 <= next.y < len(grid) or not 0 <= next.x < len(grid[next.y]):
                continue

            if grid[next.y][next.x] == '#' or next in visited:
                continue

            queue.put((next, visited.union({next})))

    return longest


grid = tuple(tuple(line.strip()) for line in sys.stdin)
start = Vector(x=1, y=0)
goal = Vector(x=len(grid[-1]) - 2, y=len(grid) - 1)

print(find_longest(grid=grid, start=start, goal=goal, slippery=True))

# TODO Optimize
# print(find_longest(grid=grid, start=start, goal=goal, slippery=False))
