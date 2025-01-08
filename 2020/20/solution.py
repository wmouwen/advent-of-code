import re
import sys
from math import prod


def line_to_int(line: str) -> int:
    line = line.replace('.', '0').replace('#', '1')
    return int(line, 2)


def map_neighbours(tiles) -> dict:
    neighbours = {
        key: [other for other in tiles.keys() if key != other and any(
            side == other_side
            for orientation in tiles[key]
            for side in orientation
            for other_orientation in tiles[other]
            for other_side in other_orientation
        )]
        for key in tiles.keys()
    }

    print([
        key for key, n in neighbours.items() if len(n) == 2
    ])
    print(prod([
        key for key, n in neighbours.items() if len(n) == 2
    ]))

    # print(*neighbours.items(), sep="\n")
    exit(0)
    return dict()


def create_picture(tiles, neighbours=None, placed=None, picture=None):
    if picture is None:
        picture = []
    elif len(picture) == len(tiles):
        return picture

    if neighbours is None:
        neighbours = map_neighbours(tiles)
    if placed is None:
        placed = set()

    return None


def main():
    tile_grids, key = {}, None

    for line in sys.stdin:
        if match := re.match(r'^Tile (\d+):', line.strip()):
            key = int(match.group(1))
            tile_grids[key] = []
        elif line.strip() != '':
            assert key is not None
            tile_grids[key].append(line.strip())

    tiles = {key: (
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

    picture = create_picture(tiles)
    print(picture)


if __name__ == '__main__':
    main()
