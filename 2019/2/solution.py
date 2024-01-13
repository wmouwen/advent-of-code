import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode')))
from intcode import IntcodeComputer, ParameterMode


def main():
    input_csv = sys.stdin.readline().strip()

    program = IntcodeComputer(program=list(map(int, input_csv.split(','))))
    program.write(addr=0x01, value=12)
    program.write(addr=0x02, value=2)
    program.run()
    print(program.read(0x00, ParameterMode.IMMEDIATE))

    for attempt in range(0, 10000):
        program = IntcodeComputer(program=list(map(int, input_csv.split(','))))
        program.write(addr=0x01, value=attempt // 100)
        program.write(addr=0x02, value=attempt % 100)

        program.run()
        if program.read(0x00, ParameterMode.IMMEDIATE) == 19690720:
            print(attempt)
            break


if __name__ == '__main__':
    main()
