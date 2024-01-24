import re
import sys
from dataclasses import dataclass
from typing import NamedTuple, Iterable


class Vector(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class Cuboid:
    on: bool
    x: range
    y: range
    z: range

    def intersect(self, other: 'Cuboid', on: bool) -> 'Cuboid | None':
        intersection = Cuboid(
            on=on,
            x=range(max(self.x.start, other.x.start), min(self.x.stop, other.x.stop)),
            y=range(max(self.y.start, other.y.start), min(self.y.stop, other.y.stop)),
            z=range(max(self.z.start, other.z.start), min(self.z.stop, other.z.stop)),
        )

        if (
            intersection.x.start > intersection.x.stop
            or intersection.y.start > intersection.y.stop
            or intersection.z.start > intersection.z.stop
        ):
            return None

        return intersection


def read_input() -> list[Cuboid]:
    cuboids = []
    regex = r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'

    for line in sys.stdin:
        if match := re.match(regex, line):
            cuboids.append(
                Cuboid(
                    match.group(1) == 'on',
                    range(int(match.group(2)), int(match.group(3))),
                    range(int(match.group(4)), int(match.group(5))),
                    range(int(match.group(6)), int(match.group(7))),
                )
            )

    return cuboids


def reboot(steps: Iterable[Cuboid]) -> int:
    cuboids: list[Cuboid] = []

    for step in steps:
        new_cuboids = []

        if step.on:
            new_cuboids.append(step)

        for cuboid in cuboids:
            intersection = step.intersect(cuboid, not cuboid.on)
            if intersection is not None:
                new_cuboids.append(intersection)

        cuboids.extend(new_cuboids)

    return sum(
        (1 if cuboid.on else -1)
        * (cuboid.x.stop - cuboid.x.start + 1)
        * (cuboid.y.stop - cuboid.y.start + 1)
        * (cuboid.z.stop - cuboid.z.start + 1)
        for cuboid in cuboids
    )


def main():
    cuboids = read_input()

    init_area = Cuboid(
        on=False,
        x=range(-50, 50),
        y=range(-50, 50),
        z=range(-50, 50),
    )
    init_area_cuboids = filter(
        lambda cuboid: cuboid is not None,
        [init_area.intersect(cuboid, cuboid.on) for cuboid in cuboids],
    )

    print(reboot(init_area_cuboids))
    print(reboot(cuboids))


if __name__ == '__main__':
    main()
