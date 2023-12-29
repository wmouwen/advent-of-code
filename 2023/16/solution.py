import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Beam(NamedTuple):
    location: Vector
    direction: str


directions = {
    'R': Vector(x=1, y=0),
    'D': Vector(x=0, y=1),
    'L': Vector(x=-1, y=0),
    'U': Vector(x=0, y=-1)
}


def energized_tiles(contraption: tuple, start: Beam) -> int:
    beams = tuple(tuple([] for tile in row) for row in contraption)
    todo: [(Vector, str)] = [start]

    while todo:
        beam = todo.pop()

        # Check out of bounds
        if not 0 <= beam.location.y < len(beams) or not 0 <= beam.location.x < len(beams[beam.location.y]):
            continue

        # Check revisit
        if beam.direction in beams[beam.location.y][beam.location.x]:
            continue

        # Energize field
        beams[beam.location.y][beam.location.x].append(beam.direction)

        # Forward beam
        new_directions = []

        if contraption[beam.location.y][beam.location.x] == '.':
            new_directions.append(beam.direction)
        elif contraption[beam.location.y][beam.location.x] == '/':
            new_directions.append({'R': 'U', 'D': 'L', 'L': 'D', 'U': 'R'}[beam.direction])
        elif contraption[beam.location.y][beam.location.x] == '\\':
            new_directions.append({'R': 'D', 'D': 'R', 'L': 'U', 'U': 'L'}[beam.direction])
        elif contraption[beam.location.y][beam.location.x] == '|':
            new_directions.extend(['D', 'U'] if beam.direction in ['R', 'L'] else beam.direction)
        elif contraption[beam.location.y][beam.location.x] == '-':
            new_directions.extend(['R', 'L'] if beam.direction in ['D', 'U'] else beam.direction)

        for direction in new_directions:
            todo.append(Beam(
                location=Vector(x=beam.location.x + directions[direction].x,
                                y=beam.location.y + directions[direction].y),
                direction=direction
            ))

    return sum(1 for row in beams for tile in row if tile)


contraption = tuple(tuple(line.strip()) for line in sys.stdin)

best = energized_tiles(contraption, Beam(location=Vector(x=0, y=0), direction='R'))
print(best)

for y in range(len(contraption)):
    best = max(
        best,
        energized_tiles(contraption, Beam(location=Vector(x=0, y=y), direction='R')),
        energized_tiles(contraption, Beam(location=Vector(x=len(contraption) - 1, y=y), direction='L'))
    )

for x in range(len(contraption[0])):
    best = max(
        best,
        energized_tiles(contraption, Beam(location=Vector(x=x, y=0), direction='D')),
        energized_tiles(contraption, Beam(location=Vector(x=x, y=len(contraption) - 1), direction='U'))
    )

print(best)