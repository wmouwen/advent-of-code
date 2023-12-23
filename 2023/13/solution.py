import sys

Pattern = list[str]


def find_reflection(pattern: Pattern, smudges: int) -> int:
    score = 0

    for pivot in range(len(pattern) - 1):
        reflection = True
        offset = 0
        smudges_left = smudges

        while pivot - offset >= 0 and pivot + 1 + offset < len(pattern):
            top = pattern[pivot - offset]
            bottom = pattern[pivot + 1 + offset]

            if top != bottom:
                smudges_found = sum(1 for pair in zip(top, bottom) if pair[0] != pair[1])
                if smudges_found > smudges_left:
                    reflection = False
                    break

                smudges_left -= smudges_found

            offset += 1

        if reflection and smudges_left == 0:
            score += pivot + 1

    return score


part1 = 0
part2 = 0
pattern: Pattern = []
for line in map(lambda line: list(line.strip()), sys.stdin):
    if not line:
        part1 += 100 * find_reflection(pattern, 0) + find_reflection(list(zip(*pattern)), 0)
        part2 += 100 * find_reflection(pattern, 1) + find_reflection(list(zip(*pattern)), 1)
        pattern = []
    else:
        pattern.append(line)

part1 += 100 * find_reflection(pattern, 0) + find_reflection(list(zip(*pattern)), 0)
part2 += 100 * find_reflection(pattern, 1) + find_reflection(list(zip(*pattern)), 1)

print(part1)
print(part2)
