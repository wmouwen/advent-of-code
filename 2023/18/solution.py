import sys
from collections import namedtuple


def surface(corners) -> int:
    area = 0
    boundary_length = 0

    for i in range(len(corners) - 1):
        area += corners[i].x * corners[i + 1].y - corners[i].y * corners[i + 1].x
        boundary_length += abs(corners[i + 1].x + corners[i + 1].y - (corners[i].x + corners[i].y))

    return (area + boundary_length) // 2 + 1


Coord = namedtuple('Coord', 'x y')

corners_part1 = [Coord(x=0, y=0)]
corners_part2 = [Coord(x=0, y=0)]

for line in sys.stdin:
    direction, length, color = line.strip().split(' ')

    if direction == 'R':
        corners_part1.append(Coord(x=corners_part1[-1].x + int(length), y=corners_part1[-1].y))
    if direction == 'D':
        corners_part1.append(Coord(x=corners_part1[-1].x, y=corners_part1[-1].y + int(length)))
    if direction == 'L':
        corners_part1.append(Coord(x=corners_part1[-1].x - int(length), y=corners_part1[-1].y))
    if direction == 'U':
        corners_part1.append(Coord(x=corners_part1[-1].x, y=corners_part1[-1].y - int(length)))

    if color[-2] == '0':
        corners_part2.append(Coord(x=corners_part2[-1].x + int(color[2:-2], 16), y=corners_part2[-1].y))
    if color[-2] == '1':
        corners_part2.append(Coord(x=corners_part2[-1].x, y=corners_part2[-1].y + int(color[2:-2], 16)))
    if color[-2] == '2':
        corners_part2.append(Coord(x=corners_part2[-1].x - int(color[2:-2], 16), y=corners_part2[-1].y))
    if color[-2] == '3':
        corners_part2.append(Coord(x=corners_part2[-1].x, y=corners_part2[-1].y - int(color[2:-2], 16)))

print(surface(corners_part1))
print(surface(corners_part2))
