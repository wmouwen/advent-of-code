import sys


class Vector:
    def __init__(self, y: int, x: int) -> None:
        self.y = y
        self.x = x

    def __eq__(self, other) -> bool:
        return self.y == other.y and self.x == other.x


def start_vector(grid: list[list[str]]) -> Vector:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 'S':
                return Vector(y=y, x=x)

    raise ValueError('No starting coordinates found')


def start_symbol(grid: list[list[str]], start: Vector) -> str:
    up = start.y > 0 and grid[start.y - 1][start.x] in ['|', 'F', '7']
    left = start.x > 0 and grid[start.y][start.x - 1] in ['-', 'L', 'F']
    down = start.y < len(grid) - 1 and grid[start.y + 1][start.x] in ['|', 'L', 'J']
    right = start.x < len(grid[start.y]) - 1 and grid[start.y][start.x + 1] in ['|', 'L', 'J']

    if up and left:
        return 'J'
    if up and right:
        return 'L'
    if down and left:
        return '7'
    if down and right:
        return 'F'
    if up and down:
        return '|'
    if left and right:
        return '-'

    raise RuntimeError


def start_direction(symbol: str) -> Vector:
    if symbol in ['-', 'F', 'L']:
        return Vector(y=0, x=-1)
    if symbol in ['|', '7']:
        return Vector(y=1, x=0)
    if symbol == 'J':
        return Vector(y=-1, x=0)

    raise ValueError('No loop in input')


def next_direction(cell: str, direction: Vector) -> Vector:
    if cell in ['|', '-']:
        return direction

    if cell == 'F':
        return Vector(y=1, x=0) if direction.x == -1 else Vector(y=0, x=1)
    if cell == 'L':
        return Vector(y=-1, x=0) if direction.x == -1 else Vector(y=0, x=1)
    if cell == 'J':
        return Vector(y=-1, x=0) if direction.x == 1 else Vector(y=0, x=-1)
    if cell == '7':
        return Vector(y=1, x=0) if direction.x == 1 else Vector(y=0, x=-1)

    raise ValueError('Invalid pipe symbol')


grid = [list(line.strip()) for line in sys.stdin]
start = start_vector(grid)
start_symbol = start_symbol(grid, start)

is_main_pipe = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
is_main_pipe[start.y][start.x] = True
direction = start_direction(start_symbol)
current = Vector(y=start.y, x=start.x)
length = 0

while True:
    current.y += direction.y
    current.x += direction.x

    is_main_pipe[current.y][current.x] = True
    length += 1

    if grid[current.y][current.x] == 'S':
        break

    direction = next_direction(grid[current.y][current.x], direction)

print(length >> 1)

grid[start.y][start.x] = start_symbol
enclosed = 0
for y in range(len(grid)):
    inner = False
    on_horizontal_stretch = None

    for x in range(len(grid[y])):
        if is_main_pipe[y][x]:
            if on_horizontal_stretch is not None:
                if grid[y][x] == '-':
                    continue
                elif grid[y][x] == '7':
                    if on_horizontal_stretch == 'L':
                        inner = not inner
                    on_horizontal_stretch = None
                elif grid[y][x] == 'J':
                    if on_horizontal_stretch == 'F':
                        inner = not inner
                    on_horizontal_stretch = None
            else:
                if grid[y][x] == 'L':
                    on_horizontal_stretch = 'L'
                elif grid[y][x] == 'F':
                    on_horizontal_stretch = 'F'
                elif grid[y][x] == '|':
                    inner = not inner
                else:
                    raise RuntimeError
        else:
            if inner:
                enclosed += 1

print(enclosed)
