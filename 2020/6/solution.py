import collections
import sys

groups = [collections.Counter()]
group_sizes = [0]

for line in sys.stdin:
    line = line.strip()

    if not line:
        groups.append(collections.Counter())
        group_sizes.append(0)
        continue

    groups[-1].update(collections.Counter(line))
    group_sizes[-1] += 1

print(sum(len(group) for group in groups))
print(sum(len(set(filter(lambda q: group[q] == group_sizes[index], group))) for index, group in enumerate(groups)))
