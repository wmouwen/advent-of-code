import re
import sys


def solve(ax, ay, bx, by, x, y):
    # x = ca * ax + cb * bx
    # y = ca * ay + cb * by
    #
    # ca = (x - cb * bx) / ax
    # ca = (y - cb * by) / ay
    #
    # (x - cb * bx) / ax = (y - cb * by) / ay
    # (x - cb * bx) * ay = (y - cb * by) * ax
    # x * ay - cb * bx * ay = y * ax - cb * by * ax
    # cb * bx * ay - cb * by * ax = x * ay - y * ax
    # cb * (bx * ay - by * ax) = x * ay - y * ax

    if ax == 0 or bx * ay - by * ax == 0:
        return None, None

    cb = (x * ay - y * ax) / (bx * ay - by * ax)
    ca = (x - cb * bx) / ax

    if ca % 1 != 0 or cb % 1 != 0:
        return None, None

    return int(ca), int(cb)


def main():
    tokens_near, tokens_far = 0, 0

    while True:
        line = sys.stdin.readline()
        if line.strip().split(' ')[0] != 'Button':
            break

        ax, ay = map(int, re.findall(r'(\d+)', line))
        bx, by = map(int, re.findall(r'(\d+)', sys.stdin.readline()))
        x, y = map(int, re.findall(r'(\d+)', sys.stdin.readline()))
        sys.stdin.readline()

        ca, cb = solve(ax, ay, bx, by, x, y)
        if ca is not None and cb is not None and 0 <= ca <= 100 and 0 <= cb <= 100:
            tokens_near += 3 * ca + cb

        ca, cb = solve(ax, ay, bx, by, x + 10000000000000, y + 10000000000000)
        if ca is not None and cb is not None:
            tokens_far += 3 * ca + cb

    print(tokens_near)
    print(tokens_far)


if __name__ == '__main__':
    main()
