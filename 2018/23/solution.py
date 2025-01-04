import re
import sys

Coord = tuple[int, ...]
Nanobot = tuple[Coord, int]


def distance(a: Coord, b: Coord) -> int:
    return sum(abs(a[i] - b[i]) for i in range(len(a)))


def main():
    nanobots: list[Nanobot] = []

    for line in sys.stdin:
        match = re.findall(r'-?\d+', line.strip())
        assert len(match) == 4
        nanobots.append(((int(match[0]), int(match[1]), int(match[2])), int(match[3])))

    nanobots.sort(key=lambda x: x[1], reverse=True)
    origin, r = nanobots[0]
    print(sum(1 for bot, _ in nanobots if distance(origin, bot) <= r))


if __name__ == '__main__':
    main()
