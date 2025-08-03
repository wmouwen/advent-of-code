import re
import sys


class Number:
    def __init__(self, line: int, start: int, end: int, value: int):
        self.line = line
        self.start = start
        self.end = end
        self.value = value


class Symbol:
    def __init__(self, line: int, location: int, symbol: str):
        self.line = line
        self.location = location
        self.symbol = symbol


line_number = 0
numbers: list[Number] = []
symbols: list[Symbol] = []

for line in sys.stdin:
    for match in re.finditer(r'\d+', line.strip()):
        numbers.append(
            Number(line_number, match.start(), match.end() - 1, int(match[0]))
        )

    for match in re.finditer(r'[^\d.]', line.strip()):
        symbols.append(Symbol(line_number, match.start(), match[0]))

    line_number += 1

part1 = 0
for number in numbers:
    for symbol in symbols:
        if (
            number.line - 1 <= symbol.line <= number.line + 1
            and number.start - 1 <= symbol.location <= number.end + 1
        ):
            # print(number.value, number.start, number.end, symbol.symbol)
            part1 += number.value
            break

print(part1)

part2 = 0

for symbol in symbols:
    if symbol.symbol != '*':
        continue

    gears_count = 0
    gears_ratio = 1
    for number in numbers:
        if (
            number.line - 1 <= symbol.line <= number.line + 1
            and number.start - 1 <= symbol.location <= number.end + 1
        ):
            gears_count += 1
            gears_ratio *= number.value

    if gears_count == 2:
        part2 += gears_ratio

print(part2)
