import sys
from queue import PriorityQueue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    @property
    def length(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x - other.x, y=self.y - other.y)


GRID_SIZE = Vector(x=70, y=70)
DIRECTIONS = [Vector(x=0, y=-1), Vector(x=1, y=0), Vector(x=0, y=1), Vector(x=-1, y=0)]


def shortest_path(
    walls: set[Vector], source: Vector, target: Vector
) -> list[Vector] | None:
    visited = set()

    queue: PriorityQueue[tuple[int, int, list[Vector]]] = PriorityQueue()
    queue.put((0, 0, [source]))

    while not queue.empty():
        _, _, path = queue.get()

        curr_pos = path[-1]
        if curr_pos in visited:
            continue

        visited.add(curr_pos)

        for move in DIRECTIONS:
            next_pos = curr_pos + move

            if next_pos == target:
                return path + [next_pos]

            if not (0 <= next_pos.x <= target.x and 0 <= next_pos.y <= target.y):
                continue

            if next_pos not in walls:
                queue.put(
                    (
                        len(path),
                        (GRID_SIZE - next_pos).length,
                        path + [next_pos],
                    )
                )

    return None


def main():
    walls: set[Vector] = set()

    for _ in range(1024):
        line = sys.stdin.readline().strip()
        if not line:
            break

        x, y = map(int, line.split(','))
        walls.add(Vector(x=x, y=y))

    path = shortest_path(walls, Vector(0, 0), GRID_SIZE)
    print(len(path) - 1)

    for line in sys.stdin:
        x, y = map(int, line.strip().split(','))
        walls.add(wall := Vector(x=x, y=y))

        if wall in path:
            path = shortest_path(walls, Vector(0, 0), GRID_SIZE)

            if path is None:
                print(line.strip())
                break


if __name__ == '__main__':
    main()
