import sys

Pattern = list[str]


def solve(pattern: Pattern) -> int:
    # TODO
    print(pattern)
    return 5


points = 0
pattern: Pattern = []
for line in map(lambda line: line.strip(), sys.stdin):
    if not line:
        points += solve(pattern)
        pattern = []
    else:
        pattern.append(line)

points += solve(pattern)

print(points)
