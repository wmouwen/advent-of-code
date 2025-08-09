import sys
from functools import cache
from queue import Queue, PriorityQueue
from string import ascii_lowercase, ascii_uppercase
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


Maze = tuple[tuple[str, ...], ...]
DIRECTIONS = (
    Vector(x=0, y=-1),
    Vector(x=1, y=0),
    Vector(x=0, y=1),
    Vector(x=-1, y=0),
)


class QueueItem(NamedTuple):
    priority_key_count: int
    priority_distance: int
    positions: frozenset[Vector]
    keys: frozenset[str]
    distance: int


def locate(char: str, maze: Maze) -> frozenset[Vector]:
    return frozenset(
        Vector(x=x, y=y)
        for y, row in enumerate(maze)
        for x, cell in enumerate(row)
        if cell == char
    )


def min_dists(maze: Maze, start: Vector) -> dict[str, tuple[int, frozenset]]:
    reachable_keys = dict()
    visited = {start}
    queue = Queue()
    queue.put((start, 0, frozenset()))

    while not queue.empty():
        current, distance, doors = queue.get()
        for d in DIRECTIONS:
            candidate = Vector(x=current.x + d.x, y=current.y + d.y)
            if candidate in visited:
                continue

            char = maze[candidate.y][candidate.x]
            if char == '#':
                continue

            if char in ascii_uppercase:
                doors = frozenset(doors | {char.lower()})

            if char in ascii_lowercase:
                reachable_keys[char] = (distance + 1, doors)

            visited.add(candidate)
            queue.put((candidate, distance + 1, doors))

    return reachable_keys


@cache
def reachable(maze: Maze, keys: frozenset[str], start: Vector) -> dict[str, int]:
    reachable_keys = dict()
    distances = {start: 0}
    queue = Queue()
    queue.put(start)

    while not queue.empty():
        current = queue.get()
        distance = distances[current] + 1

        for d in DIRECTIONS:
            candidate = Vector(x=current.x + d.x, y=current.y + d.y)
            if candidate in distances:
                continue

            char = maze[candidate.y][candidate.x]
            if char == '#' or (char in ascii_uppercase and char.lower() not in keys):
                continue

            if char in ascii_lowercase:
                reachable_keys[char] = distance

            distances[candidate] = distance
            queue.put(candidate)

    return reachable_keys


def find_shortest_path(maze: Maze) -> int:
    entrances = locate('@', maze)

    key_locations: dict[str, Vector] = {
        key: next(iter(locations))
        for key in ascii_lowercase
        if len(locations := locate(key, maze)) > 0
    }
    key_count = len(key_locations)
    assert key_count > 0

    min_dist = min(
        min(
            min(d[0] for d in min_dists(maze, key_locations[key]).values())
            for key in key_locations
        ),
        min(
            min(d[0] for d in min_dists(maze, entrance).values())
            for entrance in entrances
        ),
    )

    best = len(maze) * len(maze[0]) * key_count

    queue = PriorityQueue()
    queue.put(
        QueueItem(
            priority_key_count=0,
            priority_distance=0,
            positions=entrances,
            distance=0,
            keys=frozenset(),
        )
    )

    while not queue.empty():
        item: QueueItem = queue.get()
        if item.distance + min_dist * (key_count - (len(item.keys) + 1)) >= best:
            break

        targets = []
        for start in item.positions:
            for key, distance in reachable(
                maze=maze, keys=frozenset(sorted(item.keys)), start=start
            ).items():
                targets.append((start, key, distance))

        for start, key, distance in targets:
            if key in item.keys:
                continue

            new_distance = item.distance + distance
            if new_distance >= best:
                continue

            new_keys = frozenset(sorted(item.keys | {key}))
            new_key_count = len(new_keys)
            if (new_distance + min_dist * (key_count - new_key_count)) >= best:
                continue

            if new_key_count == key_count:
                best = new_distance
                continue

            queue.put(
                QueueItem(
                    priority_key_count=-new_key_count,
                    priority_distance=-new_distance,
                    positions=item.positions.difference({start}).union(
                        {key_locations[key]}
                    ),
                    distance=new_distance,
                    keys=new_keys,
                )
            )

    return best


def main():
    maze = tuple(tuple(line.strip()) for line in sys.stdin)
    print(find_shortest_path(maze))

    entrance = next(iter(locate('@', maze)))
    maze = list(list(row) for row in maze)
    maze[entrance.y - 1][entrance.x - 1] = '@'
    maze[entrance.y - 1][entrance.x] = '#'
    maze[entrance.y - 1][entrance.x + 1] = '@'
    maze[entrance.y][entrance.x - 1] = '#'
    maze[entrance.y][entrance.x] = '#'
    maze[entrance.y][entrance.x + 1] = '#'
    maze[entrance.y + 1][entrance.x - 1] = '@'
    maze[entrance.y + 1][entrance.x] = '#'
    maze[entrance.y + 1][entrance.x + 1] = '@'
    maze = tuple(tuple(row) for row in maze)

    print(find_shortest_path(maze))


if __name__ == '__main__':
    main()
