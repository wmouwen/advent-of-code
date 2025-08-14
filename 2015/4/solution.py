import sys
from hashlib import md5
from itertools import count


def main():
    salt = sys.stdin.readline().strip()
    five_zeroes_found = False

    for offset in count(1):
        hashed = md5((salt + str(offset)).encode()).hexdigest()

        if hashed.startswith('00000'):
            if not five_zeroes_found:
                five_zeroes_found = True
                print(offset)

            if hashed.startswith('000000'):
                print(offset)
                break


if __name__ == '__main__':
    main()
