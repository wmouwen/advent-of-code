import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer


def run(program: list[int], instructions: list[str]) -> list[str]:
    instructions = list(map(ord, '\n'.join(instructions) + '\n'))
    output = []

    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: instructions.pop(0),
        output_callback=lambda value: output.append(value),
    )
    computer.run()

    return ''.join(map(lambda x: chr(x) if x < 255 else str(x), output)).split('\n')


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    output = run(
        program,
        [
            # Jump early if B or C is a hole and D is ground
            'NOT B T',
            'OR T J',
            'NOT C T',
            'OR T J',
            'AND D J',

            # Always jump if A is a hole
            'NOT A T',
            'OR T J',

            # Walking mode
            'WALK',
        ],
    )
    print(output[-1])

    output = run(
        program,
        [
            # Jump early if B or C is a hole and D is ground
            'NOT B T',
            'OR T J',
            'NOT C T',
            'OR T J',
            'AND D J',

            # Make sure a double jump is possible if needed
            'AND H J',

            # Always jump if A is a hole
            'NOT A T',
            'OR T J',

            # Running mode
            'RUN',
        ],
    )
    print(output[-1])


if __name__ == '__main__':
    main()
