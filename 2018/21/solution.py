import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device'))
)
from device import parse_instructions


def main():
    instructions, ip_register = parse_instructions(sys.stdin.readlines())
    seed, prime = instructions[7][1], instructions[11][2]

    nr, cycle = 0, 0
    seen = list()

    while True:
        nr = calc_next_nr(nr, seed, prime)

        if len(seen) == 0:
            print(nr)

        if nr in seen:
            print(seen[-1])
            break

        seen.append(nr)


def calc_next_nr(nr: int, seed: int, prime: int):
    x = nr | 65536
    nr = seed

    while x > 0:
        nr = (nr + (x & 255)) & 16777215
        nr = (nr * prime) & 16777215
        x >>= 8

    return nr


if __name__ == '__main__':
    main()
