import functools
import sys
from collections import namedtuple
from math import floor

Vector = namedtuple('Vector', 'y x')


def find_guard_start(grid) -> Vector:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                return Vector(y=y, x=x)

    raise Exception('No guard found')


def main():
    grid: list[list[str]] = []
    dirs = [Vector(y=-1, x=0), Vector(y=0, x=1), Vector(y=1, x=0), Vector(y=0, x=-1)]

    for line in sys.stdin:
        if line.strip() == '':
            break

        grid.append(list(line.strip()))

    guard_start = find_guard_start(grid)

    curr_pos = guard_start
    curr_dir = 0
    visited_positions = {curr_pos}
    patrol_route = {(curr_pos, curr_dir)}
    # obstacle_candidates = {}

    while True:
        next_pos = Vector(y=curr_pos.y + dirs[curr_dir].y, x=curr_pos.x + dirs[curr_dir].x)
        while 0 <= next_pos.y < len(grid) and 0 <= next_pos.x < len(grid[next_pos.y]):
            if grid[next_pos.y][next_pos.x] != '#':
                break
            curr_dir = (curr_dir + 1) % len(dirs)
            next_pos = Vector(y=curr_pos.y + dirs[curr_dir].y, x=curr_pos.x + dirs[curr_dir].x)

        if not (0 <= next_pos.y < len(grid) and 0 <= next_pos.x < len(grid[next_pos.y])):
            break

        curr_pos = next_pos
        visited_positions.add(curr_pos)
        patrol_route.add((curr_pos, curr_dir))

        # if (curr_pos, (curr_dir + 1) % 4) in patrol_route:
        #     print('obstacle?')

    print(len(visited_positions))


if __name__ == '__main__':
    main()
