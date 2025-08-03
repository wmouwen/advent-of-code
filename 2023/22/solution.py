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
        self.top = top
        self.bottom = bottom
        self.supporting: set[Self] = set()
        self.supported_by: set[Self] = set()

    @classmethod
    def from_str(cls, definition: str) -> Self:
        a, b = map(lambda coord: coord.split(','), definition.split('~'))

        return cls(
            top=Vector(
                x=max(int(a[0]), int(b[0])),
                y=max(int(a[1]), int(b[1])),
                z=max(int(a[2]), int(b[2])),
            ),
            bottom=Vector(
                x=min(int(a[0]), int(b[0])),
                y=min(int(a[1]), int(b[1])),
                z=min(int(a[2]), int(b[2])),
            ),
        )

    @property
    def distance_to_ground(self) -> int:
        return self.bottom.z - 1

    def fall(self, distance: int = 1) -> None:
        self.top.z -= distance
        self.bottom.z -= distance

    def is_beneath(self, other: Self) -> bool:
        return (
            self.top.x >= other.bottom.x
            and self.bottom.x <= other.top.x
            and self.top.y >= other.bottom.y
            and self.bottom.y <= other.top.y
            and self.top.z < other.bottom.z
        )

    def supports(self, other: Self) -> bool:
        return self.is_beneath(other) and self.top.z == other.bottom.z - 1


def main():
    bricks = [Brick.from_str(line.strip()) for line in sys.stdin]
    bricks.sort(key=lambda brick: brick.distance_to_ground)

    for i, brick in enumerate(bricks):
        if brick.distance_to_ground == 0:
            continue

        brick.fall(
            min(
                sys.maxsize,
                brick.distance_to_ground,
                *(
                    brick.bottom.z - other.top.z - 1
                    for other in bricks[:i]
                    if other.is_beneath(brick)
                ),
            )
        )

    for a, b in itertools.combinations(bricks, r=2):
        assert isinstance(a, Brick) and isinstance(b, Brick)

        if a.supports(b):
            a.supporting.add(b)
            b.supported_by.add(a)

    safe_to_remove = sum(
        all(len(other.supported_by) != 1 for other in brick.supporting)
        for brick in bricks
    )
    print(safe_to_remove)

    disintegrating_sum = 0
    for brick in bricks:
        chain_reaction = {brick}

        queue: Queue[Brick] = Queue()
        for other in brick.supporting:
            queue.put(other)

        while not queue.empty():
            other = queue.get()

            if len(other.supported_by - chain_reaction) > 0:
                continue

            chain_reaction.add(other)
            for third in other.supporting:
                queue.put(third)

        disintegrating_sum += len(chain_reaction) - 1

    print(disintegrating_sum)


if __name__ == '__main__':
    main()
