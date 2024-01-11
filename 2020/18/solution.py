import re
import sys


def evaluate_no_precedence(expression: str) -> int:
    parts = expression.split(' ')
    answer = int(parts[0])

    for i in range(2, len(parts), 2):
        if parts[i - 1] == '+':
            answer += int(parts[i])
        elif parts[i - 1] == '*':
            answer *= int(parts[i])

    return answer


def evaluate_addition_first(expression: str) -> int:
    while match := re.search(r'(\d+) \+ (\d+)', expression):
        expression = expression.replace(match.group(0), str(int(match.group(1)) + int(match.group(2))))

    while match := re.search(r'(\d+) \* (\d+)', expression):
        expression = expression.replace(match.group(0), str(int(match.group(1)) * int(match.group(2))))

    return int(expression)


homework = [line.strip() for line in sys.stdin]

part1 = 0
for expression in homework:
    while match := re.search(r'\(([^()]+)\)', expression):
        expression = expression.replace(match.group(0), str(evaluate_no_precedence(match.group(1))))
    part1 += evaluate_no_precedence(expression)
print(part1)

part2 = 0
for expression in homework:
    while match := re.search(r'\(([^()]+)\)', expression):
        expression = expression.replace(match.group(0), str(evaluate_addition_first(match.group(1))))
    part2 += evaluate_addition_first(expression)
print(part2)
