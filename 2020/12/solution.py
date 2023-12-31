import re
import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


movements = {
    'E': Vector(x=1, y=0),
    'S': Vector(x=0, y=1),
    'W': Vector(x=-1, y=0),
    'N': Vector(x=0, y=-1)
}
directions = list(movements.keys())


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 'E'

    def move_direction(self, direction: str, velocity: int):
        self.x += velocity * movements[direction].x
        self.y += velocity * movements[direction].y

    def rotate(self, velocity: int):
        self.direction = directions[(directions.index(self.direction) + int(velocity)) % len(directions)]


instructions = []
for line in sys.stdin:
    action, velocity = re.match(r'(\w)(\d+)', line).groups()
    instructions.append((action, int(velocity)))

ship = Ship()

for action, velocity in instructions:
    if action in movements:
        ship.move_direction(direction=action, velocity=velocity)
    elif action == 'F':
        ship.move_direction(direction=ship.direction, velocity=velocity)
    elif action == 'R':
        ship.rotate(velocity=velocity // 90)
    elif action == 'L':
        ship.rotate(velocity=-1 * (velocity // 90))

print(abs(ship.x) + abs(ship.y))
