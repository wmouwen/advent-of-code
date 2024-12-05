import re
import sys


def word_hit(grid: list[list[str]], y: int, x: int, dy: int, dx: int, target: str) -> bool:
    if 0 <= y < len(grid) and 0 <= x < len(grid[y]) and grid[y][x] == target[0]:
        return len(target) == 1 or word_hit(grid, y + dy, x + dx, dy, dx, target[1:])
    else:
        return False


def main():
    grid = [list(line.strip()) for line in sys.stdin if line.strip() != '']
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    print(sum(
        1
        for y in range(len(grid))
        for x in range(len(grid[y]))
        for (dy, dx) in dirs
        if word_hit(grid, y, x, dy, dx, 'XMAS')
    ))

    cross_count = 0
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x] != 'A':
                continue
            corners = [grid[y - 1][x - 1], grid[y - 1][x + 1], grid[y + 1][x + 1], grid[y + 1][x - 1]]
            if corners.count('M') == 2 and corners.count('S') == 2 and corners[0] != corners[2]:
                cross_count += 1

    print(cross_count)


if __name__ == '__main__':
    main()
