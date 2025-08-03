import sys
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


movements = [Vector(x=1, y=0), Vector(x=0, y=1), Vector(x=-1, y=0), Vector(x=0, y=-1)]

grid: list[list[int]] = []
summit: Vector | None = None
start: Vector | None = None

for line in sys.stdin:
    grid.append([])
    for field in line.strip():
        if field == 'S':
            grid[-1].append(0)
            start = Vector(x=len(grid[-1]) - 1, y=len(grid) - 1)
        elif field == 'E':
            grid[-1].append(25)
            summit = Vector(x=len(grid[-1]) - 1, y=len(grid) - 1)
        else:
            grid[-1].append(ord(field) - ord('a'))

assert isinstance(summit, Vector)
assert isinstance(start, Vector)

distances: list[list[int | None]] = [[None for _ in row] for row in grid]
distances[summit.y][summit.x] = 0

queue = Queue()
queue.put(summit)
while not queue.empty():
    location = queue.get()
    for movement in movements:
        next = Vector(x=location.x + movement.x, y=location.y + movement.y)
        if not 0 <= next.y < len(grid) or not 0 <= next.x < len(grid[next.y]):
            continue

        if distances[next.y][next.x] is not None:
            continue

        if grid[location.y][location.x] - grid[next.y][next.x] > 1:
            continue

        distances[next.y][next.x] = distances[location.y][location.x] + 1
        queue.put(next)

print(distances[start.y][start.x])

trails = (
    distance
    for y, row in enumerate(distances)
    for x, distance in enumerate(row)
    if distance is not None and grid[y][x] == 0
)
print(min(trails))
