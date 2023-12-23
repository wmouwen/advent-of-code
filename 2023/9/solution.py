import sys

part1 = 0
part2 = 0

for line in sys.stdin:
    sequences = [[int(x) for x in line.split()]]

    while len([diff for diff in sequences[-1] if diff == 0]) < len(sequences[-1]):
        sequences.append([sequences[-1][i + 1] - sequences[-1][i] for i in range(len(sequences[-1]) - 1)])

    sequences[-1].append(0)
    sequences[-1].insert(0, 0)
    for i in range(len(sequences) - 1, 0, -1):
        sequences[i - 1].append(sequences[i - 1][-1] + sequences[i][-1])
        sequences[i - 1].insert(0, sequences[i - 1][0] - sequences[i][0])

    part1 += sequences[0][-1]
    part2 += sequences[0][0]

print(part1)
print(part2)
