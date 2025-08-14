import sys


def main():
    floor = 0
    first_negative = None
    for i, move in enumerate(sys.stdin.readline().strip()):
        floor += 1 if move == '(' else -1

        if floor < 0 and first_negative is None:
            first_negative = i + 1

    print(floor)
    print(first_negative)

if __name__ == '__main__':
    main()
