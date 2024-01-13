import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode')))
from intcode import IntcodeComputer


def main():
    input_csv = sys.stdin.readline().strip()

    output = []
    program = IntcodeComputer(
        program=list(map(int, input_csv.split(','))),
        input_callback=lambda: 1,
        output_callback=lambda value: output.append(value)
    )
    program.run()
    print(output[-1])

    output = []
    program = IntcodeComputer(
        program=list(map(int, input_csv.split(','))),
        input_callback=lambda: 5,
        output_callback=lambda value: output.append(value)
    )
    program.run()
    print(output[-1])


if __name__ == '__main__':
    main()
