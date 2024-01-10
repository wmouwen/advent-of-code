import sys


def spoken_in_turn(turn: int, numbers: list[int]) -> int:
    numbers.reverse()

    while len(numbers) < turn:
        number: int = numbers[0]

        try:
            previous = numbers.index(number, 1)
            numbers.insert(0, previous)
        except ValueError:
            numbers.insert(0, 0)

    return numbers[0]


numbers: list[int] = list(map(int, sys.stdin.readline().strip().split(',')))

print(spoken_in_turn(turn=2020, numbers=numbers.copy()))

# TODO Optimize; keep track of previous position in dict, don't keep on searching a full list.
print(spoken_in_turn(turn=30000000, numbers=numbers.copy()))
