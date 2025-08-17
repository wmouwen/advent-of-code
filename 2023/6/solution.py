import re
import sys
from math import sqrt, ceil, floor, prod


def options(time: int, distance: int) -> int:
    """
    Solve equation (time - hold) * hold > distance, with 0 < hold < time
    """
    discriminator = time**2 - 4 * (distance + 1)
    roots = (
        (time - sqrt(discriminator)) / 2,
        (time + sqrt(discriminator)) / 2,
    )

    option_count = min(distance - 1, floor(roots[1])) - max(1, ceil(roots[0])) + 1

    return max(0, option_count)


def main():
    times = re.findall(r'\d+', sys.stdin.readline())
    distances = re.findall(r'\d+', sys.stdin.readline())

    options_prod = prod(
        options(time, distance)
        for time, distance in zip(map(int, times), map(int, distances))
    )
    print(options_prod)

    print(options(int(''.join(times)), int(''.join(distances))))


if __name__ == '__main__':
    main()
