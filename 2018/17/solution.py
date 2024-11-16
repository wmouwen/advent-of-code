import re
import sys
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int

    def above(self):
        return Coord(y=self.y - 1, x=self.x)

    def below(self):
        return Coord(y=self.y + 1, x=self.x)

    def left(self):
        return Coord(y=self.y, x=self.x - 1)

    def right(self):
        return Coord(y=self.y, x=self.x + 1)


def main():
    grid = [['.' for _ in range(700)] for _ in range(2000)]

    # Input parsing
    for line in sys.stdin:
        if matches := re.match(r'x=(\d+), y=(\d+)\.\.(\d+)$', line.strip()):
            for y in range(int(matches[2]), int(matches[3]) + 1):
                grid[y][int(matches[1])] = '#'
        elif matches := re.match(r'y=(\d+), x=(\d+)\.\.(\d+)$', line.strip()):
            for x in range(int(matches[2]), int(matches[3]) + 1):
                grid[int(matches[1])][x] = '#'

    grid[0][500] = '+'
    x_min = min(x for y, row in enumerate(grid) for x, field in enumerate(row) if field == '#')
    x_max = max(x for y, row in enumerate(grid) for x, field in enumerate(row) if field == '#')
    y_min = min(y for y, row in enumerate(grid) for field in row if field == '#')
    y_max = max(y for y, row in enumerate(grid) for field in row if field == '#')

    while True:
        # Find candidate for flow
        candidates = [
            Coord(y=y, x=x)
            for y in range(0, y_max + 1)
            for x in range(x_min - 1, x_max + 2)
            if grid[y][x] in ['+', '|'] and (
                    grid[y + 1][x] == '.'
                    or (grid[y + 1][x] in ['~', '#'] and (grid[y][x - 1] == '.' or grid[y][x + 1] == '.'))
                    or (grid[y + 1][x] in ['~', '#'] and (grid[y][x - 1] == '#' and grid[y][x + 1] == '#'))
            )
        ]

        if not len(candidates):
            break

        current = candidates[0]

        # Move downwards
        while current.below().y <= y_max + 1 and grid[current.below().y][current.below().x] == '.':
            current = current.below()
            grid[current.y][current.x] = '|'

        if current.y > y_max:
            continue

        # Move sideways
        left = current.left()
        while grid[left.y][left.x] in ['.', '|']:
            grid[left.y][left.x] = '|'
            if grid[left.below().y][left.below().x] not in ['#', '~']:
                break
            left = left.left()

        right = current.right()
        while grid[right.y][right.x] in ['.', '|']:
            grid[right.y][right.x] = '|'
            if grid[right.below().y][right.below().x] not in ['#', '~']:
                break
            right = right.right()

        # Detect still water
        if grid[left.y][left.x] == '#' and grid[right.y][right.x] == '#':
            for x in range(left.x + 1, right.x):
                grid[current.y][x] = '~'

    # for y in range(y_min - 1, y_max + 2):
    #     for x in range(x_min - 1, x_max + 2):
    #         print(grid[y][x], end='')
    #     print()

    flowing = sum(1 for y in range(y_min, y_max + 1) for x in range(x_min - 1, x_max + 2) if grid[y][x] == '|')
    still = sum(1 for y in range(y_min, y_max + 1) for x in range(x_min - 1, x_max + 2) if grid[y][x] == '~')

    print(flowing + still)
    print(still)


if __name__ == '__main__':
    main()
