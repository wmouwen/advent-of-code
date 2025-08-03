import sys
from collections import defaultdict

dirs = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


def move_player(grid, old_positions):
    new_positions = set()

    for x, y in old_positions:
        new_positions.add((x, y))

        for dx, dy in dirs.values():
            if not (0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[y + dy])):
                continue

            if grid[y + dy][x + dx] == '#':
                continue

            new_positions.add((x + dx, y + dy))

    return new_positions


def move_blizzards(grid, old_blizzards):
    new_blizzards = defaultdict(list)

    for x, y in old_blizzards.keys():
        for dx, dy in old_blizzards[x, y]:
            nx, ny = x + dx, y + dy

            if ny == 0:
                ny = len(grid) - 2
            if ny == len(grid) - 1:
                ny = 1
            if nx == 0:
                nx = len(grid[ny]) - 2
            if nx == len(grid[ny]) - 1:
                nx = 1

            new_blizzards[(nx, ny)].append((dx, dy))

    return new_blizzards


def wipe_player(player, blizzards):
    for x, y in blizzards.keys():
        if (x, y) in player:
            player.remove((x, y))

    return player


def main():
    grid = [list(line.strip()) for line in sys.stdin if line.strip() != '']

    start = (grid[0].index('.'), 0)
    finish = (grid[-1].index('.'), len(grid) - 1)

    blizzards = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in ['>', '<', '^', 'v']:
                blizzards[(x, y)].append(dirs[cell])

    minutes = 0

    player = {start}
    while finish not in player:
        minutes += 1
        player = move_player(grid, player)
        blizzards = move_blizzards(grid, blizzards)
        player = wipe_player(player, blizzards)

    print(minutes)

    player = {finish}
    while start not in player:
        minutes += 1
        player = move_player(grid, player)
        blizzards = move_blizzards(grid, blizzards)
        player = wipe_player(player, blizzards)

    player = {start}
    while finish not in player:
        minutes += 1
        player = move_player(grid, player)
        blizzards = move_blizzards(grid, blizzards)
        player = wipe_player(player, blizzards)

    print(minutes)


if __name__ == '__main__':
    main()
