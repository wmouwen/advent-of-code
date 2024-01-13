import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode')))
from intcode import IntcodeComputer, ParameterMode


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    computer = IntcodeComputer(program=program)
    computer.write(addr=0x01, value=12)
    computer.write(addr=0x02, value=2)
    computer.run()
    print(computer.read(0x00, ParameterMode.IMMEDIATE))

    for attempt in range(0, 10000):
        computer = IntcodeComputer(program=program)
        computer.write(addr=0x01, value=attempt // 100)
        computer.write(addr=0x02, value=attempt % 100)

        computer.run()
        if computer.read(0x00, ParameterMode.IMMEDIATE) == 19690720:
            print(attempt)
            break


if __name__ == '__main__':
    main()
