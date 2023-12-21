import re
import sys
import time

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
print(nodes)
while len([node for node in nodes if node[2] != 'Z']):
    for i in range(len(nodes)):
        nodes[i] = edges[nodes[i]][0 if sequence[step % len(sequence)] == 'L' else 1]
    step += 1

    # print(nodes)
    if nodes[1][2] == 'Z':
        print(step)
        time.sleep(1)

# FIXME
print(step)
