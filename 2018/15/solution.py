import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Unit:
    def __init__(self, pos: Vector, attack_power: int):
        self.pos = pos
        self.attack_power = attack_power
        self.hp = 200

    def __repr__(self):
        return "{} [{}, {}]".format(type(self).__name__, self.pos, self.hp)


class Elf(Unit):
    pass


class Goblin(Unit):
    pass


def play(grid, attack_power):
    walls = [
        [True if cell == '#' else False for cell in row]
        for row in grid
    ]

    units = [
                Elf(Vector(x=x, y=y), attack_power=attack_power)
                for y, row in enumerate(grid)
                for x, cell in enumerate(row)
                if cell == 'E'
            ] + [
                Goblin(Vector(x=x, y=y), attack_power=3)
                for y, row in enumerate(grid)
                for x, cell in enumerate(row)
                if cell == 'G'
            ]

    combat_rounds = 0
    while len(units) and not all(isinstance(unit, type(units[0])) for unit in units):
        combat_rounds += 1

        playing_order = sorted(units, key=lambda unit: unit.pos.y * len(grid[0]) + unit.pos.x)
        for unit in playing_order:
            if unit not in units:
                continue

            all_targets = [target for target in units if not isinstance(target, type(unit))]
            neighboring_targets = [
                target
                for target in all_targets
                if abs(unit.pos.x - target.pos.x) + abs(unit.pos.y - target.pos.y) == 1
            ]

            if not len(neighboring_targets):
                target_squares = [
                    Vector(x=target.pos.x + move.x, y=target.pos.y + move.y)
                    for target in all_targets
                    for move in [Vector(x=0, y=-1), Vector(x=-1, y=0), Vector(x=1, y=0), Vector(x=0, y=1)]
                    if not walls[target.pos.y + move.y][target.pos.x + move.x] and not any([
                        target.pos.x + move.x == other.pos.x
                        and target.pos.y + move.y == other.pos.y
                        for other in units
                    ])
                ]

                visited: list[list[tuple | None]] = [[None for _ in row] for row in grid]
                visited[unit.pos.y][unit.pos.x] = (0, None)
                queue = [unit.pos]
                while len(queue):
                    current = queue.pop(0)
                    for move in [Vector(x=0, y=-1), Vector(x=-1, y=0), Vector(x=1, y=0), Vector(x=0, y=1)]:
                        if visited[current.y + move.y][current.x + move.x]:
                            continue

                        if walls[current.y + move.y][current.x + move.x]:
                            continue

                        if (any(
                                current.x + move.x == other.pos.x and current.y + move.y == other.pos.y
                                for other in units
                        )):
                            continue

                        visited[current.y + move.y][current.x + move.x] = (
                            visited[current.y][current.x][0] + 1,
                            current
                        )
                        queue.append(Vector(x=current.x + move.x, y=current.y + move.y))

                reachable_squares = []
                for target_square in target_squares:
                    if visited[target_square.y][target_square.x] is not None:
                        reachable_squares.append(target_square)

                if len(reachable_squares):
                    reachable_squares.sort(key=lambda square: visited[square.y][square.x][0])
                    nearest_squares = [
                        square
                        for square in reachable_squares
                        if visited[square.y][square.x][0] == visited[reachable_squares[0].y][reachable_squares[0].x][0]
                    ]

                    nearest_squares.sort(key=lambda square: square.y * len(grid[0]) + square.x)

                    chosen_square = nearest_squares[0]
                    while visited[chosen_square.y][chosen_square.x][1] != unit.pos:
                        chosen_square = visited[chosen_square.y][chosen_square.x][1]

                    unit.pos = chosen_square

            neighboring_targets = [
                target
                for target in all_targets
                if abs(unit.pos.x - target.pos.x) + abs(unit.pos.y - target.pos.y) == 1
            ]

            if len(neighboring_targets):
                if len(neighboring_targets) > 1:
                    neighboring_targets.sort(key=lambda target: target.hp)
                    neighboring_targets = [
                        target
                        for target in neighboring_targets
                        if target.hp == neighboring_targets[0].hp
                    ]

                neighboring_targets.sort(key=lambda target: target.pos.y * len(grid[0]) + target.pos.x)
                target = neighboring_targets[0]

                target.hp -= unit.attack_power
                if target.hp <= 0:
                    units.remove(target)

    return combat_rounds, units


def main():
    grid = [line.strip() for line in sys.stdin.readlines()]

    count_elves = sum(1 for row in grid for field in row if field == 'E')
    assert (count_elves > 0)

    (combat_rounds, units) = play(grid=grid, attack_power=3)
    print((combat_rounds - 1) * sum(unit.hp for unit in units))

    for attack_power in range(4, 200):
        (combat_rounds, units) = play(grid=grid, attack_power=attack_power)
        if sum(1 for unit in units if isinstance(unit, Elf)) == count_elves:
            print((combat_rounds - 1) * sum(unit.hp for unit in units))
            break


if __name__ == '__main__':
    main()
