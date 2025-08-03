import json
import sys
from copy import deepcopy
from functools import reduce
from itertools import permutations

Snailfish = list[int | list] | int


def explode_first(
    number: Snailfish, depth: int = 0
) -> (Snailfish, tuple[int, int] | None):
    if isinstance(number, int):
        return number, None

    if depth == 4:
        return 0, number

    number[0], carry = explode_first(number[0], depth + 1)
    if carry is not None:
        if isinstance(number[1], int):
            number[1] += carry[1]
        else:
            target = number[1]
            while isinstance(target[0], list):
                target = target[0]
            target[0] += carry[1]
        return number, (carry[0], 0)

    number[1], carry = explode_first(number[1], depth + 1)
    if carry is not None:
        if isinstance(number[0], int):
            number[0] += carry[0]
        else:
            target = number[0]
            while isinstance(target[1], list):
                target = target[1]
            target[1] += carry[0]
        return number, (0, carry[1])

    return number, None


def split_first(number: Snailfish) -> (Snailfish, bool):
    if isinstance(number, int):
        if number >= 10:
            return [number >> 1, number - (number >> 1)], True

        return number, False

    for i in range(len(number)):
        number[i], is_split = split_first(number[i])
        if is_split:
            return number, True

    return number, False


def reduce_snailfish(number: Snailfish) -> Snailfish:
    number = deepcopy(number)

    while True:
        number, carry = explode_first(number)
        if carry is not None:
            continue

        number, is_split = split_first(number)
        if is_split:
            continue

        break

    return number


def magnitude(number: Snailfish) -> int:
    if isinstance(number, int):
        return number

    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def main():
    snailfishes = [json.loads(line.strip()) for line in sys.stdin.readlines()]

    print(
        magnitude(
            reduce(lambda carry, item: reduce_snailfish([carry, item]), snailfishes)
        )
    )

    print(
        max(
            magnitude(reduce_snailfish([a, b])) for a, b in permutations(snailfishes, 2)
        )
    )


if __name__ == '__main__':
    main()
