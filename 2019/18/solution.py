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
    position: Vector
    keys: frozenset[str]
    distance: int


def locate(char: str, maze: Maze) -> Vector | None:
    return next(
        (
            Vector(x=x, y=y)
            for y, row in enumerate(maze)
            for x, cell in enumerate(row)
            if cell == char
        ),
        None,
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


def main():
    maze = tuple(tuple(line.strip()) for line in sys.stdin)
    entrance = locate('@', maze)
    assert entrance is not None

    key_locations: dict[str, Vector] = {
        key: location
        for key in ascii_lowercase
        if (location := locate(key, maze)) is not None
    }
    key_count = len(key_locations)
    assert key_count > 0

    min_dist = min(
        min(
            min(d[0] for d in min_dists(maze, key_locations[key]).values())
            for key in key_locations
        ),
        min(d[0] for d in min_dists(maze, entrance).values()),
    )

    intermediate_best = {key: dict() for key in key_locations}
    best = len(maze) * len(maze[0]) * key_count

    queue = PriorityQueue()
    queue.put(
        QueueItem(
            priority_key_count=0,
            priority_distance=0,
            position=entrance,
            distance=0,
            keys=frozenset(),
        )
    )

    while not queue.empty():
        item = queue.get()
        if item.distance + min_dist * (key_count - (len(item.keys) + 1)) >= best:
            break

        targets = reachable(
            maze=maze, keys=frozenset(sorted(item.keys)), start=item.position
        ).items()
        for key, distance in targets:
            if key in item.keys:
                continue

            new_distance = item.distance + distance
            if new_distance >= best:
                continue

            new_keys = frozenset(sorted(item.keys | {key}))
            if (
                new_keys in intermediate_best[key]
                and new_distance >= intermediate_best[key][new_keys]
            ):
                continue

            new_key_count = len(new_keys)
            if (new_distance + min_dist * (key_count - new_key_count)) >= best:
                continue

            intermediate_best[key][new_keys] = new_distance
            if new_key_count == key_count:
                best = new_distance
                continue

            queue.put(
                QueueItem(
                    priority_key_count=-new_key_count,
                    priority_distance=-new_distance,
                    position=key_locations[key],
                    distance=new_distance,
                    keys=new_keys,
                )
            )

    print(best)


if __name__ == '__main__':
    main()
