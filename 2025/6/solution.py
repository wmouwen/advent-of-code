import math
import re
import sys


def solve_normal(lines: list[str]) -> int:
    numbers, operations = [], []

    for line in lines:
        if matches := re.findall(r'\d+', line):
            numbers.append(list(map(int, matches)))
        if matches := re.findall(r'[+*]', line):
            operations = matches

    total = 0
    for x, op in enumerate(operations):
        match op:
            case '+':
                total += sum(numbers[y][x] for y in range(len(numbers)))
            case '*':
                total += math.prod(numbers[y][x] for y in range(len(numbers)))

    return total


def solve_rtl(lines: list[str]) -> int:
    return 0


def main():
    lines = [line.strip() for line in sys.stdin]

    print(solve_normal(lines))
    print(solve_rtl(lines))


if __name__ == '__main__':
    main()
