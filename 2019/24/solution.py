import sys


def evolve(old: list[list[str]]):
    new = [['.' for x in range(len(old[y]))] for y in range(len(old))]

    for y in range(len(new)):
        for x in range(len(new[y])):
            neighbours = sum(
                1
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= y + dy < len(old) and 0 <= x + dx < len(old[y]) and old[y + dy][x + dx] == '#'
            )
            if (old[y][x] == '#' and neighbours == 1) or (old[y][x] == '.' and 1 <= neighbours <= 2):
                new[y][x] = '#'

    return new


def biodiversity(grid: list[list[str]]) -> int:
    return sum(pow(2, i) for i in range(25) if grid[i // 5][i % 5] == '#')


def main():
    grid = []
    for line in sys.stdin:
        if line.strip() == '':
            break
        grid.append(list(line.strip()))

    if len(grid) != 5 or any(len(row) != 5 for row in grid):
        raise Exception('Invalid input')

    seen = set()
    while (score := biodiversity(grid)) not in seen:
        seen.add(score)
        grid = evolve(grid)

    print(score)
    # print('=====', *[''.join(row) for row in grid], '=====', sep="\n")


if __name__ == '__main__':
    main()
