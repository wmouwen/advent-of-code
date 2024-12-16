import sys
from queue import PriorityQueue

dirs = ['N', 'E', 'S', 'W']


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = dict()


def main():
    grid = [list(line.strip()) for line in sys.stdin]

    cells = dict()
    start, end = None, None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                continue

            cells[x, y] = Cell(x, y)

            if (x - 1, y) in cells:
                cells[x - 1, y].neighbors['E'] = cells[x, y]
                cells[x, y].neighbors['W'] = cells[x - 1, y]

            if (x, y - 1) in cells:
                cells[x, y - 1].neighbors['S'] = cells[x, y]
                cells[x, y].neighbors['N'] = cells[x, y - 1]

            if cell == 'S': start = cells[x, y]
            if cell == 'E': end = cells[x, y]

    assert start is not None and end is not None

    shortest_paths = {}
    previous_path = {}
    queue = PriorityQueue()
    queue.put((0, start.x, start.y, 'E', None, None, None))
    while not queue.empty():
        distance, x, y, direction, px, py, pd = queue.get()
        cell = cells[x, y]

        if (cell, direction) in shortest_paths and distance >= shortest_paths[cell, direction]: continue
        shortest_paths[(cell, direction)] = distance
        previous_path[(cell, direction)] = (px, py, pd)

        if direction in cell.neighbors:
            neighbor = cell.neighbors[direction]
            queue.put((distance + 1, neighbor.x, neighbor.y, direction, cell.x, cell.y, direction))

        for turn in [-1, +1]:
            new_direction = dirs[(dirs.index(direction) + turn) % len(dirs)]
            queue.put((distance + 1000, cell.x, cell.y, new_direction, cell.x, cell.y, direction))

    print(min(distance for (cell, _), distance in shortest_paths.items() if cell == end))


if __name__ == '__main__':
    main()
