import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer

dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def build_grid(program):
    output = []
    computer = IntcodeComputer(
        program=program, output_callback=lambda value: output.append(value)
    )
    computer.run()

    return list(filter(lambda line: line != '', ''.join(map(chr, output)).split('\n')))


def alignment_parameters(grid):
    return [
        x * y
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if all(
            0 <= y + dy < len(grid)
            and 0 <= x + dx < len(grid[y + dy])
            and grid[y + dy][x + dx] == '#'
            for dx, dy in dirs
        )
    ]


def extract_path(grid):
    path = []

    x, y = [
        (x, y)
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] == '^'
    ][0]
    d = 0

    while True:
        dx, dy = dirs[d]

        if (
            not (0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y + dy]))
            or grid[y + dy][x + dx] != '#'
        ):
            lx, ly = dirs[ld := ((d - 1) % len(dirs))]
            rx, ry = dirs[rd := ((d + 1) % len(dirs))]
            if (
                0 <= y + ly < len(grid)
                and 0 <= x + lx < len(grid[y + ly])
                and grid[y + ly][x + lx] == '#'
            ):
                dx, dy, d = lx, ly, ld
                path.extend(['L', 0])
            elif (
                0 <= y + ry < len(grid)
                and 0 <= x + rx < len(grid[y + ry])
                and grid[y + ry][x + rx] == '#'
            ):
                dx, dy, d = rx, ry, rd
                path.extend(['R', 0])
            else:
                break

        x, y = x + dx, y + dy
        path[-1] += 1

    if path[0] == 0:
        path.pop(0)

    return path


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    grid = build_grid(program)
    print(sum(alignment_parameters(grid)))

    path = extract_path(grid)
    path = ','.join(map(str, path))

    # print(path)
    functions = {
        # Find and fill these manually based on the path
        'A': 'L,4,L,6,L,8,L,12',
        'B': 'L,8,R,12,L,12',
        'C': 'R,12,L,6,L,6,L,8',
    }

    for function, movements in functions.items():
        path = path.replace(movements, function)
    # print(path)

    instructions = [path, functions['A'], functions['B'], functions['C'], 'n']

    instructions = list(map(ord, '\n'.join(instructions) + '\n'))
    output = []
    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: instructions.pop(0),
        output_callback=lambda value: output.append(value),
    )
    computer.write(0x00, 2)
    computer.run()

    print(output[-1])


if __name__ == '__main__':
    main()
