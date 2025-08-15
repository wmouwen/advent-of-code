import math
import statistics
import sys


def main():
    points = tuple(map(int, sys.stdin.readline().strip().split(',')))

    median = int(statistics.median(points))
    print(sum(abs(point - median) for point in points))

    mean = statistics.mean(points)
    fuel = min(
        sum((dist := abs(point - candidate)) * (dist + 1) // 2 for point in points)
        for candidate in range(math.floor(mean), math.ceil(mean) + 1)
    )
    print(fuel)


if __name__ == '__main__':
    main()
