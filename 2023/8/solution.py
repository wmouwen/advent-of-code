import math
import re
import sys

sequence = list(sys.stdin.readline().strip())
edges = {}

for line in sys.stdin:
    match = re.match(r'(?P<source>\w+) = \((?P<left>\w+), (?P<right>\w+)\)', line)
    if not match:
        continue

    edges[match.group('source')] = (match.group('left'), match.group('right'))

step = 0
node = 'AAA'
while node != 'ZZZ':
    node = edges[node][0 if sequence[step % len(sequence)] == 'L' else 1]
    step += 1

print(step)

step = 0
nodes = [node for node in edges.keys() if node[2] == 'A']
first_finish: list[int | None] = [None for node in nodes]

while len([node for node in first_finish if node is None]):
    for i in range(len(nodes)):
        nodes[i] = edges[nodes[i]][0 if sequence[step % len(sequence)] == 'L' else 1]

        if nodes[i][2] == 'Z' and first_finish[i] is None:
            first_finish[i] = step + 1

    step += 1

print(math.lcm(*first_finish))
