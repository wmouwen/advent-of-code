import re
import sys
from math import prod, sqrt


def map_input():
    tile_grids, key = {}, None
    for line in sys.stdin:
        if match := re.match(r'^Tile (\d+):', line.strip()):
            key = int(match.group(1))
            tile_grids[key] = []
        elif line.strip() != '':
            assert key is not None
            tile_grids[key].append(line.strip())
    return tile_grids


def map_tile_edges(tile_grids):
    def line_to_int(line: str) -> int:
        line = line.replace('.', '0').replace('#', '1')
        return int(line, 2)

    return {key: (
        (  # Normal: NESW, clockwise
            line_to_int(grid[0]),
            line_to_int(''.join(grid[y][-1] for y in range(len(grid)))),
            line_to_int(grid[-1][::-1]),
            line_to_int(''.join(grid[y][0] for y in range(len(grid)))[::-1]),
        ),
        (  # Reversed: NWSE, counter-clockwise
            line_to_int(grid[0][::-1]),
            line_to_int(''.join(grid[y][0] for y in range(len(grid)))),
            line_to_int(grid[-1]),
            line_to_int(''.join(grid[y][-1] for y in range(len(grid)))[::-1]),
        )
    ) for key, grid in tile_grids.items()}


def map_neighbours(tile_edges) -> dict:
    neighbours = dict()

    for key, tile in tile_edges.items():
        neighbours[key] = ([None] * 4, [None] * 4)

        for orientation, edges in enumerate(tile):
            for direction, edge in enumerate(edges):
                neighbour = [
                    (other, other_orientation, other_direction)
                    for other, other_edges in tile_edges.items()
                    for other_orientation, other_edges in enumerate(other_edges)
                    for other_direction, other_edge in enumerate(other_edges)
                    if other != key and other_edge == edge
                ]

                if neighbour:
                    neighbours[key][orientation][direction] = neighbour[0]

    return neighbours


def main():
    tile_grids = map_input()
    picture_size = int(sqrt(len(tile_grids)))
    tile_edges = map_tile_edges(tile_grids)
    neighbours = map_neighbours(tile_edges)

    # Assert puzzle input has a single possible layout
    num_edges_found = sum(1 for v in neighbours.values() for o in v for e in o if e is not None)
    num_edges_required = 2 * 4 + 3 * (picture_size - 2) * 4 + 4 * (picture_size - 2) * (picture_size - 2)
    assert num_edges_found == num_edges_required * 2

    corners = {k: v for k, v in neighbours.items() if len([1 for a in v for b in a if b is not None]) == 2 * 2}
    print(prod(corners.keys()))

    # print(*neighbours.items(), sep='\n')


if __name__ == '__main__':
    main()
