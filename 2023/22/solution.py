import itertools
import sys
from queue import Queue
from typing import Self


class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Brick:
    def __init__(self, top: Vector, bottom: Vector):
        self.id = '?'
        self.top = top
        self.bottom = bottom
        self.supporting: list[Self] = []
        self.supported_by: list[Self] = []

    @classmethod
    def from_str(cls, definition: str) -> Self:
        a, b = map(lambda coord: coord.split(','), definition.split('~'))

        return cls(
            top=Vector(x=max(int(a[0]), int(b[0])), y=max(int(a[1]), int(b[1])), z=max(int(a[2]), int(b[2]))),
            bottom=Vector(x=min(int(a[0]), int(b[0])), y=min(int(a[1]), int(b[1])), z=min(int(a[2]), int(b[2])))
        )

    @property
    def distance_to_ground(self) -> int:
        return self.bottom.z - 1

    def fall(self, distance: int = 1) -> None:
        self.top.z -= distance
        self.bottom.z -= distance

    def is_beneath(self, other: Self) -> bool:
        return (self.top.x >= other.bottom.x and self.bottom.x <= other.top.x and
                self.top.y >= other.bottom.y and self.bottom.y <= other.top.y and
                self.top.z < other.bottom.z)

    def supports(self, other: Self) -> bool:
        return self.is_beneath(other) and self.top.z == other.bottom.z - 1


bricks = [Brick.from_str(line.strip()) for line in sys.stdin]
for i, brick in enumerate(bricks):
    brick.id = chr(ord('A') + i)
bricks.sort(key=lambda brick: brick.distance_to_ground)

for i, brick in enumerate(bricks):
    if brick.distance_to_ground == 0:
        continue

    brick.fall(min(
        brick.distance_to_ground,
        *(brick.bottom.z - other.top.z - 1 for other in bricks[:i] if other.is_beneath(brick))
    ))

for a, b in itertools.combinations(bricks, 2):
    assert isinstance(a, Brick) and isinstance(b, Brick)

    if a.supports(b):
        a.supporting.append(b)
        b.supported_by.append(a)

safe_to_remove = sum(all(len(other.supported_by) != 1 for other in brick.supporting) for brick in bricks)
print(safe_to_remove)
