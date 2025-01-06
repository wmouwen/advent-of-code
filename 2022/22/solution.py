import re
import sys
from typing import NamedTuple, Self


class V(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return V(x=self.x + other.x, y=self.y + other.y)


DIRECTIONS = (V(x=1, y=0), V(x=0, y=1), V(x=-1, y=0), V(x=0, y=-1))


def password(pos, facing):
    return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + (facing % len(DIRECTIONS))


def oob_flat(grid, pos, facing) -> (V, int):
    pos += DIRECTIONS[facing]
    return V(x=pos.x % len(grid[pos.y % len(grid)]), y=pos.y % len(grid)), facing


def oob_cube_test(grid, pos, facing) -> (V, int):
    """
    Cube layout:
      __#_
      ###_
      __##
    """

    pos += DIRECTIONS[facing]

    size = len(grid) // 3
    x_max, y_max = 4 * size - 1, 3 * size - 1
    fwd = lambda o, c: o * size + (c % size)
    rev = lambda o, c: o * size + size - (c % size) - 1

    if pos.y < 0:
        if 0 * size <= pos.x < 1 * size: return V(x=rev(o=2, c=pos.x), y=0), 1
        if 1 * size <= pos.x < 2 * size: return V(x=0, y=fwd(o=0, c=pos.x)), 0
        if 2 * size <= pos.x < 3 * size: return V(x=rev(o=0, c=pos.x), y=0), 1
        if 3 * size <= pos.x < 4 * size: return V(x=x_max, y=rev(o=1, c=pos.x)), 2
        raise Exception

    if pos.y >= 3 * size:
        if 0 * size <= pos.x < 1 * size: return V(x=rev(o=2, c=pos.x), y=y_max), 3
        if 1 * size <= pos.x < 2 * size: return V(x=0, y=fwd(o=2, c=pos.x)), 0
        if 2 * size <= pos.x < 3 * size: return V(x=rev(o=0, c=pos.x), y=y_max), 3
        if 3 * size <= pos.x < 4 * size: return V(x=x_max, y=rev(o=1, c=pos.x)), 2
        raise Exception

    if pos.x < 0:
        if 0 * size <= pos.y < 1 * size: return V(x=rev(o=1, c=pos.y), y=0), 1
        if 1 * size <= pos.y < 2 * size: return V(x=rev(o=3, c=pos.y), y=y_max), 3
        if 2 * size <= pos.y < 3 * size: return V(x=rev(o=1, c=pos.y), y=y_max), 3
        raise Exception

    if pos.x >= 4 * size:
        if 0 * size <= pos.y < 1 * size: return V(x=x_max, y=rev(o=2, c=pos.y)), 2
        if 1 * size <= pos.y < 2 * size: return V(x=rev(o=3, c=pos.y), y=0), 1
        if 2 * size <= pos.y < 3 * size: return V(x=x_max, y=rev(o=0, c=pos.y)), 2
        raise Exception

    return pos, facing


def oob_cube_puzzle(grid, pos, facing) -> (V, int):
    """
    Cube layout:
      _##
      _#_
      ##_
      #__
    """

    pos += DIRECTIONS[facing]

    raise Exception('Not implemented')


def walk(grid, instructions, move_callback):
    pos, facing = V(x=min(x for x, cell in enumerate(grid[0]) if cell == '.'), y=0), 0

    for instruction in re.findall(r"(\d+|R|L)", instructions):
        if instruction == 'R':
            facing = (facing + 1) % len(DIRECTIONS)
            continue

        if instruction == 'L':
            facing = (facing - 1) % len(DIRECTIONS)
            continue

        for _ in range(int(instruction)):
            next_pos, next_facing = move_callback(grid, pos, facing)
            while grid[next_pos.y][next_pos.x] == ' ':
                next_pos, next_facing = move_callback(grid, next_pos, next_facing)

            if grid[next_pos.y][next_pos.x] != '#':
                pos, facing = next_pos, next_facing

    return pos, facing


def main():
    grid = []
    for line in sys.stdin:
        if line.strip() == "": break
        grid.append(list(line.rstrip()))

    width = max(len(row) for row in grid)
    for row in grid:
        row.extend([' '] * (width - len(row)))

    instructions = sys.stdin.readline().strip()

    print(password(*walk(grid, instructions, oob_flat)))
    print(password(*walk(grid, instructions, oob_cube_puzzle if len(grid) > 12 else oob_cube_test)))


if __name__ == '__main__':
    main()
