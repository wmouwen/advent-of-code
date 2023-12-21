import math
import sys


def hits(trees, dx, dy) -> int:
    hits = 0

    for tick in range(0, math.ceil(len(trees) / dy)):
        y = tick * dy
        x = tick * dx % len(trees[y])
        hits += trees[y][x]

    return hits


trees = [([char == '#' for char in line.strip()]) for line in sys.stdin]

tree_hits = [
    hits(trees, 1, 1),
    part_one := hits(trees, 3, 1),
    hits(trees, 5, 1),
    hits(trees, 7, 1),
    hits(trees, 1, 2),
]

print(part_one)
print(math.prod(tree_hits))
