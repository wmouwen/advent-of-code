import copy
import re
import sys

stacks_part1 = {}
stacks_part2 = {}

for line in sys.stdin:
    if re.match(r'^\s+(\d\s+)+$', line):
        break

    for match in re.finditer(r'\[(?P<char>\w)]', line.rstrip("\n")):
        index = int(match.start()) // 4 + 1

        if index not in stacks_part1:
            stacks_part1[index] = []

        stacks_part1[index].insert(0, match['char'])

stacks_part2 = copy.deepcopy(stacks_part1)

for line in sys.stdin:
    match = re.match(r'move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)', line)
    if match is None:
        continue

    for _ in range(int(match['count'])):
        stacks_part1[int(match['to'])].append(stacks_part1[int(match['from'])].pop())

    stacks_part2[int(match['to'])].extend(stacks_part2[int(match['from'])][-1 * int(match['count']):])
    stacks_part2[int(match['from'])] = stacks_part2[int(match['from'])][:-1 * int(match['count'])]

print(''.join(stacks_part1[key][-1] for key in sorted(stacks_part1)))
print(''.join(stacks_part2[key][-1] for key in sorted(stacks_part2)))
