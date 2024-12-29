import sys


def score(deck: list[int]) -> int:
    return sum((len(deck) - i) * card for i, card in enumerate(deck))


def combat(one: tuple[int, ...], two: tuple[int, ...]) -> int:
    one, two = list(one), list(two)

    while len(one) > 0 and len(two) > 0:
        card_one, card_two = one.pop(0), two.pop(0)

        if card_one > card_two:
            one.extend([card_one, card_two])
        else:
            two.extend([card_two, card_one])

    return score(one) if len(one) > 0 else -1 * score(two)


def recursive_combat(one: tuple[int, ...], two: tuple[int, ...]) -> int:
    one, two = list(one), list(two)
    history_one, history_two = set(), set()

    while len(one) > 0 and len(two) > 0:
        # Prevent loops
        if tuple(one) in history_one or tuple(two) in history_two:
            return 1

        history_one.add(tuple(one)), history_two.add(tuple(two))
        card_one, card_two = one.pop(0), two.pop(0)

        if len(one) >= card_one and len(two) >= card_two:
            subscore = recursive_combat(tuple(one[:card_one]), tuple(two[:card_two]))
        else:
            subscore = int(card_one > card_two)

        if subscore > 0:
            one.extend([card_one, card_two])
        else:
            two.extend([card_two, card_one])

    return score(one) if len(one) > 0 else -1 * score(two)


def main():
    players = []

    for line in sys.stdin:
        if line.strip() == '':
            continue

        if line.startswith('Player'):
            players.append([])
            continue

        players[-1].append(int(line.strip()))

    assert len(players) == 2 and len(players[0]) == len(players[1])

    print(abs(combat(*map(tuple, players))))
    print(abs(recursive_combat(*map(tuple, players))))


if __name__ == '__main__':
    main()
