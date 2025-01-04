import os
import sys
from itertools import combinations
from math import prod

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, parse_instructions


def calc_prime_factors(n):
    i = 2
    factors = []

    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)

    return factors


def find_answer(target):
    prime_factors = calc_prime_factors(target)

    return sum([
        sum(
            prod(c)
            for n in range(2, len(prime_factors) + 1)
            for c in combinations(prime_factors, n)
        ),
        sum(prime_factors),
        1
    ])


def main():
    instructions, ip_register = parse_instructions(sys.stdin.readlines())

    for start in [0, 1]:
        device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
        device.registers[0] = start
        device.run(halt_on_ip=3)
        print(find_answer(device.registers[instructions[4][2]]))


if __name__ == '__main__':
    main()
