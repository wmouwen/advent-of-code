import sys


def distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    assert len(a) == len(b)
    return sum(abs(a[i] - b[i]) for i in range(len(a)))


def main():
    constellations = [
        [tuple(map(int, line.strip().split(',')))]
        for line in sys.stdin
        if line.strip() != ''
    ]

    for i in range(len(constellations)):
        for j in range(i + 1, len(constellations)):
            if any(
                distance(a, b) <= 3
                for a in constellations[i]
                for b in constellations[j]
            ):
                constellations[j].extend(constellations[i])
                constellations[i] = None
                break

    print(sum(1 for constellation in constellations if constellation is not None))


if __name__ == '__main__':
    main()
