import re
import sys

digits = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}


def digit_value(digit: str) -> int:
    return digits[digit] if digit in digits else int(digit)


part1 = part2 = 0

for line in sys.stdin:
    matches = re.findall(r'\d', line)
    part1 += int(matches[0]) * 10 + int(matches[-1])

    matches = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
    part2 += digit_value(matches[0]) * 10 + digit_value(matches[-1])

print(part1)
print(part2)
