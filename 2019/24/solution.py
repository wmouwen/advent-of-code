import sys
from collections import defaultdict
from functools import cache
from typing import NamedTuple, Self


class V(NamedTuple):
    x: int
    y: int
    depth: int

    def __add__(self, other: Self):
        return V(x=self.x + other.x, y=self.y + other.y, depth=self.depth + other.depth)


def evolve_plain(bugs: set[V]) -> set[V]:
    bug_neighbors, empty_neighbors = defaultdict(int), defaultdict(int)

    for bug in bugs:
        for direction in {V(0, -1, 0), V(1, 0, 0), V(0, 1, 0), V(-1, 0, 0)}:
            if (neighbor := bug + direction) in bugs:
                bug_neighbors[bug] += 1
            else:
                empty_neighbors[neighbor] += 1

    return ({
        cell for cell, active_neighbors in bug_neighbors.items()
        if 0 <= cell.x < 5 and 0 <= cell.y < 5 and active_neighbors == 1
    }).union({
        cell for cell, active_neighbors in empty_neighbors.items()
        if 0 <= cell.x < 5 and 0 <= cell.y < 5 and 1 <= active_neighbors <= 2
    })


def find_repetition_rating(bugs: set[V]) -> int:
    seen = set()

    while True:
        rating = sum(1 << (5 * bug.y + bug.x) for bug in bugs)
        if rating in seen:
            return rating

        seen.add(rating)
        bugs = evolve_plain(bugs)


@cache
def neighbors_layered(bug) -> set[V]:
    neighbors = set()

    # Up
    if bug.y == 0:
        neighbors.add(V(2, 1, bug.depth - 1))
    elif bug.y == 3 and bug.x == 2:
        neighbors.update({V(x, 4, bug.depth + 1) for x in range(5)})
    else:
        neighbors.add(V(bug.x, bug.y - 1, bug.depth))

    # Right
    if bug.x == 4:
        neighbors.add(V(3, 2, bug.depth - 1))
    elif bug.x == 1 and bug.y == 2:
        neighbors.update({V(0, y, bug.depth + 1) for y in range(5)})
    else:
        neighbors.add(V(bug.x + 1, bug.y, bug.depth))

    # Down
    if bug.y == 4:
        neighbors.add(V(2, 3, bug.depth - 1))
    elif bug.y == 1 and bug.x == 2:
        neighbors.update({V(x, 0, bug.depth + 1) for x in range(5)})
    else:
        neighbors.add(V(bug.x, bug.y + 1, bug.depth))

    # Left
    if bug.x == 0:
        neighbors.add(V(1, 2, bug.depth - 1))
    elif bug.x == 3 and bug.y == 2:
        neighbors.update({V(4, y, bug.depth + 1) for y in range(5)})
    else:
        neighbors.add(V(bug.x - 1, bug.y, bug.depth))

    return neighbors


def evolve_layered(bugs: set[V]) -> set[V]:
    bugs = set(filter(lambda bug: bug.x != 2 or bug.y != 2, bugs))
    bug_neighbors, empty_neighbors = defaultdict(int), defaultdict(int)

    for bug in bugs:
        for neighbor in neighbors_layered(bug):
            if neighbor in bugs:
                bug_neighbors[bug] += 1
            else:
                empty_neighbors[neighbor] += 1

    return ({
        cell for cell, active_neighbors in bug_neighbors.items()
        if 0 <= cell.x < 5 and 0 <= cell.y < 5 and active_neighbors == 1
    }).union({
        cell for cell, active_neighbors in empty_neighbors.items()
        if 0 <= cell.x < 5 and 0 <= cell.y < 5 and 1 <= active_neighbors <= 2
    })


def main():
    bugs = {
        V(x, y, depth=0)
        for y, row in enumerate(sys.stdin.readlines())
        for x, cell in enumerate(row)
        if cell == '#'
    }

    print(find_repetition_rating(bugs))

    for _ in range(200):
        bugs = evolve_layered(bugs)

    print(len(bugs))


if __name__ == '__main__':
    main()
