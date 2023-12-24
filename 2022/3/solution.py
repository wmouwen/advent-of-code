import sys

rucksacks = []
part1 = 0

for line in sys.stdin:
    stripped = line.strip()
    rucksacks.append(stripped)

    intersection = set(stripped[:len(stripped) >> 1]) & set(stripped[len(stripped) >> 1:])
    for char in intersection:
        if 'a' <= char <= 'z':
            part1 += ord(char) - ord('a') + 1
        else:
            part1 += ord(char) - ord('A') + 27

print(part1)
