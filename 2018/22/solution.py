import re
import sys

GRID_SIZE = 1500


def main():
    depth = int(re.match(r'depth: (\d+)', sys.stdin.readline()).group(1))
    target = re.match(r'target: (\d+),(\d+)', sys.stdin.readline())
    tx = int(target.group(1))
    ty = int(target.group(2))

    geologic_indexes = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    erosion_levels = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    region_type = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if x == 0 and y == 0:
                geologic_indexes[y][x] = 0
            elif x == tx and y == ty:
                geologic_indexes[y][x] = 0
            elif y == 0:
                geologic_indexes[y][x] = x * 16807
            elif x == 0:
                geologic_indexes[y][x] = y * 48271
            else:
                geologic_indexes[y][x] = erosion_levels[y - 1][x] * erosion_levels[y][x - 1]

            erosion_levels[y][x] = (geologic_indexes[y][x] + depth) % 20183
            region_type[y][x] = erosion_levels[y][x] % 3

    print(sum(sum(row[0:tx + 1]) for row in region_type[0:ty + 1]))


if __name__ == '__main__':
    main()
