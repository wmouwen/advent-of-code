import sys


def cycle_3d(old):
    new = set()

    for x in range(min(c[0] for c in old) - 1, max(c[0] for c in old) + 2):
        for y in range(min(c[1] for c in old) - 1, max(c[1] for c in old) + 2):
            for z in range(min(c[2] for c in old) - 1, max(c[2] for c in old) + 2):
                neighbors = list(filter(
                    lambda cell: cell != (x, y, z) and
                                 abs(cell[0] - x) <= 1 and
                                 abs(cell[1] - y) <= 1 and
                                 abs(cell[2] - z) <= 1,
                    old
                ))

                if ((x, y, z) in old and 2 <= len(neighbors) <= 3) or ((x, y, z) not in old and len(neighbors) == 3):
                    new.add((x, y, z))

    return new


def cycle_4d(old):
    new = set()

    for x in range(min(c[0] for c in old) - 1, max(c[0] for c in old) + 2):
        for y in range(min(c[1] for c in old) - 1, max(c[1] for c in old) + 2):
            for z in range(min(c[2] for c in old) - 1, max(c[2] for c in old) + 2):
                for w in range(min(c[3] for c in old) - 1, max(c[3] for c in old) + 2):
                    neighbors = list(filter(
                        lambda cell: cell != (x, y, z, w) and
                                     abs(cell[0] - x) <= 1 and
                                     abs(cell[1] - y) <= 1 and
                                     abs(cell[2] - z) <= 1 and
                                     abs(cell[3] - w) <= 1,
                        old
                    ))

                    if ((x, y, z, w) in old and 2 <= len(neighbors) <= 3) or (
                            (x, y, z, w) not in old and len(neighbors) == 3):
                        new.add((x, y, z, w))

    return new


def main():
    cells_3d = {
        (x, y, 0)
        for y, row in enumerate(sys.stdin.readlines())
        for x, cell in enumerate(row)
        if cell == '#'
    }
    cells_4d = [
        (x, y, z, 0)
        for x, y, z in cells_3d
    ]

    for i in range(6):
        cells_3d = cycle_3d(cells_3d)
    print(len(cells_3d))

    for i in range(6):
        cells_4d = cycle_4d(cells_4d)
    print(len(cells_4d))


if __name__ == '__main__':
    main()
