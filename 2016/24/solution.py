import sys
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


directions = (Vector(x=1, y=0), Vector(x=0, y=1), Vector(x=-1, y=0), Vector(x=0, y=-1))


def floodfill(grid: list[list[str]], start: Vector) -> list[list[int]]:
    distances = [[sys.maxsize for _ in row] for row in grid]
    distances[start.y][start.x] = 0

    queue = Queue()
    queue.put(start)

    while not queue.empty():
        current = queue.get()

        for direction in directions:
            location = Vector(x=current.x + direction.x, y=current.y + direction.y)

            if grid[location.y][location.x] == '#':
                continue

            if distances[location.y][location.x] != sys.maxsize:
                continue

            distances[location.y][location.x] = distances[current.y][current.x] + 1
            queue.put(location)

    return distances


def hamiltonian_path(
    edges: dict[str, dict[str, int]],
    current: str,
    visited: set[str],
    final_node: str | None,
    travelled: int = 0,
) -> int:
    if len(visited) == len(edges.keys()):
        return travelled + (
            edges[current][final_node] if isinstance(final_node, str) else 0
        )

    best = sys.maxsize

    for node, distance in edges[current].items():
        if node in visited:
            continue

        best = min(
            best,
            hamiltonian_path(
                edges, node, visited | {node}, final_node, travelled + distance
            ),
        )

    return best


def main():
    grid: list[list[str]] = list(list(line.strip()) for line in sys.stdin)

    nodes = {
        field: Vector(x=x, y=y)
        for y, row in enumerate(grid)
        for x, field in enumerate(row)
        if field.isnumeric()
    }
    edges = {}

    for current in nodes:
        distances = floodfill(grid=grid, start=nodes[current])
        edges[current] = {
            other: distances[nodes[other].y][nodes[other].x]
            for other in nodes
            if current != other
        }

    print(hamiltonian_path(edges, '0', {'0'}, None))
    print(hamiltonian_path(edges, '0', {'0'}, '0'))


if __name__ == '__main__':
    main()
