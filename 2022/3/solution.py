import sys
from functools import reduce


def score(rucksacks) -> int:
    intersection = reduce(lambda a, b: set(a) & set(b), rucksacks)
    return sum(ord(c) - ord('a') + 1 if 'a' <= c <= 'z' else ord(c) - ord('A') + 27 for c in intersection)


rucksacks = [line.strip() for line in sys.stdin]

print(sum(score([rucksack[:len(rucksack) >> 1], rucksack[len(rucksack) >> 1:]]) for rucksack in rucksacks))
print(sum(score(rucksacks[3 * i:3 * (i + 1)]) for i in range(len(rucksacks) // 3)))
