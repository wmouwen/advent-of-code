import sys
from functools import cache
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    @cache
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)


def accessible_rolls(rolls_of_paper: set[Vector]) -> set[Vector]:
    neighbors = list(
        Vector(x=dx, y=dy)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
        if dx != 0 or dy != 0
    )

    return set(
        roll
        for roll in rolls_of_paper
        if sum(1 for d in neighbors if roll + d in rolls_of_paper) < 4
    )


def main():
    rolls_of_paper = {
        Vector(x=x, y=y)
        for y, line in enumerate(sys.stdin)
        for x, cell in enumerate(line.strip())
        if cell == '@'
    }
    initial_count = len(rolls_of_paper)

    for i in range(len(rolls_of_paper)):
        accessible = accessible_rolls(rolls_of_paper)

        if i == 0:
            print(len(accessible))

        if not accessible:
            break

        rolls_of_paper = rolls_of_paper - accessible

    print(initial_count - len(rolls_of_paper))


if __name__ == '__main__':
    main()
