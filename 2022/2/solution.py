import sys

part1 = 0
part2 = 0

for line in sys.stdin:
    a, b = line.strip().split(' ')
    left = ord(a) - ord('A')
    right = ord(b) - ord('X')

    part1 += 3 * ((right - left + 1) % 3) + right + 1
    part2 += 3 * right + ((left + right - 1) % 3) + 1

print(part1)
print(part2)
