import math
import re
import sys
from queue import PriorityQueue

GRID_SIZE = 1500


def main():
    depth = int(re.match(r'depth: (\d+)', sys.stdin.readline()).group(1))
    target = re.match(r'target: (\d+),(\d+)', sys.stdin.readline())
    target_x = int(target.group(1))
    target_y = int(target.group(2))

    geologic_indexes = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    erosion_levels = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    region_type = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    lcm = math.lcm(16807, 48271, 20183, 3)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x == 0 and y == 0) or (x == target_x and y == target_y):
                geologic_indexes[y][x] = 0
            elif y == 0:
                geologic_indexes[y][x] = x * 16807
            elif x == 0:
                geologic_indexes[y][x] = y * 48271
            else:
                geologic_indexes[y][x] = (
                    erosion_levels[y - 1][x] * erosion_levels[y][x - 1]
                ) % lcm

            erosion_levels[y][x] = (geologic_indexes[y][x] + depth) % 20183
            region_type[y][x] = erosion_levels[y][x] % 3

    print(sum(sum(row[0 : target_x + 1]) for row in region_type[0 : target_y + 1]))

    distances = [
        [[sys.maxsize, sys.maxsize, sys.maxsize] for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]
    distances[0][0] = [0, 0, 0]
    target_distance = sys.maxsize

    queue = PriorityQueue()
    queue.put((0, 0, 0, 1))

    while not queue.empty():
        distance, y, x, forbidden_type = queue.get()

        if distance >= target_distance:
            continue

        if x == target_x and y == target_y:
            target_distance = min(
                distance + (7 if forbidden_type != 1 else 0), target_distance
            )
            continue

        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                continue

            new_forbidden_type = forbidden_type
            if forbidden_type == region_type[ny][nx]:
                new_forbidden_type = (3 - region_type[y][x] - region_type[ny][nx]) % 3

            new_distance = distance + (1 if forbidden_type == new_forbidden_type else 8)

            if new_distance >= distances[ny][nx][new_forbidden_type]:
                continue

            distances[ny][nx][new_forbidden_type] = min(
                distances[ny][nx][new_forbidden_type], new_distance
            )
            queue.put((new_distance, ny, nx, new_forbidden_type))

    print(target_distance)


if __name__ == '__main__':
    main()
