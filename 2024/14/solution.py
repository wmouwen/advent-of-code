import re
import sys
from functools import reduce
from typing import NamedTuple

Vector = NamedTuple('Vector', {('x', int), ('y', int)})
Robot = NamedTuple('Robot', {('position', Vector), ('velocity', Vector)})


def positions_after_seconds(robots: list[Robot], seconds: int, space: Vector):
    return [
        Vector(
            x=(robot.position.x + robot.velocity.x * seconds) % space.x,
            y=(robot.position.y + robot.velocity.y * seconds) % space.y
        )
        for robot in robots
    ]


def safety_factor(positions: list[Vector], space: Vector):
    return reduce(lambda carry, item: carry * item, [
        len([position for position in positions if position.x < space.x // 2 and position.y < space.y // 2]),
        len([position for position in positions if position.x > space.x // 2 and position.y < space.y // 2]),
        len([position for position in positions if position.x < space.x // 2 and position.y > space.y // 2]),
        len([position for position in positions if position.x > space.x // 2 and position.y > space.y // 2]),
    ])


def main():
    space = Vector(x=101, y=103)

    robots = []
    for line in sys.stdin:
        if match := re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()):
            robots.append(Robot(
                position=Vector(x=int(match.group(1)), y=int(match.group(2))),
                velocity=Vector(x=int(match.group(3)), y=int(match.group(4)))
            ))

    print(safety_factor(positions_after_seconds(robots, 100, space), space))

    for t in range(space.x * space.y):
        positions = positions_after_seconds(robots, t, space)

        if len(positions) == len(set(positions)):
            # for y in range(space.y):
            #     print(''.join('*' if Vector(x=x, y=y) in positions else ' ' for x in range(space.x)))
            print(t)
            break


if __name__ == '__main__':
    main()
