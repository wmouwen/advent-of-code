import sys
from functools import cache
from queue import PriorityQueue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    @property
    def length(self) -> int:
        return abs(self.x) + abs(self.y)

    @cache
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y)

    @cache
    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x - other.x, y=self.y - other.y)


DIRECTIONS = (
    Vector(x=0, y=-1),
    Vector(x=1, y=0),
    Vector(x=0, y=1),
    Vector(x=-1, y=0),
)


def main():
    grid = [line.strip() for line in sys.stdin]

    nodes = set(
        Vector(x=x, y=y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell in 'SE.'
    )

    source = next(Vector(x=x, y=y) for x, y in nodes if grid[y][x] == 'S')
    target = next(Vector(x=x, y=y) for x, y in nodes if grid[y][x] == 'E')

    shortest_distance, shortest_paths = None, list()

    queue: PriorityQueue[tuple[int, int, tuple[Vector, ...], int]] = PriorityQueue()
    queue.put((0, 0, (source,), 1))
    queue.put((0, 1000, (source,), 0))

    visited = dict()

    while not queue.empty():
        _, distance, path, orientation = queue.get()

        if shortest_distance is not None and distance > shortest_distance:
            continue

        current_position = path[-1]

        visited_key = (path[-1], orientation)
        if visited_key in visited and visited[visited_key] < distance:
            continue
        visited[visited_key] = distance

        if current_position == target:
            if shortest_distance is None or distance < shortest_distance:
                shortest_distance = distance
                shortest_paths.clear()
            if distance == shortest_distance:
                shortest_paths.append(path)
            continue

        for turn in range(-1, 2):
            next_orientation = (orientation + turn) % len(DIRECTIONS)
            next_position = current_position + DIRECTIONS[next_orientation]

            if next_position in nodes:
                next_distance = distance + 1 + (abs(turn) * 1000)

                queue.put(
                    (
                        next_distance + (target - next_position).length * 1000,
                        next_distance,
                        path + (next_position,),
                        next_orientation,
                    )
                )

    print(shortest_distance)
    print(len(set(node for path in shortest_paths for node in path)))


if __name__ == '__main__':
    main()
