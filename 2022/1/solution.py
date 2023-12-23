import sys

elves = [0]

for line in sys.stdin:
    if line.strip():
        elves[-1] += int(line)
    else:
        elves.append(0)

elves.sort(reverse=True)

print(elves[0])
print(sum(elves[0:3]))
