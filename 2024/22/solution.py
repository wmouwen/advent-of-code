import sys
from functools import cache


@cache
def evolve(secret):
    secret = ((secret << 6) ^ secret) & 16777215
    secret = ((secret >> 5) ^ secret) & 16777215
    secret = ((secret << 11) ^ secret) & 16777215

    return secret


def main():
    new_secret_sum = 0

    for line in sys.stdin:
        if line.strip() == '':
            break

        secret = int(line.strip())
        for _ in range(2000):
            secret = evolve(secret)

        new_secret_sum += secret

    print(new_secret_sum)


if __name__ == '__main__':
    main()
