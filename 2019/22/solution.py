import re
import sys


def simulate(moves, size):
    deck = list(range(size))

    for move in moves:
        if move == 'deal into new stack':
            deck.reverse()

        elif match := re.match(r'cut (-?\d+)', move):
            cut = int(match.group(1))
            deck = deck[cut:] + deck[:cut]

        elif match := re.match(r'deal with increment (\d+)', move):
            increment = int(match.group(1))

            deck, old = [0 for _ in range(len(deck))], deck
            for i in range(len(deck)):
                deck[(increment * i) % len(deck)] = old[i]

    return deck


def shuffle(moves: list[str], size: int):
    a, b = 1, 0

    for move in moves[::-1]:
        if move == 'deal into new stack':
            a = -1 * a
            b = size - b - 1

        elif match := re.match(r'cut (-?\d+)', move):
            cut = int(match.group(1))
            b = (b + cut) % size

        elif match := re.match(r'deal with increment (\d+)', move):
            increment = int(match.group(1))
            modinv = pow(increment, size - 2, size)
            a = (a * modinv) % size
            b = (b * modinv) % size

    return a, b


def main():
    moves = [line.strip() for line in sys.stdin]

    a, b = shuffle(moves, 10007)
    print([(a * i + b) % 10007 for i in range(10007)].index(2019))

    # a, b = shuffle(moves, 119315717514047)
    # print(a, b)

    # a = (a * 101741582076661) % 119315717514047
    # b = (b * 101741582076661) % 119315717514047
    # print(a, b)

    # 2344101622014 - too low
    # print((a * 101741582076661* 2020 + b * 101741582076661) % 119315717514047)


if __name__ == '__main__':
    main()
