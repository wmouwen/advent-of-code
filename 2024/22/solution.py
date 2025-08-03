import sys
from collections import defaultdict


def evolve(secret):
    secret = ((secret << 6) ^ secret) & 16777215
    secret = ((secret >> 5) ^ secret) & 16777215
    secret = ((secret << 11) ^ secret) & 16777215

    return secret


def main():
    last_secret_sum = 0
    gains = defaultdict(int)

    for line in sys.stdin:
        if line.strip() == '':
            break

        secret = int(line.strip())
        prices = [secret % 10]
        changes = []
        sequences = dict()

        for _ in range(2000):
            secret = evolve(secret)

            prices.append(secret % 10)
            changes.append(prices[-1] - prices[-2])

            if (
                len(changes) >= 4
                and (seq := tuple(changes[-4:])) not in sequences.keys()
            ):
                sequences[seq] = prices[-1]

        last_secret_sum += secret

        for seq, price in sequences.items():
            gains[seq] += price

    print(last_secret_sum)
    print(max(gain for gain in gains.values()))


if __name__ == '__main__':
    main()
