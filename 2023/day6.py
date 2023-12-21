import re
import sys

times = re.findall(r'\d+', sys.stdin.readline())
distances = re.findall(r'\d+', sys.stdin.readline())

part1 = 1

for i in range(len(times)):
    time = int(times[i])
    distance = int(distances[i])

    options = sum(1 for x in range(1, time) if (time - x) * x > distance)
    part1 *= options

print(part1)

time = int(''.join(times))
distance = int(''.join(distances))
print(sum(1 for x in range(1, time) if (time - x) * x > distance))
