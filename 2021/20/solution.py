import sys


def evolve(lit, algorithm, cycle_nr):
    minx, maxx = min(p[0] for p in lit), max(p[0] for p in lit)
    miny, maxy = min(p[1] for p in lit), max(p[1] for p in lit)
    lit, prev = set(), lit
    is_edge_lit = (
        algorithm[0]
        and cycle_nr > 0
        and not (cycle_nr & 1 == 0 and not algorithm[(1 << 9) - 1])
    )

    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            hash_value = sum(
                1 << (3 * (1 - dy) + (1 - dx))
                for dy in range(-1, 2)
                for dx in range(-1, 2)
                if (x + dx, y + dy) in prev
                or (
                    is_edge_lit
                    and (not minx <= x + dx <= maxx or not miny <= y + dy <= maxy)
                )
            )

            if algorithm[hash_value]:
                lit.add((x, y))

    return lit


def main():
    algorithm = [cell == '#' for cell in sys.stdin.readline().strip()]
    sys.stdin.readline()

    assert len(algorithm) == 1 << 9

    lit = {
        (x, y)
        for y, line in enumerate(sys.stdin.readlines())
        for x, cell in enumerate(line.strip())
        if cell == '#'
    }

    for cycle_nr in range(0, 2):
        lit = evolve(lit, algorithm, cycle_nr)

    print(len(lit))

    for cycle_nr in range(2, 50):
        lit = evolve(lit, algorithm, cycle_nr)

    print(len(lit))


if __name__ == '__main__':
    main()
