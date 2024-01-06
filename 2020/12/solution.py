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


class Waypoint:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 'E'
        self.waypoint = Waypoint(dx=10, dy=-1)

    def rotate(self, degrees: int):
        self.direction = directions[(directions.index(self.direction) + int(degrees // 90)) % len(directions)]
        for _ in range(int(degrees // 90) % 4):
            self.waypoint.dx, self.waypoint.dy = -1 * self.waypoint.dy, self.waypoint.dx

    def move_to_direction(self, direction: str, velocity: int):
        self.x += velocity * movements[direction].x
        self.y += velocity * movements[direction].y

    def move_to_waypoint(self, velocity: int):
        self.x += velocity * self.waypoint.dx
        self.y += velocity * self.waypoint.dy

    def move_waypoint(self, direction: str, velocity: int):
        self.waypoint.dx += velocity * movements[direction].x
        self.waypoint.dy += velocity * movements[direction].y


ship1, ship2 = Ship(), Ship()
for line in sys.stdin:
    action, velocity = re.match(r'(\w)(\d+)', line).groups()

    if action in movements:
        ship1.move_to_direction(direction=action, velocity=int(velocity))
        ship2.move_waypoint(direction=action, velocity=int(velocity))
    elif action == 'F':
        ship1.move_to_direction(direction=ship1.direction, velocity=int(velocity))
        ship2.move_to_waypoint(velocity=int(velocity))
    elif action == 'R':
        ship1.rotate(degrees=int(velocity))
        ship2.rotate(degrees=int(velocity))
    elif action == 'L':
        ship1.rotate(degrees=-1 * int(velocity))
        ship2.rotate(degrees=-1 * int(velocity))

print(abs(ship1.x) + abs(ship1.y))
print(abs(ship2.x) + abs(ship2.y))
