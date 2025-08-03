import re
import sys
from functools import reduce
from queue import PriorityQueue
from typing import NamedTuple, Self


class V(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: Self) -> Self:
        return V(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return V(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __rshift__(self, p: int) -> Self:
        return V(x=self.x >> p, y=self.y >> p, z=self.z >> p)

    def dist(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


ORIGIN = V(0, 0, 0)


class Bot(NamedTuple):
    v: V
    range: int


class Box(NamedTuple):
    min: V
    max: V

    @property
    def valid(self) -> bool:
        return (
            self.max.x > self.min.x
            and self.max.y > self.min.y
            and self.max.z > self.min.z
        )

    @property
    def size(self) -> V:
        return self.max - self.min

    def dist(self, v: V):
        return (
            max(0, self.min.x - v.x)
            + max(0, v.x - (self.max.x - 1))
            + max(0, self.min.y - v.y)
            + max(0, v.y - (self.max.y - 1))
            + max(0, self.min.z - v.z)
            + max(0, v.z - (self.max.z - 1))
        )

    @property
    def subboxes(self) -> list[Self]:
        size = self.size >> 1
        lo, hi = self.min, self.max

        return list(
            filter(
                lambda sub: sub.valid,
                [
                    Box(
                        V(x=lo.x, y=lo.y, z=lo.z),
                        V(x=lo.x + size.x, y=lo.y + size.y, z=lo.z + size.z),
                    ),
                    Box(
                        V(x=lo.x + size.x, y=lo.y, z=lo.z),
                        V(x=hi.x, y=lo.y + size.y, z=lo.z + size.z),
                    ),
                    Box(
                        V(x=lo.x, y=lo.y + size.y, z=lo.z),
                        V(x=lo.x + size.x, y=hi.y, z=lo.z + size.z),
                    ),
                    Box(
                        V(x=lo.x, y=lo.y, z=lo.z + size.z),
                        V(x=lo.x + size.x, y=lo.y + size.y, z=hi.z),
                    ),
                    Box(
                        V(x=lo.x, y=lo.y + size.y, z=lo.z + size.z),
                        V(x=lo.x + size.x, y=hi.y, z=hi.z),
                    ),
                    Box(
                        V(x=lo.x + size.x, y=lo.y, z=lo.z + size.z),
                        V(x=hi.x, y=lo.y + size.y, z=hi.z),
                    ),
                    Box(
                        V(x=lo.x + size.x, y=lo.y + size.y, z=lo.z),
                        V(x=hi.x, y=hi.y, z=lo.z + size.z),
                    ),
                    Box(
                        V(x=lo.x + size.x, y=lo.y + size.y, z=lo.z + size.z),
                        V(x=hi.x, y=hi.y, z=hi.z),
                    ),
                ],
            )
        )


def bounding_box(bots: set[Bot]) -> Box:
    return Box(
        min=reduce(
            lambda carry, bot: V(
                x=min(carry.x, bot.v.x),
                y=min(carry.y, bot.v.y),
                z=min(carry.z, bot.v.z),
            ),
            bots,
            ORIGIN,
        ),
        max=reduce(
            lambda carry, bot: V(
                x=max(carry.x, bot.v.x),
                y=max(carry.y, bot.v.y),
                z=max(carry.z, bot.v.z),
            ),
            bots,
            ORIGIN,
        ),
    )


def octree_search(bots: set[Bot]) -> V:
    box = bounding_box(bots)

    queue = PriorityQueue()
    queue.put((-1 * len(bots), box.dist(ORIGIN), box, bots))

    while not queue.empty():
        _, _, box, bots = queue.get()

        if box.size == V(1, 1, 1):
            return box.min

        for subbox in box.subboxes:
            if subbots := set(
                filter(lambda bot: subbox.dist(bot.v) <= bot.range, bots)
            ):
                queue.put((-1 * len(subbots), subbox.dist(ORIGIN), subbox, subbots))


def main():
    bots = set()

    for line in sys.stdin:
        match = re.findall(r'-?\d+', line.strip())
        assert len(match) == 4

        bots.add(
            Bot(
                v=V(x=int(match[0]), y=int(match[1]), z=int(match[2])),
                range=int(match[3]),
            )
        )

    source = sorted(bots, key=lambda bot: bot.range, reverse=True)[0]
    print(sum(1 for bot in bots if source.v.dist(bot.v) <= source.range))
    print(octree_search(bots).dist(ORIGIN))


if __name__ == '__main__':
    main()
