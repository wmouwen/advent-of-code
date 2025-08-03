import re
import sys
from collections import defaultdict
from functools import cache
from itertools import combinations
from math import prod

from enum import Enum
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Field(Enum):
    Calm = '.'
    Monster = 'O'
    Rough = '#'


Grid = list[str]


MONSTER = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']
MONSTER_OFFSETS = tuple(
    Vector(x=x, y=y)
    for y, line in enumerate(MONSTER)
    for x, char in enumerate(line)
    if char == Field.Rough.value
)


def grid_flip(grid: Grid) -> Grid:
    return [row[::-1] for row in grid]


def grid_rotate(grid: Grid, rotation: int) -> Grid:
    for _ in range(rotation % 4):
        grid = [[row[i] for row in reversed(grid)] for i in range(len(grid[0]))]
    return grid


class Tile:
    def __init__(self, key: int, grid: Grid):
        self.key = key
        self._grid = grid

    def __repr__(self):
        return f'Tile(key={self.key})'

    @cache
    def edges(self):
        flipped_grid = grid_flip(self._grid)

        return (
            # Normal: NESW
            ''.join(self._grid[0]),
            ''.join(self._grid[y][-1] for y in range(len(self._grid))),
            ''.join(self._grid[-1][::-1]),
            ''.join(self._grid[y][0] for y in range(len(self._grid)))[::-1],
            # Flipped: NESW
            ''.join(flipped_grid[0]),
            ''.join(flipped_grid[y][-1] for y in range(len(flipped_grid))),
            ''.join(flipped_grid[-1][::-1]),
            ''.join(flipped_grid[y][0] for y in range(len(flipped_grid)))[::-1],
        )

    @cache
    def edge(self, direction: Direction, rotation: int, flipped: bool):
        return self.edges()[((direction.value - rotation) % 4) + (4 if flipped else 0)]

    def image(self, rotation: int, flipped: bool):
        grid = grid_flip(self._grid) if flipped else self._grid
        grid = grid_rotate(grid, rotation)

        return [row[1:-1] for row in grid[1:-1]]


class LayoutPosition(NamedTuple):
    tile: Tile
    rotation: int
    flipped: bool


NeighborDict = defaultdict[Tile, list[Tile]]
TileLayout = list[list[LayoutPosition]]


def map_neighbors(tiles: list[Tile]) -> NeighborDict:
    neighbors = defaultdict(list)

    for a, b in combinations(tiles, 2):
        if any(edge in a.edges() for edge in b.edges()):
            neighbors[a].append(b)
            neighbors[b].append(a)

    return neighbors


def build_layout(neighbors: NeighborDict, corner: Tile) -> TileLayout:
    # Find initial corner rotation
    rotation = 0
    a, b = neighbors[corner]
    while rotation < 4:
        edge_east = corner.edge(Direction.East, rotation, False)
        edge_south = corner.edge(Direction.South, rotation, False)

        if (edge_east in a.edges() and edge_south in b.edges()) or (
            edge_east in b.edges() and edge_south in a.edges()
        ):
            break

        rotation += 1

    # Build the layout
    layout = [
        [current := LayoutPosition(tile=corner, rotation=rotation, flipped=False)]
    ]
    while True:
        while True:
            # Find next tile in the current row
            edge = current.tile.edge(Direction.East, current.rotation, current.flipped)
            neighbor = next(
                (
                    neighbor
                    for neighbor in neighbors[current.tile]
                    if edge in neighbor.edges()
                ),
                None,
            )
            if neighbor is None:
                break
            rotation, flipped = next(
                (rotation, flipped)
                for rotation in range(4)
                for flipped in (False, True)
                if neighbor.edge(Direction.West, rotation, flipped) == edge[::-1]
            )
            layout[-1].append(current := LayoutPosition(neighbor, rotation, flipped))

        # Find start of next row
        current = layout[-1][0]
        edge = current.tile.edge(Direction.South, current.rotation, current.flipped)
        neighbor = next(
            (
                neighbor
                for neighbor in neighbors[current.tile]
                if edge in neighbor.edges()
            ),
            None,
        )
        if neighbor is None:
            break
        rotation, flipped = next(
            (rotation, flipped)
            for rotation in range(4)
            for flipped in (False, True)
            if neighbor.edge(Direction.North, rotation, flipped) == edge[::-1]
        )

        layout.append([current := LayoutPosition(neighbor, rotation, flipped)])

    return layout


def build_image(layout: TileLayout) -> Grid:
    image = []

    for y, row in enumerate(layout):
        for tile, rotation, flipped in row:
            tile_image = tile.image(rotation, flipped)
            for i, line in enumerate(tile_image):
                if len(image) <= y * (len(tile_image)) + i:
                    image.append([])
                image[y * (len(tile_image)) + i] += line

    return image


def find_monsters(image: Grid) -> tuple[Vector, ...]:
    return tuple(
        Vector(x=x, y=y)
        for y in range(len(image) - len(MONSTER) + 1)
        for x in range(len(image[y]) - len(MONSTER[0]) + 1)
        if all(
            image[y + d.y][x + d.x] in (Field.Rough.value, Field.Monster.value)
            for d in MONSTER_OFFSETS
        )
    )


def mark_monsters(image: Grid, monsters: tuple[Vector, ...]) -> Grid:
    for monster in monsters:
        for d in MONSTER_OFFSETS:
            image[monster.y + d.y][monster.x + d.x] = Field.Monster.value

    return image


def read_input() -> list[Tile]:
    tiles, key, grid = [], None, []

    for line in sys.stdin:
        if match := re.match(r'^Tile (\d+):', line.strip()):
            if key is not None:
                tiles.append(Tile(key, grid))
                grid = []
            key = int(match.group(1))
        elif line.strip() != '':
            grid.append(list(line.strip()))

    if key is not None and len(grid):
        tiles.append(Tile(key, grid))

    return tiles


def main():
    tiles = read_input()

    neighbors = map_neighbors(tiles)
    assert len(neighbors) == len(tiles)
    assert all(2 <= len(neighbors[tile]) <= 4 for tile in neighbors)

    corners = tuple(filter(lambda tile: len(neighbors[tile]) == 2, neighbors.keys()))
    assert len(corners) == 4
    print(prod(tile.key for tile in corners))

    layout = build_layout(neighbors, corners[0])
    assert sum(len(row) for row in layout) == len(tiles)

    image = build_image(layout)
    print(*[''.join(row) for row in image], sep='\n')
    assert len(image) * len(image[0]) == (
        (len(tiles[0].edge(Direction.North, 0, False)) - 2) ** 2
    ) * (len(layout) * len(layout[0]))

    for _ in (False, True):
        image = grid_flip(image)
        for _ in range(4):
            image = grid_rotate(image, 1)
            monsters = find_monsters(image)
            image = mark_monsters(image, monsters)

    print(sum(row.count(Field.Rough.value) for row in image))


if __name__ == '__main__':
    main()
