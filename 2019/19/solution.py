import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer


def is_within_beam(program, x, y):
    coordinates = [x, y]
    output = []

    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: coordinates.pop(0),
        output_callback=lambda value: output.append(value),
    )
    computer.run()

    return output[0] == 1


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    print(
        sum(
            1 for ay in range(50) for ax in range(50) if is_within_beam(program, ax, ay)
        )
    )

    x, y = 0, 99

    while True:
        if not is_within_beam(program, x, y):
            x += 1
            continue

        if y - 99 >= 0 and is_within_beam(program, x + 99, y - 99):
            break

        y += 1

    print(x * 10000 + (y - 99))


if __name__ == '__main__':
    main()
