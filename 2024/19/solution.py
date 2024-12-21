import re
import sys
from functools import cache


@cache
def towel_arrangements(pattern: str, towels: tuple):
    if pattern == '':
        return 1

    count = 0
    for towel in towels:
        if pattern.startswith(towel):
            count += towel_arrangements(pattern[len(towel):], towels)

    return count


def main():
    towels = tuple(re.findall(r'(\w+)', sys.stdin.readline()))
    sys.stdin.readline()

    possible = 0
    total_possibilities = 0
    for line in sys.stdin:
        arrangements = towel_arrangements(line.strip(), towels)
        possible += int(arrangements > 0)
        total_possibilities += arrangements

    print(possible)
    print(total_possibilities)


if __name__ == '__main__':
    main()
