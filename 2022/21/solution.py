import re
import sys
from typing import Self


class Monkey:
    def __init__(self, left: str, operator: str, right: str):
        self.left: str = left
        self.operator: str = operator
        self.right: str = right

    def value(self, monkeys: dict[str, Self | int]) -> int:
        left = (
            monkeys[self.left]
            if isinstance(monkeys[self.left], int)
            else monkeys[self.left].value(monkeys)
        )
        right = (
            monkeys[self.right]
            if isinstance(monkeys[self.right], int)
            else monkeys[self.right].value(monkeys)
        )

        match self.operator:
            case '+':
                return left + right
            case '-':
                return left - right
            case '*':
                return left * right
            case '/':
                return left // right
            case '=':
                return int(left == right)
            case _:
                raise Exception('Invalid operator')


def main():
    monkeys: dict[str, Monkey | int] = {}

    for line in sys.stdin:
        if match := re.match(r'(\w+): (\w+) (.) (\w+)', line):
            monkeys[match.group(1)] = Monkey(
                left=match.group(2), operator=match.group(3), right=match.group(4)
            )
        elif match := re.match(r'(\w+): (\d+)', line):
            monkeys[match.group(1)] = int(match.group(2))

    print(monkeys['root'].value(monkeys))

    # TODO Optimize and/or cache
    monkeys['root'].operator = '='
    for yell in range(0, sys.maxsize):
        monkeys['humn'] = yell

        if monkeys['root'].value(monkeys) == 1:
            print(yell)
            return


if __name__ == '__main__':
    main()
