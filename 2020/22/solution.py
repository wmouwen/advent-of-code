import sys


def combat(one: list[int], two: list[int]):
    one, two = one.copy(), two.copy()

    while len(one) > 0 and len(two) > 0:
        a, b = one.pop(0), two.pop(0)
        (one if a > b else two).extend(sorted([a, b], reverse=True))

    winner = one if len(one) > 0 else two

    return sum((len(winner) - i) * card for i, card in enumerate(winner))


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

    print(combat(*players))


if __name__ == '__main__':
    main()
