import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int
    z: int


class Brick:
    def __init__(self, top: Vector, bottom: Vector):
        self.top = top
        self.bottom = bottom


def main():
    for line in sys.stdin:
        print(line.strip())


if __name__ == '__main__':
    main()
