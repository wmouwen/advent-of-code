import sys
from collections import defaultdict


def blink(stones: dict[int, int]) -> dict[int, int]:
    output = defaultdict(int)

    for value, count in stones.items():
        if value == 0:
            output[1] += count
        elif (strlen := len(str(value))) % 2 == 0:
            sep = pow(10, strlen // 2)
            output[value // sep] += count
            output[value % sep] += count
        else:
            output[value * 2024] += count

    return output


def main():
    stones = defaultdict(int)
    for value in map(int, sys.stdin.readline().strip().split(' ')):
        stones[value] += 1

    for i in range(25):
        stones = blink(stones)
    print(sum(stones.values()))

    for i in range(75 - 25):
        stones = blink(stones)
    print(sum(stones.values()))


if __name__ == '__main__':
    main()
