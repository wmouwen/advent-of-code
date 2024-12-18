import sys
from queue import Queue

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def floodfill(grid):
    distances: list[list[int | None]] = [[None for _ in range(len(grid))] for _ in range(len(grid))]
    distances[0][0] = 0

    queue = Queue()
    queue.put((0, 0, 0))
    while not queue.empty():
        distance, x, y = queue.get()

        for dx, dy in dirs:
            if not (0 <= x + dx < len(grid) and 0 <= y + dy < len(grid)):
                continue

            if distances[y + dy][x + dx] is not None or grid[y + dy][x + dx] == '#':
                continue

            distances[y + dy][x + dx] = distance + 1
            queue.put((distance + 1, x + dx, y + dy))

    return distances


def main():
    grid_size = 71
    lap_count = 1024

    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

    for i in range(lap_count):
        line = sys.stdin.readline()
        if line.strip() == '':
            break

        x, y = map(int, line.split(','))
        grid[y][x] = '#'

    distances = floodfill(grid)
    print(distances[grid_size - 1][grid_size - 1])

    for line in sys.stdin:
        x, y = map(int, line.split(','))
        grid[y][x] = '#'
        distances = floodfill(grid)
        if distances[-1][-1] is None:
            print(f'{x},{y}')
            break


if __name__ == '__main__':
    main()
