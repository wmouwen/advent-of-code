import re
import sys


def shuffle(deck, moves):
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


def main():
    moves = [line.strip() for line in sys.stdin]

    print(shuffle(list(range(10007)), moves).index(2019))

    # TODO Part 2: Instead of tracking the entire deck, only track the requested card.


if __name__ == '__main__':
    main()
