import sys


def hash_sequence(algorithm: str) -> int:
    value = 0

    for char in algorithm:
        value = ((value + ord(char)) * 17) % 256

    return value


init_sequence = sys.stdin.readline().strip().split(',')

print(sum(hash_sequence(algorithm) for algorithm in init_sequence))
