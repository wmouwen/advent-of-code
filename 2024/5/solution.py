import functools
import re
import sys
from math import floor


def main():
    rules = {}

    for line in sys.stdin:
        if '|' not in line:
            break

        (left, right) = map(int, line.strip().split('|'))
        if left not in rules:
            rules[left] = []
        rules[left].append(right)

    def compare(x, y) -> int:
        if x in rules and y in rules[x]:
            return -1
        if y in rules and x in rules[y]:
            return 1
        return 0

    sorted_sum = 0
    unsorted_sum = 0
    for line in sys.stdin:
        update = list(map(int, line.strip().split(',')))
        sorted_update = sorted(update, key=functools.cmp_to_key(compare))

        if update == sorted_update:
            sorted_sum += update[floor(len(update)/2)]
        else:
            unsorted_sum += sorted_update[floor(len(update)/2)]

    print(sorted_sum)
    print(unsorted_sum)


if __name__ == '__main__':
    main()
