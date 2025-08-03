import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    output = []
    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: 1,
        output_callback=lambda value: output.append(value),
    )
    computer.run()
    print(output[0])

    output = []
    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: 2,
        output_callback=lambda value: output.append(value),
    )
    computer.run()
    print(output[0])


if __name__ == '__main__':
    main()
