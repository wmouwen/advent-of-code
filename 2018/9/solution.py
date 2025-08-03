import collections
import re
import sys

match = re.match(
    r'^(?P<players>\d+) players; last marble is worth (?P<max_marble>\d+) points$',
    sys.stdin.readline().strip(),
)

scores = [0 for _ in range(int(match['players']))]
deque = collections.deque()
deque.append(0)

for i in range(1, 100 * int(match['max_marble']) + 1):
    if not i % 23:
        deque.rotate(7)
        scores[i % len(scores)] += i + deque.pop()
        deque.rotate(-1)
    else:
        deque.rotate(-1)
        deque.append(i)

    if i == int(match['max_marble']):
        print(max(scores))

print(max(scores))
