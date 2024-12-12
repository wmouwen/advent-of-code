import sys


class Region:
    def __init__(self, letter: str) -> None:
        self.cells: list[tuple[int, int]] = []
        self.letter = letter

    def area(self):
        return len(self.cells)

    def perimeter(self):
        return sum(
            1
            for x, y in self.cells
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if (x + dx, y + dy) not in self.cells
        )

    def sides(self):
        corners = 0

        for x, y in self.cells:
            for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
                cx, cy, cxy = (x + dx, y) in self.cells, (x, y + dy) in self.cells, (x + dx, y + dy) in self.cells
                corners += int((not cx and not cy) or (cx and cy and not cxy))

        return corners


def build_region(grid, x, y):
    region = Region(letter=grid[y][x])

    queue = {(x, y)}
    while len(queue) > 0:
        x, y = queue.pop()

        if (x, y) in region.cells:
            continue

        region.cells.append((x, y))

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = (x + dx, y + dy)

            if not (0 <= ny < len(grid) and 0 <= nx < len(grid[ny])):
                continue

            if (nx, ny) not in region.cells and grid[ny][nx] == region.letter:
                queue.add((nx, ny))

    return region


def main():
    grid = [list(line.strip()) for line in sys.stdin if line.strip() != ""]

    regions = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] is not None:
                regions.append(region := build_region(grid, x, y))
                for cx, cy in region.cells:
                    grid[cy][cx] = None

    # print(*grid, sep="\n")
    # for region in regions:
    #     print(region.letter, f'{region.area()} * {region.perimeter()} = {region.area() * region.perimeter()}')

    print(sum(region.area() * region.perimeter() for region in regions))
    print(sum(region.area() * region.sides() for region in regions))


if __name__ == '__main__':
    main()
