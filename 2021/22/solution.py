import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Cuboid:
    on: bool
    x: range
    y: range
    z: range

    def intersect(self, other: 'Cuboid', on: bool) -> 'Cuboid | None':
        x = range(max(self.x.start, other.x.start), min(self.x.stop, other.x.stop))
        y = range(max(self.y.start, other.y.start), min(self.y.stop, other.y.stop))
        z = range(max(self.z.start, other.z.start), min(self.z.stop, other.z.stop))

        if x.start <= x.stop and y.start <= y.stop and z.start <= z.stop:
            return Cuboid(on=on, x=x, y=y, z=z)

        return None

    def volume(self) -> int:
        return (
            (self.x.stop - self.x.start + 1)
            * (self.y.stop - self.y.start + 1)
            * (self.z.stop - self.z.start + 1)
        )


def read_input() -> Iterable[Cuboid]:
    cuboids = []
    regex = r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'

    for line in sys.stdin:
        if match := re.match(regex, line):
            x = range(int(match.group(2)), int(match.group(3)))
            y = range(int(match.group(4)), int(match.group(5)))
            z = range(int(match.group(6)), int(match.group(7)))
            cuboids.append(Cuboid(on=match.group(1) == 'on', x=x, y=y, z=z))

    return cuboids


def reboot(steps: Iterable[Cuboid]) -> int:
    cuboids = []

    for step in steps:
        cuboids.extend(filter(None, [step.intersect(c, not c.on) for c in cuboids]))
        if step.on:
            cuboids.append(step)

    return sum((1 if c.on else -1) * c.volume() for c in cuboids)


def main():
    cuboids = read_input()

    init_area = Cuboid(on=False, x=range(-50, 50), y=range(-50, 50), z=range(-50, 50))
    init_cuboids = filter(None, [init_area.intersect(c, c.on) for c in cuboids])
    print(reboot(init_cuboids))

    print(reboot(cuboids))


if __name__ == '__main__':
    main()
