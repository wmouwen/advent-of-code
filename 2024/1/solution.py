import re
import sys


def main():
    lefts, rights = [], []

    for line in sys.stdin:
        left, right = map(int, re.findall(r'\d+', line))
        lefts.append(left)
        rights.append(right)

    print(sum(abs(left - right) for left, right in zip(sorted(lefts), sorted(rights))))
    print(sum(left * rights.count(left) for left in lefts))


if __name__ == '__main__':
    main()
