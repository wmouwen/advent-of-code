import sys


def joltage(batteries: list[int], n: int) -> int:
    output = 0

    while n > 0:
        n -= 1
        best = max(batteries[:-n] if n > 0 else batteries)
        output = output * 10 + best
        batteries = batteries[batteries.index(best) + 1 :]

    return output


def main():
    banks = list(list(map(int, line.strip())) for line in sys.stdin)

    print(sum(joltage(batteries, 2) for batteries in banks))
    print(sum(joltage(batteries, 12) for batteries in banks))


if __name__ == '__main__':
    main()
