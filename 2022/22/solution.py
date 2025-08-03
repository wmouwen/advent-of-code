import re
import sys
from typing import NamedTuple, Self


class V(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return V(x=self.x + other.x, y=self.y + other.y)


Link = NamedTuple('Link', [('facing', int), ('offset', int), ('reverse', bool)])
State = tuple[V, int]

DIRECTIONS = (V(x=1, y=0), V(x=0, y=1), V(x=-1, y=0), V(x=0, y=-1))


def password(pos, facing):
    return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + (facing % len(DIRECTIONS))


def oob_flat(grid, pos, facing) -> State:
    pos += DIRECTIONS[facing]
    return V(x=pos.x % len(grid[pos.y % len(grid)]), y=pos.y % len(grid)), facing


def warp(x_max: int, y_max: int, size: int, index: int, link: Link) -> State:
    facing, offset, reverse = link
    index = (offset * size) + (
        (index % size) if not reverse else (size - (index % size) - 1)
    )

    if facing == 0:
        return V(x=0, y=index), facing
    if facing == 1:
        return V(x=index, y=0), facing
    if facing == 2:
        return V(x=x_max, y=index), facing
    if facing == 3:
        return V(x=index, y=y_max), facing
    raise Exception


def oob_cube(grid, pos, facing, links) -> State:
    pos += DIRECTIONS[facing]
    size, x_max, y_max = len(grid) // len(links[0]), len(grid[0]) - 1, len(grid) - 1

    if pos.x > x_max:
        return warp(x_max, y_max, size, pos.y, links[facing][pos.y // size])
    if pos.y > y_max:
        return warp(x_max, y_max, size, pos.x, links[facing][pos.x // size])
    if pos.x < 0:
        return warp(x_max, y_max, size, pos.y, links[facing][pos.y // size])
    if pos.y < 0:
        return warp(x_max, y_max, size, pos.x, links[facing][pos.x // size])

    return pos, facing


def oob_cube_test(grid, pos, facing) -> State:
    """
    Cube layout:
      __#_
      ###_
      __##
    """
    return oob_cube(
        grid,
        pos,
        facing,
        {
            0: [Link(2, 2, True), Link(1, 3, True), Link(2, 0, True)],
            1: [
                Link(3, 2, True),
                Link(0, 2, False),
                Link(3, 0, True),
                Link(2, 1, True),
            ],
            2: [Link(1, 1, True), Link(3, 3, True), Link(3, 1, True)],
            3: [
                Link(1, 2, True),
                Link(0, 0, False),
                Link(1, 0, True),
                Link(2, 1, True),
            ],
        },
    )


def oob_cube_puzzle(grid, pos, facing) -> State:
    """
    Cube layout:
      _##
      _#_
      ##_
      #__
    """
    return oob_cube(
        grid,
        pos,
        facing,
        {
            0: [
                Link(2, 2, True),
                Link(3, 2, False),
                Link(2, 0, True),
                Link(3, 1, False),
            ],
            1: [Link(1, 2, False), Link(2, 3, False), Link(2, 1, False)],
            2: [
                Link(0, 2, True),
                Link(1, 0, False),
                Link(0, 0, True),
                Link(1, 1, False),
            ],
            3: [Link(0, 1, False), Link(0, 3, False), Link(3, 0, False)],
        },
    )


def walk(grid, instructions, move_callback):
    pos, facing = V(x=min(x for x, cell in enumerate(grid[0]) if cell == '.'), y=0), 0

    for instruction in re.findall(r'(\d+|R|L)', instructions):
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
        if line.strip() == '':
            break
        grid.append(list(line.rstrip()))

    width = max(len(row) for row in grid)
    for row in grid:
        row.extend([' '] * (width - len(row)))

    instructions = sys.stdin.readline().strip()

    print(password(*walk(grid, instructions, oob_flat)))
    print(
        password(
            *walk(
                grid, instructions, oob_cube_puzzle if len(grid) > 12 else oob_cube_test
            )
        )
    )


if __name__ == '__main__':
    main()
