import re
import sys
from typing import Self, NamedTuple


class Vector(NamedTuple):
    x: int
    y: int
    z: int = None


class Hailstone:
    def __init__(self, start: Vector, velocity: Vector):
        self.start = start
        self.velocity = velocity

    @classmethod
    def from_str(cls, definition: str) -> Self:
        x, y, z, vx, vy, vz = re.match(
            pattern=r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)',
            string=definition
        ).groups()

        return cls(
            start=Vector(x=int(x), y=int(y), z=int(z)),
            velocity=Vector(x=int(vx), y=int(vy), z=int(vz))
        )

    @property
    def xy_slope(self) -> float:
        return self.velocity.y / self.velocity.x

    @property
    def xy_offset(self) -> float:
        return self.start.y - self.start.x * self.xy_slope

    def xy_intersection(self, other: Self) -> Vector | None:
        if self.xy_slope == other.xy_slope:
            return None

        x = (other.xy_offset - self.xy_offset) / (self.xy_slope - other.xy_slope)
        y = self.xy_slope * x + self.xy_offset

        return Vector(x=x, y=y)

    def in_future(self, point: Vector) -> bool:
        return 0 <= (point.x - self.start.x) / self.velocity.x


test_area = (200000000000000, 400000000000000)
hailstones = [Hailstone.from_str(line.strip()) for line in sys.stdin]
intersections = 0

for i, stone in enumerate(hailstones):
    for other in hailstones[:i]:
        intersection = stone.xy_intersection(other)
        if intersection is None:
            continue

        if not test_area[0] <= intersection.x <= test_area[1] or not test_area[0] <= intersection.y <= test_area[1]:
            continue

        if not stone.in_future(intersection) or not other.in_future(intersection):
            continue

        intersections += 1

print(intersections)
