import sys


def find_trails(
    grid: list[list[int]], x: int, y: int, path: list[tuple[int, int]] = []
):
    if grid[y][x] == 9:
        return [path + [(x, y)]]

    return [
        trail
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= y + dy < len(grid)
        and 0 <= x + dx < len(grid[y])
        and grid[y + dy][x + dx] == grid[y][x] + 1
        for trail in find_trails(grid, x=x + dx, y=y + dy, path=path + [(x, y)])
    ]


def main():
    grid = [list(map(int, line.strip())) for line in sys.stdin if line.strip()]

    trails = [
        trail
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] == 0
        for trail in find_trails(grid, x=x, y=y)
    ]

    print(len(set((trail[0], trail[-1]) for trail in trails)))
    print(len(trails))


if __name__ == '__main__':
    main()
