import re
import sys


def play_deterministic(starting_positions: list[int]):
    positions = [position - 1 for position in starting_positions]
    scores = [0 for _ in starting_positions]
    num_dices = 3

    turn = 0
    while all(score < 1000 for score in scores):
        current_player = turn % len(positions)

        dice_throws = (
            ((num_dices * turn + dice) % 100) + 1 for dice in range(num_dices)
        )
        positions[current_player] = (positions[current_player] + sum(dice_throws)) % 10
        scores[current_player] += positions[current_player] + 1

        turn += 1

    return min(scores) * (turn * num_dices)


def count_universes(
    positions: list[int], target: int, scores: list[int] = None
) -> list[int]:
    if scores is None:
        positions = [position - 1 for position in positions]
        scores = [0 for _ in positions]

    if scores[1] >= target:
        return [0, 1]

    wins = [0, 0]

    for roll, frequency in {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}.items():
        universes = count_universes(
            positions=[positions[1], (positions[0] + roll) % 10],
            target=target,
            scores=[scores[1], scores[0] + ((positions[0] + roll) % 10 + 1)],
        )

        wins = [wins[0] + frequency * universes[1], wins[1] + frequency * universes[0]]

    return wins


def main():
    starting_positions = [
        int(re.match(r'Player \d+ starting position: (\d+)', line.strip()).group(1))
        for line in sys.stdin
    ]

    print(play_deterministic(starting_positions))
    print(max(count_universes(positions=starting_positions, target=21)))


if __name__ == '__main__':
    main()
