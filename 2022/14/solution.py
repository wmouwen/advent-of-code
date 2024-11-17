import sys
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int


def main():
    grid = [['.' for _ in range(1000)] for _ in range(2000)]

    for line in sys.stdin:
        coords = list(map(
            lambda item: Coord(y=int(item.split(',')[1]), x=int(item.split(',')[0])),
            line.strip().split(' -> ')
        ))
        for i in range(1, len(coords)):
            for x in range(min(coords[i - 1].x, coords[i].x), max(coords[i - 1].x, coords[i].x) + 1):
                for y in range(min(coords[i - 1].y, coords[i].y), max(coords[i - 1].y, coords[i].y) + 1):
                    grid[y][x] = '#'

    x_min = min(x for y, row in enumerate(grid) for x, field in enumerate(row) if field == '#')
    x_max = max(x for y, row in enumerate(grid) for x, field in enumerate(row) if field == '#')
    y_max = max(y for y, row in enumerate(grid) for field in row if field == '#')

    for x in range(0, len(grid[y_max + 2])):
        grid[y_max + 2][x] = '#'

    source = Coord(y=0, x=500)
    grid[source.y][source.x] = '+'
    stack = [source]
    current = source
    handled_part_one = False
    while len(stack):
        if grid[current.y + 1][current.x] == '.':
            stack.append(current)
            current = Coord(y=current.y + 1, x=current.x)
            grid[current.y][current.x] = '~'
        elif grid[current.y + 1][current.x - 1] == '.':
            stack.append(current)
            current = Coord(y=current.y + 1, x=current.x - 1)
            grid[current.y][current.x] = '~'
        elif grid[current.y + 1][current.x + 1] == '.':
            stack.append(current)
            current = Coord(y=current.y + 1, x=current.x + 1)
            grid[current.y][current.x] = '~'
        else:
            grid[current.y][current.x] = 'o'
            current = stack.pop()

        if current.y == y_max and not handled_part_one:
            print(sum(1 for y in range(0, y_max + 1) for x in range(x_min - 1, x_max + 2) if grid[y][x] == 'o'))
            handled_part_one = True

    print(sum(1 for y in range(0, y_max + 2) for x in range(len(grid[y])) if grid[y][x] == 'o'))

    # for y in range(0, y_max + 4):
    #     for x in range(x_min - 1, x_max + 2):
    #         print(grid[y][x], end='')
    #     print()


if __name__ == '__main__':
    main()
