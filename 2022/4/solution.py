import sys

part1 = 0
part2 = 0

for line in sys.stdin:
    pairs = list(map(lambda x: tuple(map(int, x.split('-'))), line.strip().split(',')))

    if (pairs[0][0] >= pairs[1][0] and pairs[0][1] <= pairs[1][1]) or (
        pairs[1][0] >= pairs[0][0] and pairs[1][1] <= pairs[0][1]
    ):
        part1 += 1

    if len(
        set([i for i in range(pairs[0][0], pairs[0][1] + 1)])
        & set([i for i in range(pairs[1][0], pairs[1][1] + 1)])
    ):
        part2 += 1

print(part1)
print(part2)
