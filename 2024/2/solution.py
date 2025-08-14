import sys


def sign(num: int) -> int:
    return int(num / abs(num)) if num != 0 else 0


def safe(levels: list[int]) -> bool:
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]

    return all(abs(diff) <= 3 and sign(diff) == sign(diffs[0]) for diff in diffs)


def main():
    safe_complete, safe_tolerated = 0, 0

    for line in sys.stdin:
        levels = list(map(int, line.strip().split()))

        if safe(levels):
            safe_complete += 1
        elif any(safe(levels[:i] + levels[i + 1 :]) for i in range(len(levels))):
            safe_tolerated += 1

    print(safe_complete)
    print(safe_complete + safe_tolerated)


if __name__ == '__main__':
    main()
