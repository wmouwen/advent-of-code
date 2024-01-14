import sys


def step(seafloor):
    next_floor = [['.' for _ in line] for line in seafloor]

    for y, row in enumerate(seafloor):
        for x, field in enumerate(row):
            if field == '>':
                if seafloor[y][(x + 1) % len(row)] == '.':
                    next_floor[y][(x + 1) % len(row)] = '>'
                else:
                    next_floor[y][x] = '>'

    for y, row in enumerate(seafloor):
        for x, field in enumerate(row):
            if field == 'v':
                if seafloor[(y + 1) % len(seafloor)][x] != 'v' and next_floor[(y + 1) % len(seafloor)][x] == '.':
                    next_floor[(y + 1) % len(seafloor)][x] = 'v'
                else:
                    next_floor[y][x] = 'v'

    return next_floor


def hash_floor(seafloor):
    return '\n'.join((''.join(line) for line in seafloor))


def main():
    seafloor = [list(line.strip()) for line in sys.stdin]

    states = [hash_floor(seafloor)]

    while True:
        seafloor = step(seafloor)
        state = hash_floor(seafloor)
        if state in states:
            break
        states.append(state)

    print(len(states))


if __name__ == '__main__':
    main()
