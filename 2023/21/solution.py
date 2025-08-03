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
            Vector(self.x + 0, self.y - 1),
        ]


Grid = list[list[str | int | None]]


def find_start(grid: Grid) -> Vector:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                return Vector(x=x, y=y)

    raise Exception('No starting location found in the grid')


def flood_fill(grid: Grid) -> Grid:
    distances: Grid = [[None for _ in row] for row in grid]
    queue = Queue()

    start = find_start(grid)
    queue.put(start)
    distances[start.y][start.x] = 0

    while not queue.empty():
        current = queue.get()
        for neighbor in current.neighbors():
            if (
                0 <= neighbor.y < len(grid)
                and 0 <= neighbor.x < len(grid[neighbor.y])
                and grid[neighbor.y][neighbor.x] != '#'
                and distances[neighbor.y][neighbor.x] is None
            ):
                distances[neighbor.y][neighbor.x] = distances[current.y][current.x] + 1
                queue.put(neighbor)

    return distances


grid = [list(line.strip()) for line in sys.stdin]
distances = flood_fill(grid)

total_even = sum(
    1 for row in distances for cell in row if cell is not None and not cell % 2
)
inner_even = sum(
    1
    for row in distances
    for cell in row
    if cell is not None and not cell % 2 and cell <= len(grid) // 2
)
corners_even = total_even - inner_even

total_odd = sum(1 for row in distances for cell in row if cell is not None and cell % 2)
inner_odd = sum(
    1
    for row in distances
    for cell in row
    if cell is not None and cell % 2 and cell <= len(grid) // 2
)
corners_odd = total_odd - inner_odd

max_steps = 26501365
diamond_radius = (max_steps - len(grid) // 2) // len(grid)
full_even_grids = diamond_radius**2
full_odd_grids = (diamond_radius + 1) ** 2

print(inner_even)
print(
    (
        full_even_grids * total_even
        + diamond_radius * corners_even
        + full_odd_grids * total_odd
        - (diamond_radius + 1) * corners_odd
    )
)
