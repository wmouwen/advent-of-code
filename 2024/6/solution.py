import functools
import sys
from collections import namedtuple
from math import floor

Vector = namedtuple('Vector', 'y x')


class LoopException(Exception):
    pass


def steps_to_exit(grid: list[list[str]]) -> set[Vector]:
    dirs = [Vector(y=-1, x=0), Vector(y=0, x=1), Vector(y=1, x=0), Vector(y=0, x=-1)]
    guard_start = find_guard_start(grid)
    curr_pos = guard_start
    curr_dir = 0
    visited_positions = {curr_pos}
    patrol_route = {(curr_pos, curr_dir)}

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

        if (curr_pos, curr_dir) in patrol_route:
            raise LoopException

        patrol_route.add((curr_pos, curr_dir))
        visited_positions.add(curr_pos)

    return visited_positions


def find_guard_start(grid) -> Vector:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '^':
                return Vector(y=y, x=x)

    raise Exception('No guard found')


def main():
    grid: list[list[str]] = []

    for line in sys.stdin:
        if line.strip() == '':
            break

        grid.append(list(line.strip()))

    visited_positions = steps_to_exit(grid)
    print(len(visited_positions))

    visited_positions.remove(find_guard_start(grid))
    obstacles_causing_loops = 0
    for position in visited_positions:
        grid[position.y][position.x] = '#'
        try:
            steps_to_exit(grid)
        except LoopException:
            obstacles_causing_loops += 1
        grid[position.y][position.x] = '.'

    print(obstacles_causing_loops)


if __name__ == '__main__':
    main()
