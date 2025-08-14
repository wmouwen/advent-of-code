import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)


DIRECTIONS = {
    '^': Vector(x=0, y=1),
    '>': Vector(x=1, y=0),
    'v': Vector(x=0, y=-1),
    '<': Vector(x=-1, y=0),
}


def house_visits(moves: str, token_count: int) -> int:
    tokens = tuple(Vector(0, 0) for _ in range(token_count))
    visited = set(tokens)

    for i, move in enumerate(moves):
        tokens[i % len(tokens)] += DIRECTIONS[move]
        visited.add(tokens[i % len(tokens)])

    return len(visited)


def main():
    moves = sys.stdin.readline().strip()

    print(house_visits(moves, 1))
    print(house_visits(moves, 2))


if __name__ == '__main__':
    main()
