import copy
import sys


def evolve(grid_old):
    grid_new = copy.deepcopy(grid_old)

    for y, row in enumerate(grid_old):
        for x, field in enumerate(row):
            neighbors = [
                grid_old[ny][nx]
                for ny in range(max(0, y - 1), min(len(grid_old), y + 2))
                for nx in range(max(0, x - 1), min(len(grid_old[ny]), x + 2))
                if nx != x or ny != y
            ]

            if (
                grid_old[y][x] == '.'
                and sum(1 for neighbor in neighbors if neighbor == '|') >= 3
            ):
                grid_new[y][x] = '|'
            elif (
                grid_old[y][x] == '|'
                and sum(1 for neighbor in neighbors if neighbor == '#') >= 3
            ):
                grid_new[y][x] = '#'
            elif grid_old[y][x] == '#' and not ('|' in neighbors and '#' in neighbors):
                grid_new[y][x] = '.'
            else:
                grid_new[y][x] = grid_old[y][x]

    return grid_new


def resource_value(grid):
    return sum(1 for row in grid for field in row if field == '#') * sum(
        1 for row in grid for field in row if field == '|'
    )


def main():
    grid = [[field for field in line.strip()] for line in sys.stdin.readlines()]

    visited = dict()
    tick = 0
    while tick < 1000000000:
        tick += 1
        grid = evolve(grid)

        if tick == 10:
            print(resource_value(grid))

        hash = ''.join([''.join(row) for row in grid])
        if hash in visited:
            tick += (tick - visited[hash]) * (
                (1000000000 - tick) // (tick - visited[hash])
            )

        visited[hash] = tick

    print(resource_value(grid))


if __name__ == '__main__':
    main()
