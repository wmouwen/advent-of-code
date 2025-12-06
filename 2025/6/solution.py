import math
import re
import sys


def solve_normal(lines: list[str]) -> int:
    numbers, operations, total = [], [], 0

    for line in lines:
        if matches := re.findall(r'\d+', line):
            numbers.append(list(map(int, matches)))
        if matches := re.findall(r'[+*]', line):
            operations = matches

    for x, op in enumerate(operations):
        if op == '+':
            total += sum(numbers[y][x] for y in range(len(numbers)))
        if op == '*':
            total += math.prod(numbers[y][x] for y in range(len(numbers)))

    return total


def solve_rtl(lines: list[str]) -> int:
    numbers, total = [], 0

    for x in range(max(len(lines[y]) for y in range(len(lines))) - 1, -1, -1):
        number = ''.join(
            lines[y][x] if x < len(lines[y]) else ' ' for y in range(len(lines) - 1)
        ).strip()

        if number == '':
            continue

        numbers.append(int(number))

        op = lines[-1][x] if x < len(lines[-1]) else ' '
        if op == '+':
            total += sum(numbers)
            numbers.clear()
        if op == '*':
            total += math.prod(numbers)
            numbers.clear()

    return total


def main():
    lines = [line.rstrip() for line in sys.stdin]

    print(solve_normal(lines))
    print(solve_rtl(lines))


if __name__ == '__main__':
    main()
