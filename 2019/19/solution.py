import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode')))
from intcode import IntcodeComputer


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    beam_size = 0

    for y in range(50):
        for x in range(50):
            coordinates = [x, y]
            output = []

            computer = IntcodeComputer(
                program=program,
                input_callback=lambda: coordinates.pop(0),
                output_callback=lambda value: output.append(value)
            )
            computer.run()
            beam_size += int(output[0] == 1)

    print(beam_size)


if __name__ == '__main__':
    main()
