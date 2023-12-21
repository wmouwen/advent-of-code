import math
import sys
import itertools


def find_target(combinations) -> int:
    for combination in combinations:
        if sum(combination) == 2020:
            return math.prod(combination)


input = [int(line) for line in sys.stdin]

print(find_target(itertools.combinations(input, 2)))
print(find_target(itertools.combinations(input, 3)))
