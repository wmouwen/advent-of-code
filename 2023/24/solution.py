from typing import Self, NamedTuple
import re
from sympy import Symbol, solve_poly_system
import sys


class Vector(NamedTuple):
    x: int | Symbol
    y: int | Symbol
    z: int | Symbol = None


class Hailstone:
    def __init__(self, start: Vector, velocity: Vector):
        self.start = start
        self.velocity = velocity

    @classmethod
    def from_str(cls, definition: str) -> Self:
        x, y, z, vx, vy, vz = re.match(
            pattern=r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)',
            string=definition,
        ).groups()

        return cls(
            start=Vector(x=int(x), y=int(y), z=int(z)),
            velocity=Vector(x=int(vx), y=int(vy), z=int(vz)),
        )

    @property
    def xy_slope(self) -> float:
        return self.velocity.y / self.velocity.x

    @property
    def xy_y_intercept(self) -> float:
        return self.start.y - self.start.x * self.xy_slope

    def xy_intersection(self, other: Self) -> Vector | None:
        if self.xy_slope == other.xy_slope:
            return None

        x = (other.xy_y_intercept - self.xy_y_intercept) / (
            self.xy_slope - other.xy_slope
        )
        y = self.xy_slope * x + self.xy_y_intercept

        return Vector(x=x, y=y)

    def in_future(self, point: Vector) -> bool:
        return 0 <= (point.x - self.start.x) / self.velocity.x


hailstones = [Hailstone.from_str(line.strip()) for line in sys.stdin]

test_area = (200000000000000, 400000000000000)
if len(hailstones) == 5:
    test_area = (7, 27)

intersections = 0
for i, hailstone in enumerate(hailstones):
    for other in hailstones[:i]:
        intersection = hailstone.xy_intersection(other)
        if intersection is None:
            continue

        if (
            not test_area[0] <= intersection.x <= test_area[1]
            or not test_area[0] <= intersection.y <= test_area[1]
        ):
            continue

        if not hailstone.in_future(intersection) or not other.in_future(intersection):
            continue

        intersections += 1

print(intersections)

rock = Hailstone(
    start=Vector(Symbol('x'), Symbol('y'), Symbol('z')),
    velocity=Vector(Symbol('vx'), Symbol('vy'), Symbol('vz')),
)

variables = [*rock.start, *rock.velocity]
equations = []

for hailstone in hailstones[:3]:
    variables.append(time := Symbol(f'hailstone_{id(hailstone)}'))
    equations.extend(
        [
            (rock.start.x + rock.velocity.x * time)
            - (hailstone.start.x + hailstone.velocity.x * time),
            (rock.start.y + rock.velocity.y * time)
            - (hailstone.start.y + hailstone.velocity.y * time),
            (rock.start.z + rock.velocity.z * time)
            - (hailstone.start.z + hailstone.velocity.z * time),
        ]
    )

solved_system = solve_poly_system(equations, variables)
print(sum(solved_system[0][:3]))
