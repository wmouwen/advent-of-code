import sys
from collections import defaultdict
from dataclasses import dataclass
from queue import Queue, PriorityQueue
from string import ascii_lowercase, ascii_uppercase


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x if self.y == other.y else self.y < other.y


Maze = list[list[str]]
ObjectDict = dict[str, Vector]
DistanceMatrix = dict[Vector, dict[Vector, int]]

DIRECTIONS = (
    Vector(x=0, y=-1),
    Vector(x=1, y=0),
    Vector(x=0, y=1),
    Vector(x=-1, y=0),
)


def floodfill(maze: Maze, start: Vector) -> dict[Vector, int]:
    distances = {start: 0}

    queue: Queue[Vector] = Queue()
    queue.put(start)

    while not queue.empty():
        current = queue.get()

        for d in DIRECTIONS:
            neighbor = Vector(current.x + d.x, current.y + d.y)

            if maze[neighbor.y][neighbor.x] == '#' or neighbor in distances:
                continue

            distances[neighbor] = distances[current] + 1

            if maze[neighbor.y][neighbor.x] == '.':
                queue.put(neighbor)

    return distances


def distance_matrix(
    maze: Maze, robots: list[Vector], keys: ObjectDict, doors: ObjectDict
) -> DistanceMatrix:
    targets = list(keys.values()) + list(doors.values())
    sources = robots + targets
    distances = defaultdict(dict)

    for source in sources:
        distances_from_object = floodfill(maze, source)

        for target in targets:
            if source == target:
                continue

            if target not in distances_from_object:
                continue

            distances[source][target] = distances_from_object[target]

    return dict(distances)


def shortest_multipath(
    maze: Maze, robots: list[Vector], keys: ObjectDict, doors: ObjectDict
) -> int | None:
    distances = distance_matrix(maze, robots, keys, doors)

    queue: PriorityQueue[tuple[int, int, set[str], set[Vector]]] = PriorityQueue()
    queue.put((0, 0, set(), set(robots)))

    best = None
    min_weight = min(min(distances[source].values()) for source in keys.values())
    visited = dict()

    while not queue.empty():
        _, distance, collected_keys, robots = queue.get()

        # Prune unrealistic remainder weights
        if (
            best is not None
            and distance + min_weight * (len(keys) - len(collected_keys)) > best
        ):
            continue

        # Prune visited states
        visited_key = (''.join(sorted(collected_keys)), tuple(sorted(robots)))
        if visited_key in visited and visited[visited_key] <= distance:
            continue

        visited[visited_key] = distance

        # Break loop if all keys have been collected
        if len(collected_keys) == len(keys):
            best = distance
            continue

        # Attempt to move each robot to all its reachable locations
        for robot in robots:
            for key in keys:
                if keys[key] not in distances[robot]:
                    continue

                new_keys = collected_keys | {key}
                queue.put(
                    (
                        -len(new_keys),
                        distance + distances[robot][keys[key]],
                        new_keys,
                        (robots - {robot}) | {keys[key]},
                    )
                )

            for door in doors:
                if doors[door] not in distances[robot]:
                    continue

                if door.lower() not in collected_keys:
                    continue

                queue.put(
                    (
                        -len(collected_keys),
                        distance + distances[robot][doors[door]],
                        collected_keys,
                        (robots - {robot}) | {doors[door]},
                    )
                )

    return best


def main():
    maze = list(list(line.strip()) for line in sys.stdin)

    robots, keys, doors = [], dict(), dict()
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '@':
                robots.append(Vector(x=x, y=y))
                maze[y][x] = '.'
            elif cell in ascii_lowercase:
                keys.update({cell: Vector(x=x, y=y)})
            elif cell in ascii_uppercase:
                doors.update({cell: Vector(x=x, y=y)})

    print(shortest_multipath(maze, robots, keys, doors))

    robot = robots[0]
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            maze[robot.y + dy][robot.x + dx] = '#'

    robots = [
        Vector(x=robot.x - 1, y=robot.y - 1),
        Vector(x=robot.x - 1, y=robot.y + 1),
        Vector(x=robot.x + 1, y=robot.y - 1),
        Vector(x=robot.x + 1, y=robot.y + 1),
    ]
    for robot in robots:
        maze[robot.y][robot.x] = '.'

    print(shortest_multipath(maze, robots, keys, doors))


if __name__ == '__main__':
    main()
