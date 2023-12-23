import sys

grid_size = 700

trenches: list[list[str]] = [[' ' for x in range(grid_size)] for y in range(grid_size)]
x = y = grid_size // 2

trenches[y][x] = True

for line in sys.stdin:
    direction, length, color = line.split(' ')

    for i in range(int(length)):
        if direction == 'U':
            y -= 1
        if direction == 'D':
            y += 1
        if direction == 'R':
            x += 1
        if direction == 'L':
            x -= 1

        if not 0 < x < grid_size - 1 or not 0 < y < grid_size - 1:
            raise RuntimeError('Grid size inadequate')

        trenches[y][x] = '#'

trenches[0][0] = '.'
todo = [(0, 0)]

while len(todo):
    y, x = todo.pop()
    if trenches[y][x] == '#':
        continue

    if y < grid_size - 1 and trenches[y + 1][x] == ' ':
        trenches[y + 1][x] = '.'
        todo.append((y + 1, x))
    if y > 0 and trenches[y - 1][x] == ' ':
        trenches[y - 1][x] = '.'
        todo.append((y - 1, x))
    if x < grid_size - 1 and trenches[y][x + 1] == ' ':
        trenches[y][x + 1] = '.'
        todo.append((y, x + 1))
    if x > 0 and trenches[y][x - 1] == ' ':
        trenches[y][x - 1] = '.'
        todo.append((y, x - 1))

total_size = 0
for y, row in enumerate(trenches):
    for x, cell in enumerate(row):
        if cell in ['#', ' ']:
            total_size += 1

print(total_size)
# TODO Part 2 requires an algorithm to calculate surface instead of using a floodfill approach.
