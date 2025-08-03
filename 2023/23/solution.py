import sys
from queue import Queue
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Node:
    def __init__(self, location: Vector):
        self.location = location
        self.edges: dict[Node, int] = {}


Graph = dict[Vector, Node]
allowed_moves = {
    '>': [Vector(x=1, y=0)],
    'v': [Vector(x=0, y=1)],
    '<': [Vector(x=-1, y=0)],
    '^': [Vector(x=0, y=-1)],
    '.': [Vector(x=1, y=0), Vector(x=0, y=1), Vector(x=-1, y=0), Vector(x=0, y=-1)],
}


def build_graph(grid, start: Vector, goal: Vector) -> Graph:
    graph = {start: Node(location=start), goal: Node(location=goal)}

    queue = Queue()
    queue.put((Vector(x=start.x, y=start.y + 1), start, graph[start], 1))

    while not queue.empty():
        current, previous, last_node, distance = queue.get()

        next_moves = []
        for move in allowed_moves[grid[current.y][current.x]]:
            if not 0 <= current.y + move.y < len(
                grid
            ) or not 0 <= current.x + move.x <= len(grid[current.y + move.y]):
                continue

            if previous.y == current.y + move.y and previous.x == current.x + move.x:
                continue

            if grid[current.y + move.y][current.x + move.x] != '#':
                next_moves.append(Vector(y=current.y + move.y, x=current.x + move.x))

        if len(next_moves) >= 2 or current == goal:
            if current in graph:
                next_moves = []
            else:
                graph[current] = Node(location=current)
                next_moves.append(previous)

            current_node = graph[current]
            last_node.edges[current_node] = distance
            last_node = current_node
            distance = 0

        for next_move in next_moves:
            queue.put((next_move, current, last_node, distance + 1))

    return graph


def find_longest_path(
    graph: Graph, goal: Vector, current: Vector, distance: int, visited: list[Node]
) -> int:
    if current == goal:
        return distance

    longest = 0
    visited.append(graph[current])

    for next_node, weight in graph[current].edges.items():
        if next_node not in visited:
            longest = max(
                longest,
                find_longest_path(
                    graph, goal, next_node.location, distance + weight, visited
                ),
            )

    visited.remove(graph[current])

    return longest


def main():
    grid = tuple(tuple(line.strip()) for line in sys.stdin)
    start = Vector(x=grid[0].index('.'), y=0)
    goal = Vector(x=grid[-1].index('.'), y=len(grid) - 1)

    graph = build_graph(grid, start, goal)
    # for location, node in graph.items():
    #     print(location)
    #     for other, weight in node.edges.items():
    #         print('->', other.location, weight)

    print(find_longest_path(graph, goal, start, 0, []))

    for node in graph.values():
        for other, weight in node.edges.items():
            other.edges[node] = weight

    previous_to_last_node, last_edge_weight = next(iter(graph[goal].edges.items()))
    print(
        find_longest_path(graph, previous_to_last_node.location, start, 0, [])
        + last_edge_weight
    )


if __name__ == '__main__':
    main()
