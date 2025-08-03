import sys
from itertools import combinations
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int
    z: int

    def is_neighbor(self, other) -> bool:
        return (
            abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) == 1
        )


neighbor_directions = (
    Vector(-1, 0, 0),
    Vector(1, 0, 0),
    Vector(0, -1, 0),
    Vector(0, 1, 0),
    Vector(0, 0, -1),
    Vector(0, 0, 1),
)


def main():
    droplet = set(Vector(*map(int, line.strip().split(','))) for line in sys.stdin)

    print(
        6 * len(droplet)
        - sum(2 for a, b in combinations(droplet, r=2) if a.is_neighbor(b))
    )

    lower = Vector(
        x=min(cube.x for cube in droplet) - 1,
        y=min(cube.y for cube in droplet) - 1,
        z=min(cube.z for cube in droplet) - 1,
    )
    upper = Vector(
        x=max(cube.x for cube in droplet) + 1,
        y=max(cube.y for cube in droplet) + 1,
        z=max(cube.z for cube in droplet) + 1,
    )

    queue = Queue()
    queue.put(lower)
    visited = {lower}
    surface_area = 0

    while not queue.empty():
        cube = queue.get()

        for direction in neighbor_directions:
            neighbor = Vector(
                x=cube.x + direction.x, y=cube.y + direction.y, z=cube.z + direction.z
            )

            if not (
                lower.x <= neighbor.x <= upper.x
                and lower.y <= neighbor.y <= upper.y
                and lower.z <= neighbor.z <= upper.z
            ):
                continue

            if neighbor in droplet:
                surface_area += 1
                continue

            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.put(neighbor)

    print(surface_area)


if __name__ == '__main__':
    main()
