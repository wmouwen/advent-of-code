import re
import sys
from queue import Queue


def main():
    towels = re.findall(r'(\w+)', sys.stdin.readline())
    sys.stdin.readline()

    pattern = '^(' + '|'.join(towels) + ')+$'
    possible = 0
    for line in sys.stdin:
        possible += int(re.match(pattern, line.strip()) is not None)

    print(possible)


if __name__ == '__main__':
    main()
