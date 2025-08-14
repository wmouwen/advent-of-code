import sys
from itertools import combinations
from math import prod


def main():
    wrapping_paper, ribbon = 0, 0

    for line in sys.stdin:
        box = tuple(sorted(map(int, line.strip().split('x'))))
        sides = tuple(a * b for a, b in combinations(box, 2))

        wrapping_paper += 2 * sum(sides) + min(sides)
        ribbon += 2 * (sum(box) - max(box)) + prod(box)

    print(wrapping_paper)
    print(ribbon)


if __name__ == '__main__':
    main()
