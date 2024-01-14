import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


directions = {
    'E': Vector(x=1, y=0),
    'SE': Vector(x=1, y=1),
    'S': Vector(x=0, y=1),
    'SW': Vector(x=-1, y=1),
    'W': Vector(x=-1, y=0),
    'NW': Vector(x=-1, y=-1),
    'N': Vector(x=0, y=-1),
    'NE': Vector(x=1, y=-1),
}

proposed_directions = [
    ('N', ('N', 'NE', 'NW')),
    ('S', ('S', 'SE', 'SW')),
    ('W', ('W', 'NW', 'SW')),
    ('E', ('E', 'NE', 'SE')),
]


def main():
    elves = [
        Vector(x=x, y=y)
        for y, line in enumerate(sys.stdin.readlines())
        for x, field in enumerate(line.strip())
        if field == '#'
    ]

    for round in range(10):
        for elf in elves:
            pass  # TODO

    print(*elves, sep="\n")
    print(len(elves))


if __name__ == '__main__':
    main()
