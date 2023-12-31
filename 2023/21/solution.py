import sys
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> list:
        return [
            Vector(self.x + 1, self.y + 0),
            Vector(self.x + 0, self.y + 1),
            Vector(self.x - 1, self.y + 0),
            Vector(self.x + 0, self.y - 1)
        ]


Grid = list[list]


def find_start(grid: Grid) -> Vector:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                return Vector(x=x, y=y)

    raise Exception('No starting location found in the grid')


def flood_fill(grid: Grid) -> Grid:
    distances = [[None for _ in row] for row in grid]
    queue = Queue()

    start = find_start(grid)
    queue.put(start)
    distances[start.y][start.x] = 0

    while not queue.empty():
        current = queue.get()
        for neighbor in current.neighbors():
            if (0 <= neighbor.y < len(grid)
                    and 0 <= neighbor.x < len(grid[neighbor.y])
                    and grid[neighbor.y][neighbor.x] != '#'
                    and distances[neighbor.y][neighbor.x] is None):
                distances[neighbor.y][neighbor.x] = distances[current.y][current.x] + 1
                queue.put(neighbor)

    return distances


grid = [list(line.strip()) for line in sys.stdin]

distances = flood_fill(grid)
print(sum(1 for row in distances for distance in row if distance is not None and distance <= 64 and not distance % 2))
