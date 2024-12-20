import sys
from queue import Queue
from typing import NamedTuple

V = NamedTuple('V', [('x', int), ('y', int)])
dirs = [V(0, -1), V(1, 0), V(0, 1), V(-1, 0)]


def floodfill(grid: list[list[str]], origin: V):
    distances: list[list[int | None]] = [[None for _ in range(len(grid[y]))] for y, _ in enumerate(grid)]
    distances[origin.y][origin.x] = 0

    queue = Queue()
    queue.put((0, origin.x, origin.y))
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


def cheat_count(distances: list[list[int | None]], start: V, max_length: int, min_profit: int) -> int:
    count = 0

    queue = Queue()
    queue.put(start)
    while not queue.empty():
        c = queue.get()

        for dy in range(-1 * max_length, max_length + 1):
            for dx in range(-1 * max_length + abs(dy), max_length + 1 - abs(dy)):
                n = V(x=c.x + dx, y=c.y + dy)
                if 0 <= n.y < len(distances) and 0 <= n.x < len(distances[n.y]) and distances[n.y][n.x] is not None:
                    if distances[c.y][c.x] - distances[n.y][n.x] - abs(dy) - abs(dx) >= min_profit:
                        count += 1

        if distances[c.y][c.x] <= min_profit:
            break

        for d in dirs:
            n = V(x=c.x + d.x, y=c.y + d.y)

            if distances[n.y][n.x] == distances[c.y][c.x] - 1:
                queue.put(n)

    return count


def main():
    grid = [list(line.strip()) for line in sys.stdin]
    start, end = None, None

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S': start = V(x, y)
            if cell == 'E': end = V(x, y)

    assert isinstance(start, V) and isinstance(end, V)
    distances = floodfill(grid, end)

    print(cheat_count(distances, start, max_length=2, min_profit=100))
    print(cheat_count(distances, start, max_length=20, min_profit=100))


if __name__ == '__main__':
    main()
