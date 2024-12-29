import re
import sys


def get_coefficients(moves: list[str], deck_size: int):
    a, b = 1, 0

    for move in moves[::-1]:
        if match := re.match(r'cut (-?\d+)', move):
            cut = int(match.group(1))
            b = (b + cut) % deck_size

        elif move == 'deal into new stack':
            a, b = -1 * a, deck_size - b - 1

        elif match := re.match(r'deal with increment (\d+)', move):
            increment = int(match.group(1))
            modinv = pow(increment, deck_size - 2, deck_size)
            a, b = (a * modinv) % deck_size, (b * modinv) % deck_size

        else:
            raise Exception(f'Unknown move "{move}"')

    return a, b


def polypow(a, b, power, modulo):
    if power == 0:
        return 1, 0

    if power & 1 == 0:
        return polypow((a * a) % modulo, ((a + 1) * b) % modulo, power >> 1, modulo)

    c, d = polypow(a, b, power - 1, modulo)
    return (a * c) % modulo, (a * d + b) % modulo


def main():
    moves = [line.strip() for line in sys.stdin]

    deck_size = 10007
    a, b = get_coefficients(moves, deck_size)
    deck = [(a * i + b) % deck_size for i in range(deck_size)]
    print(deck.index(2019))

    deck_size = 119315717514047
    a, b = get_coefficients(moves, deck_size)
    a, b = polypow(a, b, power=101741582076661, modulo=deck_size)
    print((a * 2020 + b) % deck_size)


if __name__ == '__main__':
    main()
