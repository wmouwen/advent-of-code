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
        if n % i == 0:
            factors.append(i)
            n //= i
        else:
            i += 1

    if n > 1:
        factors.append(n)

    return factors


def find_answer(target):
    prime_factors = calc_prime_factors(target)

    return 1 + sum(prod(c) for n in range(len(prime_factors)) for c in combinations(prime_factors, n + 1))


def main():
    instructions, ip_register = parse_instructions(sys.stdin.readlines())
    target_register = instructions[4][2]

    device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
    device.run(halt_on_ip=3)
    print(find_answer(device.registers[target_register]))

    device.reset()
    device.registers[0] = 1
    device.run(halt_on_ip=3)
    print(find_answer(device.registers[target_register]))


if __name__ == '__main__':
    main()
