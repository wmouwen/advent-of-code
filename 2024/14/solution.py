import re
import sys
from functools import reduce
from statistics import variance
from typing import NamedTuple

Vector = NamedTuple('Vector', {('x', int), ('y', int)})
Robot = NamedTuple('Robot', {('position', Vector), ('velocity', Vector)})


def positions_after_seconds(robots: list[Robot], seconds: int, space: Vector):
    return [
        Vector(
            x=(robot.position.x + robot.velocity.x * seconds) % space.x,
            y=(robot.position.y + robot.velocity.y * seconds) % space.y,
        )
        for robot in robots
    ]


def safety_factor(positions: list[Vector], space: Vector):
    return reduce(
        lambda carry, item: carry * item,
        [
            len(
                [
                    position
                    for position in positions
                    if position.x < space.x // 2 and position.y < space.y // 2
                ]
            ),
            len(
                [
                    position
                    for position in positions
                    if position.x > space.x // 2 and position.y < space.y // 2
                ]
            ),
            len(
                [
                    position
                    for position in positions
                    if position.x < space.x // 2 and position.y > space.y // 2
                ]
            ),
            len(
                [
                    position
                    for position in positions
                    if position.x > space.x // 2 and position.y > space.y // 2
                ]
            ),
        ],
    )


def main():
    space = Vector(x=101, y=103)

    robots = []
    for line in sys.stdin:
        if match := re.match(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()):
            robots.append(
                Robot(
                    position=Vector(x=int(match.group(1)), y=int(match.group(2))),
                    velocity=Vector(x=int(match.group(3)), y=int(match.group(4))),
                )
            )

    print(safety_factor(positions_after_seconds(robots, 100, space), space))

    best_x, best_y = 0, 0
    best_variances = {'x': len(robots) * space.x, 'y': len(robots) * space.y}
    for t in range(max(space.x, space.y)):
        positions = positions_after_seconds(robots, t, space)

        variance_x = variance(position.x for position in positions)
        if t < space.x and variance_x < best_variances['x']:
            best_variances['x'] = variance_x
            best_x = t

        variance_y = variance(position.y for position in positions)
        if t < space.y and variance_y < best_variances['y']:
            best_variances['y'] = variance_y
            best_y = t

    # t = best_x % space.x = best_y % space.y
    print(
        best_x
        + ((pow(space.x, -1, mod=space.y) * (best_y - best_x)) % space.y) * space.x
    )


if __name__ == '__main__':
    main()
