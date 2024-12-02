import sys


def sign(num: int) -> int:
    return int(num / abs(num)) if num != 0 else 0


def is_safe(levels: list[int]) -> bool:
    if len(levels) < 2: return True

    slope = sign(levels[1] - levels[0])
    if slope == 0: return False

    for i in range(len(levels) - 1):
        if sign(levels[i + 1] - levels[i]) != slope:
            return False

        if not (1 <= abs(levels[i + 1] - levels[i]) <= 3):
            return False

    return True


def is_safe_tolerated(levels: list[int]) -> bool:
    for i in range(len(levels)):
        if is_safe(list(levels[:i] + levels[i + 1:])):
            return True

    return False


def main():
    safe_complete, safe_tolerated = 0, 0

    for line in sys.stdin:
        levels = list(map(int, line.strip().split()))

        if is_safe(levels):
            safe_complete += 1
        elif is_safe_tolerated(levels):
            safe_tolerated += 1

    print(safe_complete)
    print(safe_complete + safe_tolerated)


if __name__ == '__main__':
    main()
