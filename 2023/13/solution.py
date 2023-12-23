import sys

Pattern = list[str]


def horizontal_reflections(pattern: Pattern) -> int:
    score = 0

    for pivot in range(len(pattern) - 1):
        reflection = True
        offset = 0

        while pivot - offset >= 0 and pivot + 1 + offset < len(pattern):
            if pattern[pivot - offset] != pattern[pivot + 1 + offset]:
                reflection = False
                break
            offset += 1

        if reflection:
            score += pivot + 1

    return score


points = 0
pattern: Pattern = []
for line in map(lambda line: line.strip(), sys.stdin):
    if not line:

        points += 100 * horizontal_reflections(pattern) + horizontal_reflections(list(zip(*pattern)))
        pattern = []
    else:
        pattern.append(line)

points += 100 * horizontal_reflections(pattern) + horizontal_reflections(list(zip(*pattern)))

print(points)
