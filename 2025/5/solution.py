import sys


def main():
    ranges = []

    for line in sys.stdin:
        if '-' not in line:
            break

        ranges.append(list(map(int, line.strip().split('-'))))

    ranges.sort(key=lambda r: r[0])

    fresh_count = 0
    for line in sys.stdin:
        c = int(line.strip())

        if any(start <= c <= end for start, end in ranges):
            fresh_count += 1
            continue

    print(fresh_count)

    merged_ranges = [ranges[0]]
    for r in ranges[1:]:
        if r[0] <= merged_ranges[-1][1] + 1:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], r[1])
        else:
            merged_ranges.append(r)

    print(sum(end - start + 1 for start, end in merged_ranges))


if __name__ == '__main__':
    main()
