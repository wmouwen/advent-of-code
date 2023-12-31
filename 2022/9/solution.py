import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


movements = {
    'R': Vector(x=1, y=0),
    'D': Vector(x=0, y=1),
    'L': Vector(x=-1, y=0),
    'U': Vector(x=0, y=-1)
}


def follow(locations: list[Vector]) -> list[Vector]:
    tail_locations = [Vector(x=0, y=0)]

    for head in locations[1:]:
        tail = tail_locations[-1]

        if abs(head.x - tail.x) > 1 or abs(head.y - tail.y) > 1:
            tail_locations.append(Vector(
                x=tail.x + (1 if head.x > tail.x else 0) - (1 if head.x < tail.x else 0),
                y=tail.y + (1 if head.y > tail.y else 0) - (1 if head.y < tail.y else 0)
            ))

    return tail_locations


locations = [Vector(x=0, y=0)]
for line in sys.stdin:
    direction, steps = line.strip().split(' ')
    for step in range(int(steps)):
        locations.append(Vector(x=locations[-1].x + movements[direction].x, y=locations[-1].y + movements[direction].y))

locations = follow(locations)
print(len(set(locations)))

for _ in range(8):
    locations = follow(locations)

print(len(set(locations)))
