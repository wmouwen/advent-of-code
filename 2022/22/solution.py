import re
import sys

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def main():
    grid = []
    for line in sys.stdin:
        if line.strip() == "":
            break
        grid.append(list(line.rstrip()))

    width = max(len(row) for row in grid)
    for row in grid:
        row.extend([' '] * (width - len(row)))

    x, y, d = min(x for x, cell in enumerate(grid[0]) if cell == '.'), 0, 0
    instructions = re.findall(r"(\d+|R|L)", sys.stdin.readline().strip())

    for instruction in instructions:
        if instruction == 'R':
            d = (d + 1) % len(dirs)
        elif instruction == 'L':
            d = (d - 1) % len(dirs)
        else:
            steps = int(instruction)
            while steps > 0:
                dx, dy = dirs[d % len(dirs)]

                ny = (y + dy) % len(grid)
                nx = (x + dx) % len(grid[ny])
                while grid[ny][nx] == ' ':
                    ny = (ny + dy) % len(grid)
                    nx = (nx + dx) % len(grid[ny])

                if grid[ny][nx] == '#':
                    break
                else:
                    x, y = nx, ny
                    steps -= 1

    print(1000 * (y + 1) + 4 * (x + 1) + d)


if __name__ == '__main__':
    main()
