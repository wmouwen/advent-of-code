import sys
from typing import NamedTuple

V = NamedTuple('Vector', [('x', int), ('y', int)])
dirs = {'^': V(0, -1), '>': V(1, 0), 'v': V(0, 1), '<': V(-1, 0)}


def main():
    grid = []
    for line in sys.stdin:
        if line.strip() == '': break
        grid.append(list(line.strip()))

    instructions = list(instruction for line in sys.stdin for instruction in line.strip())

    robot = next(V(x, y) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == '@')
    grid[robot.y][robot.x] = '.'

    for instruction in instructions:
        d = dirs[instruction]
        n = V(robot.x + d.x, robot.y + d.y)

        while grid[n.y][n.x] == 'O':
            n = V(n.x + d.x, n.y + d.y)

        if grid[n.y][n.x] == '#':
            continue

        robot = V(robot.x + d.x, robot.y + d.y)

        if grid[robot.y][robot.x] == 'O':
            grid[n.y][n.x] = 'O'
            grid[robot.y][robot.x] = '.'

    # print(*(''.join(row) for row in grid), sep='\n')
    print(sum(100 * y + x for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == 'O'))


if __name__ == '__main__':
    main()
