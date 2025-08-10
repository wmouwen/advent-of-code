import sys
from dataclasses import dataclass
from queue import Queue, PriorityQueue
from string import ascii_uppercase

Maze = tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


class Portal:
    def __init__(self, key: str, position: Vector, outer: bool):
        self.label: str = key
        self.position: Vector = position
        self.outer: bool = outer
        self.paths: dict['Portal', int] = dict()

    def __repr__(self):
        return f'Portal({self.label}, {self.position})'

    def __lt__(self, other):
        return self.position.y < other.position.y


def find_label(maze: Maze, position: Vector) -> str | None:
    if (
        position.x >= 2
        and maze[position.y][position.x - 2] in ascii_uppercase
        and maze[position.y][position.x - 1] in ascii_uppercase
    ):
        return maze[position.y][position.x - 2] + maze[position.y][position.x - 1]
    if (
        position.x < len(maze[position.y]) - 2
        and maze[position.y][position.x + 1] in ascii_uppercase
        and maze[position.y][position.x + 2] in ascii_uppercase
    ):
        return maze[position.y][position.x + 1] + maze[position.y][position.x + 2]
    if (
        position.y >= 2
        and position.x < len(maze[position.y - 2])
        and position.x < len(maze[position.y - 1])
        and maze[position.y - 2][position.x] in ascii_uppercase
        and maze[position.y - 1][position.x] in ascii_uppercase
    ):
        return maze[position.y - 2][position.x] + maze[position.y - 1][position.x]
    if (
        position.y < len(maze) - 2
        and position.x < len(maze[position.y + 1])
        and position.x < len(maze[position.y + 2])
        and maze[position.y + 1][position.x] in ascii_uppercase
        and maze[position.y + 2][position.x] in ascii_uppercase
    ):
        return maze[position.y + 1][position.x] + maze[position.y + 2][position.x]
    return None


def is_outer(maze: Maze, position: Vector) -> bool:
    return (
        position.x < 3
        or position.x >= len(maze[position.y]) - 3
        or position.y < 3
        or position.y >= len(maze) - 3
    )


def floodfill_maze(passages: list[Vector], start: Vector) -> dict[Vector, int]:
    distances = {start: 0}

    queue: Queue[Vector] = Queue()
    queue.put(start)

    while not queue.empty():
        current = queue.get()

        for d in (Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1)):
            neighbor = Vector(current.x + d.x, current.y + d.y)
            if neighbor in passages and neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.put(neighbor)

    return distances


def parse_maze(maze: Maze):
    passages = []
    portals = []

    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char != '.':
                continue

            passages.append(position := Vector(x, y))

            if label := find_label(maze, position):
                portal = Portal(
                    key=label, position=position, outer=is_outer(maze, position)
                )
                portals.append(portal)

    for portal in portals:
        distances = floodfill_maze(passages, portal.position)
        for other in portals:
            if portal is other:
                continue
            if portal.label == other.label:
                portal.paths[other] = 1
            elif other.position in distances:
                portal.paths[other] = distances[other.position]

    return portals


def shortest_path_without_depth(start: Portal, end: Portal) -> int:
    visited = set()
    queue: PriorityQueue[tuple[int, Portal]] = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        distance, portal = queue.get()

        if portal is end:
            return distance

        if portal in visited:
            continue

        visited.add(portal)

        for neighbor, weight in portal.paths.items():
            if neighbor not in visited:
                queue.put((distance + weight, neighbor))

    raise Exception('no path found')


def shortest_path_with_depth(start: Portal, end: Portal) -> int:
    visited: set[tuple[Portal, int]] = set()
    queue: PriorityQueue[tuple[int, int, Portal]] = PriorityQueue()
    queue.put((0, 0, start))

    while not queue.empty():
        distance, depth, portal = queue.get()

        if (portal, depth) == (end, 0):
            return distance

        if (portal, depth) in visited:
            continue

        visited.add((portal, depth))

        for neighbor, weight in portal.paths.items():
            new_depth = depth + (
                (-1 if portal.outer and not neighbor.outer else 1)
                if portal.label == neighbor.label
                else 0
            )

            if new_depth >= 0 and (neighbor, new_depth) not in visited:
                queue.put((distance + weight, new_depth, neighbor))

    raise Exception('no path found')


def main():
    portals = parse_maze(tuple(tuple(line.rstrip('\n')) for line in sys.stdin))

    source = next(portal for portal in portals if portal.label == 'AA')
    target = next(portal for portal in portals if portal.label == 'ZZ')

    print(shortest_path_without_depth(source, target))
    print(shortest_path_with_depth(source, target))


if __name__ == '__main__':
    main()
