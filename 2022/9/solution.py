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
    tail_locations = locations[:1]

    for head in locations[1:]:
        tail = tail_locations[-1]

        if abs(head.x - tail.x) > 1 or abs(head.y - tail.y) > 1:
            tail_locations.append(Vector(
                x=tail.x + (head.x > tail.x) - (head.x < tail.x),
                y=tail.y + (head.y > tail.y) - (head.y < tail.y)
            ))

    return tail_locations


locations = [Vector(x=0, y=0)]
for line in sys.stdin:
    direction, steps = line.strip().split(' ')
    for step in range(int(steps)):
        locations.append(Vector(
            x=locations[-1].x + movements[direction].x,
            y=locations[-1].y + movements[direction].y
        ))

for knot in range(1, 10):
    locations = follow(locations)
    if knot in [1, 9]:
        print(len(set(locations)))
