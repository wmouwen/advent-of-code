import sys
from typing import NamedTuple


class V(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return V(x=self.x + other.x, y=self.y + other.y)


ROCKS = [
    [V(x=0, y=0), V(x=1, y=0), V(x=2, y=0), V(x=3, y=0)],
    [V(x=1, y=2), V(x=0, y=1), V(x=1, y=1), V(x=2, y=1), V(x=1, y=0)],
    [V(x=2, y=2), V(x=2, y=1), V(x=0, y=0), V(x=1, y=0), V(x=2, y=0)],
    [V(x=0, y=3), V(x=0, y=2), V(x=0, y=1), V(x=0, y=0)],
    [V(x=0, y=1), V(x=1, y=1), V(x=0, y=0), V(x=1, y=0)],
]


def can_move(grid: list[V], rock: list[V], v_rock: V, d: V) -> bool:
    for r in rock:
        n = V(x=r.x + v_rock.x + d.x, y=r.y + v_rock.y + d.y)
        if not 0 <= n.x < 7 or not 0 <= n.y or n in grid:
            return False

    return True


def print_grid(grid: list[V]):
    for y in range(max(v.y for v in grid), -1, -1):
        print('|' + ''.join('#' if V(x, y) in grid else '.' for x in range(7)) + '|')
    print('+-------+')
    print()


def main():
    jet = tuple(sys.stdin.readline().strip())

    i_jet = 0
    grid = []

    v_rock_trail = tuple([-1] * 10)
    history = dict()
    loop_length, loop_increment = None, None

    for i_rock in range(1000000000000):
        rock = ROCKS[i_rock % len(ROCKS)]
        v_rock = V(x=2, y=4 + (max(v.y for v in grid) if len(grid) > 0 else -1))

        # Drop rock
        while True:
            d = V(x=(1 if jet[i_jet] == '>' else -1), y=0)
            if can_move(grid, rock, v_rock, d):
                v_rock += d

            i_jet = (i_jet + 1) % len(jet)

            d = V(x=0, y=-1)
            if not can_move(grid, rock, v_rock, d):
                v_rock += d
            else:
                break

        grid.extend(V(x=r.x + v_rock.x, y=r.y + v_rock.y) for r in rock)

        # Detect height of grid
        y_max = (max(v.y for v in grid) if len(grid) > 0 else -1)
        if i_rock == 2021:
            print(y_max + 1)

        # State pruning
        grid = list(filter(lambda g: g.y >= y_max - 50, grid))

        # Loop detection
        if i_rock > 2021 and loop_length is not None and (1000000000000 - i_rock - 1) % loop_length == 0:
            print(y_max + ((1000000000000 - i_rock - 1) // loop_length) * loop_increment + 1)
            break

        v_rock_trail = tuple(list(v_rock_trail[1:]) + [v_rock.x])
        entry = (i_rock % 5, i_jet, v_rock_trail)

        if entry in history:
            prev_rock, prev_max = history[entry]
            loop_length, loop_increment = i_rock - prev_rock, y_max - prev_max
        else:
            history[entry] = (i_rock, y_max)


if __name__ == '__main__':
    main()
