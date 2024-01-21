import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../assembunny')))
from assembunny import AssembunnyComputer


class Attempt:
    def __init__(self, init: int):
        self.init: int = init
        self.output_cycle: int = 0
        self.valid: bool = True


def output_validate(computer: AssembunnyComputer, attempt: Attempt, value: int) -> None:
    if attempt.output_cycle % 2 != value:
        attempt.valid = False
        computer.interrupt()

    attempt.output_cycle += 1

    if attempt.output_cycle == 8 ** 2:
        computer.interrupt()


def main():
    instructions = [line.strip().split(' ') for line in sys.stdin]

    attempt = Attempt(init=0)
    while attempt.init < 10000:
        computer = AssembunnyComputer(
            instructions=instructions,
            output_callback=lambda value: output_validate(computer, attempt, value)
        )
        computer.write('a', attempt.init)
        computer.run()

        if attempt.valid:
            print(attempt.init)
            return

        attempt = Attempt(init=attempt.init + 1)

    print(None)


if __name__ == '__main__':
    main()
