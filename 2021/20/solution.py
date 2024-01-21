import sys


def evolve(grid: list[list[str]], mapping: list[str]):
    grid = [['0', '0'] + row + ['0', '0'] for row in grid]
    grid = [
               ['0' for _ in grid[0]],
               ['0' for _ in grid[0]]
           ] + grid + [
               ['0' for _ in grid[-1]],
               ['0' for _ in grid[-1]]
           ]

    output = [['0' for _ in row] for row in grid]
    # TODO Fix algorithm to account for edges, and light/dark mapping (i.e. mapping[0] = '#')
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            inp = ''.join(grid[y - 1][x - 1:x + 2] + grid[y][x - 1:x + 2] + grid[y + 1][x - 1:x + 2])
            output[y][x] = mapping[int(inp, 2)]

    return output


def main():
    mapping = [{'.': '0', '#': '1'}[field] for field in sys.stdin.readline().strip()]

    # Ignore empty line
    sys.stdin.readline()

    grid = [[{'.': '0', '#': '1'}[field] for field in line.strip()] for line in sys.stdin]

    for _ in range(2):
        grid = evolve(grid, mapping)

    print(sum(1 for row in grid for field in row if field == '1'))


if __name__ == '__main__':
    main()
