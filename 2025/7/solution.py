import sys
from collections import defaultdict


def main():
    lines = [line.strip() for line in sys.stdin]

    beams = defaultdict(int)
    beams[lines[0].index('S')] = 1
    split_count = 0

    for line in lines[1:]:
        new_beams = defaultdict(int)

        for x, t in beams.items():
            if line[x] == '^':
                new_beams[x - 1] += t
                new_beams[x + 1] += t
                split_count += 1
            else:
                new_beams[x] += t

        beams = new_beams

    print(split_count)
    print(sum(beams.values()))


if __name__ == '__main__':
    main()
