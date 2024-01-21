import json
import sys
from typing import Self


class Snailfish:
    def __init__(self, left: Self | int, right: Self | int):
        self.left: Self | int = left
        self.right: Self | int = right

    @classmethod
    def from_list(cls, raw: list):
        left, right = raw

        return cls(
            left=left if isinstance(left, int) else cls.from_list(left),
            right=right if isinstance(right, int) else cls.from_list(right)
        )

    def reduce(self, depth: int = 0) -> None:
        exploded = self._explode(depth)

        if not isinstance(self.left, int):
            self.left.reduce(depth=depth + 1)
            return

        if not isinstance(self.right, int):
            self.right.reduce(depth=depth + 1)
            return

    def _explode(self, depth: int):
        if depth == 3:
            exploded_left = None
            exploded_right = None

            if not isinstance(self.left, int):
                exploded_left = self.left
                self.left = 0

                if isinstance(self.right, int):
                    self.right += exploded_left.right
                else:
                    self.right._add_left(exploded_left.right)

            if not isinstance(self.right, int):
                exploded_right = self.right
                self.right = 0

                if isinstance(self.left, int):
                    self.left += exploded_right.left
                else:
                    self.left._add_right(exploded_right.left)

            # TODO

            return exploded_left, exploded_right

    def _add_left(self, value: int):
        if isinstance(self.left, int):
            self.left += value
        else:
            self.left._add_left(value)

    def _add_right(self, value: int):
        if isinstance(self.right, int):
            self.right += value
        else:
            self.right._add_right(value)

    @property
    def magnitude(self) -> int:
        return sum([
            3 * (self.left if isinstance(self.left, int) else self.left.magnitude),
            2 * (self.right if isinstance(self.right, int) else self.right.magnitude)
        ])

    def __add__(self, other: Self) -> Self:
        return Snailfish(left=self, right=other)

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'


def main():
    snailfishes = [
        Snailfish.from_list(json.loads(line.strip()))
        for line in sys.stdin
    ]

    snailfish = snailfishes[0]

    for other in snailfishes[1:]:
        snailfish += other
        snailfish.reduce()

    print(snailfish)
    print(snailfish.magnitude)


if __name__ == '__main__':
    main()
