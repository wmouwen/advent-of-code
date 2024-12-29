import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode')))
from intcode import IntcodeComputer

dirs = {(1, 0), (0, 1), (-1, 0), (0, -1)}


def main():
    output = []
    computer = IntcodeComputer(
        program=list(map(int, sys.stdin.readline().strip().split(','))),
        output_callback=lambda value: output.append(value)
    )
    computer.run()

    grid = list(filter(lambda line: line != '', ''.join(map(chr, output)).split('\n')))
    print(sum(
        x * y
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if all(
            0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y + dy]) and grid[y + dy][x + dx] == '#'
            for dx, dy in dirs
        )
    ))


if __name__ == '__main__':
    main()
