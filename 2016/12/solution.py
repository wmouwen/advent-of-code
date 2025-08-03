import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../assembunny'))
)
from assembunny import AssembunnyComputer


def main():
    instructions = [line.strip().split(' ') for line in sys.stdin]
    computer = AssembunnyComputer(instructions)
    computer.run()
    print(computer.read('a'))

    computer = AssembunnyComputer(instructions)
    computer.write('c', 1)
    computer.run()
    print(computer.read('a'))


if __name__ == '__main__':
    main()
