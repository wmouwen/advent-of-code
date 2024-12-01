import re
import sys


def main():
    left, right = [], []

    for line in sys.stdin:
        if match := re.match(r'^(?P<left>\d+)\s+(?P<right>\d+)$', line.strip()):
            left.append(int(match['left']))
            right.append(int(match['right']))

    left.sort()
    right.sort()

    print(sum(abs(left[i] - right[i]) for i in range(len(left))))
    print(sum(left[i] * sum(1 for j in range(len(right)) if right[j] == left[i]) for i in range(len(left))))


if __name__ == '__main__':
    main()
