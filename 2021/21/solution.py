import re
import sys


def main():
    positions = [
        int(re.match(r'Player \d+ starting position: (\d+)', line.strip()).group(1)) - 1
        for line in sys.stdin
    ]
    scores = [0 for _ in range(len(positions))]

    turn = 0
    num_dices = 3
    while all(score < 1000 for score in scores):
        player = turn % len(positions)
        throw = sum(((num_dices * turn + dice) % 100) + 1 for dice in range(num_dices))

        positions[player] = (positions[player] + throw) % 10
        scores[player] += positions[player] + 1
        turn += 1

    print(min(scores) * (turn * num_dices))


if __name__ == '__main__':
    main()
