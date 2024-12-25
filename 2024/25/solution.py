import sys


def parse_grid(grid):
    return tuple(sum(int(grid[y][x] == '#') for y in range(len(grid))) for x in range(len(grid[0])))


def matching_pairs(locks, keys, height):
    return sum(int(all(lock[i] + key[i] <= height for i in range(len(lock)))) for lock in locks for key in keys)


def main():
    locks, keys = [], []
    height = None

    grid = []
    for line in sys.stdin:
        if line.strip() == '':
            (keys if '.' in grid[0] else locks).append(parse_grid(grid))
            height = len(grid)
            grid = []
        else:
            grid.append(line.strip())

    (keys if '.' in grid[0] else locks).append(parse_grid(grid))

    print(matching_pairs(locks, keys, height))


if __name__ == '__main__':
    main()
