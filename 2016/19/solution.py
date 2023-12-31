import collections
import sys

elves = int(sys.stdin.readline().strip())

# Part 1
circle = collections.deque(range(1, elves + 1))

while len(circle) > 1:
    circle.rotate(-1)
    circle.popleft()

print(circle.popleft())

# Part 2
circle = collections.deque(range(1, elves + 1))
circle.rotate(-1 * (len(circle) // 2))

while len(circle) > 1:
    circle.popleft()
    circle.rotate((len(circle) % 2) - 1)

print(circle.popleft())
