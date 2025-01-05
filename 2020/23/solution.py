import sys
from math import prod


def build_dict(seed: list[int], stretch: int = None) -> dict[int, int]:
    cups = {seed[i - 1]: seed[i] for i in range(len(seed))}

    if stretch is not None:
        cups.update({i: i + 1 for i in range(len(seed) + 1, stretch + 1)})
        cups[seed[-1]] = len(seed) + 1
        cups[stretch] = seed[0]

    return cups


def mix(cups: dict[int, int], current: int, moves: int):
    for m in range(moves):
        selected = (cups[current], cups[cups[current]], cups[cups[cups[current]]])

        destination = ((current - 2) % len(cups)) + 1
        while destination in selected:
            destination = ((destination - 2) % len(cups)) + 1

        cups[current] = cups[selected[-1]]
        cups[selected[-1]] = cups[destination]
        cups[destination] = selected[0]

        current = cups[current]


def first_n(cups: dict[int, int], current: int, n: int) -> list[int]:
    return [(current := cups[current]) for _ in range(n)]


def main():
    seed = list(map(int, list(sys.stdin.readline().strip())))

    cups = build_dict(seed)
    mix(cups, current=seed[0], moves=100)
    print(''.join(map(str, first_n(cups, current=1, n=len(seed) - 1))))

    cups = build_dict(seed, stretch=1_000_000)
    mix(cups, current=seed[0], moves=10_000_000)
    print(prod(first_n(cups, current=1, n=2)))


if __name__ == "__main__":
    main()
