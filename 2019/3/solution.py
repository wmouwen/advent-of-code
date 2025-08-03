import sys
from collections import namedtuple

Coord = namedtuple('Coord', 'x y')
dirs = {
    'R': Coord(x=1, y=0),
    'D': Coord(x=0, y=1),
    'L': Coord(x=-1, y=0),
    'U': Coord(x=0, y=-1),
}

wires = []

for line in sys.stdin:
    wires.append({})
    current = Coord(x=0, y=0)
    step = 0

    for segment in line.strip().split(','):
        direction = dirs[segment[0]]

        for _ in range(int(segment[1:])):
            current = Coord(x=current.x + direction.x, y=current.y + direction.y)
            step += 1
            wires[-1][current] = step

intersections = set(wires[0].keys()) & set(wires[1].keys())

print(min(abs(coord.x) + abs(coord.y) for coord in intersections))
print(min(wires[0][coord] + wires[1][coord] for coord in intersections))
