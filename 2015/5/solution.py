import sys


def is_nice_one(line: str) -> bool:
    if sum(line.count(vowel) for vowel in 'aeiou') < 3:
        return False

    if not any(line[i] == line[i + 1] for i in range(len(line) - 1)):
        return False

    if any(bad in line for bad in ('ab', 'cd', 'pq', 'xy')):
        return False

    return True


def is_nice_two(line: str) -> bool:
    if not any(
        line[j : j + 2] == line[i : i + 2]
        for i in range(len(line) - 3)
        for j in range(i + 2, len(line) - 1)
    ):
        return False

    if not any(line[i] == line[i + 2] for i in range(len(line) - 2)):
        return False

    return True


def main():
    lines = tuple(line.strip() for line in sys.stdin)

    print(sum(1 for line in lines if is_nice_one(line)))
    print(sum(1 for line in lines if is_nice_two(line)))


if __name__ == '__main__':
    main()
