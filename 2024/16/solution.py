import sys
from queue import PriorityQueue

dirs = ['N', 'E', 'S', 'W']


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = dict()


def find_shortest_paths(cells, start, end):
    distances = {}
    shortest_paths = {}

    queue = PriorityQueue()
    queue.put((0, start.x, start.y, 'E', []))

    while not queue.empty():
        distance, x, y, direction, path = queue.get()
        cell = cells[x, y]

        if (cell, direction) in distances and distance > distances[cell, direction]:
            continue

        if (cell, direction) in distances and distance == distances[cell, direction]:
            shortest_paths[(cell, direction)].append(path)

        if (cell, direction) not in distances or distance < distances[cell, direction]:
            shortest_paths[(cell, direction)] = [path]
            distances[(cell, direction)] = distance

        if direction in cell.neighbors:
            neighbor = cell.neighbors[direction]
            queue.put(
                (
                    distance + 1,
                    neighbor.x,
                    neighbor.y,
                    direction,
                    path + [(x, y, direction)],
                )
            )

        for turn in [-1, +1]:
            new_direction = dirs[(dirs.index(direction) + turn) % len(dirs)]
            queue.put(
                (
                    distance + 1000,
                    cell.x,
                    cell.y,
                    new_direction,
                    path + [(x, y, direction)],
                )
            )

    return shortest_paths, distances


def main():
    grid = [list(line.strip()) for line in sys.stdin]

    cells = dict()
    start, end = None, None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '#':
                continue

            cells[x, y] = Cell(x, y)
            if cell == 'S':
                start = cells[x, y]
            if cell == 'E':
                end = cells[x, y]

            if (x - 1, y) in cells:
                cells[x - 1, y].neighbors['E'] = cells[x, y]
                cells[x, y].neighbors['W'] = cells[x - 1, y]

            if (x, y - 1) in cells:
                cells[x, y - 1].neighbors['S'] = cells[x, y]
                cells[x, y].neighbors['N'] = cells[x, y - 1]

    assert start is not None and end is not None

    shortest_paths, distances = find_shortest_paths(cells, start, end)

    min_distance = min(
        distance for (cell, _), distance in distances.items() if cell == end
    )
    print(min_distance)

    fields_on_optimal_path = {(start.x, start.y), (end.x, end.y)}
    for direction in dirs:
        if (end, direction) not in shortest_paths or distances[
            (end, direction)
        ] > min_distance:
            continue

        for path in shortest_paths[(end, direction)]:
            fields_on_optimal_path = fields_on_optimal_path.union(
                set((x, y) for (x, y, _) in path)
            )

    print(len(fields_on_optimal_path))


if __name__ == '__main__':
    main()
