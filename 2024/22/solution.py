import sys
from collections import defaultdict


def main():
    secrets_sum = 0
    gains = defaultdict(int)

    for secret in map(int, sys.stdin.readlines()):
        if not secret:
            continue

        sequence, seen = tuple(), set()

        for _ in range(2000):
            old_price = secret % 10

            secret = ((secret * 64) ^ secret) % 16777216
            secret = (secret // 32) ^ secret
            secret = ((secret * 2048) ^ secret) % 16777216

            price = secret % 10

            sequence = sequence[-3:] + (price - old_price,)
            if len(sequence) == 4 and sequence not in seen:
                gains[sequence] += price
                seen.add(sequence)

        secrets_sum += secret

    print(secrets_sum)
    print(max(gains.values()))


if __name__ == '__main__':
    main()
