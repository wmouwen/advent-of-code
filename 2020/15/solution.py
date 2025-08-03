import sys


def spoken_in_turn(turns: int, numbers: list[int]) -> int:
    last_occurrence = dict(
        (number, turn + 1) for turn, number in enumerate(numbers[:-1])
    )
    previous = numbers[-1]
    turn = len(numbers)

    while turn < turns:
        offset = turn - last_occurrence[previous] if previous in last_occurrence else 0

        last_occurrence[previous] = turn
        previous = offset
        turn += 1

    return previous


numbers = list(map(int, sys.stdin.readline().strip().split(',')))

print(spoken_in_turn(turns=2020, numbers=numbers.copy()))
print(spoken_in_turn(turns=30000000, numbers=numbers.copy()))
