import sys


def main():
    ranges = [tuple(map(int, r.split('-'))) for r in sys.stdin.readline().split(',')]
    upper = max(r[1] for r in ranges)
    upper_magnitude = len(str(upper))

    invalid_id_count = 0
    for lo, hi in ranges:
        invalid_ids = set()
        for i in range(1, 10 ** (upper_magnitude // 2)):
            candidate = int(str(i) + str(i))
            if lo <= candidate <= hi:
                invalid_ids.add(candidate)
        invalid_id_count += sum(invalid_ids)
    print(invalid_id_count)

    invalid_id_count = 0
    for lo, hi in ranges:
        invalid_ids = set()
        for i in range(1, 10 ** (upper_magnitude // 2)):
            candidate = int(str(i))
            while candidate <= hi:
                candidate = int(str(candidate) + str(i))
                if lo <= candidate <= hi:
                    invalid_ids.add(candidate)
        invalid_id_count += sum(invalid_ids)
    print(invalid_id_count)


if __name__ == '__main__':
    main()
