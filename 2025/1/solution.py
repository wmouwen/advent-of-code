import re
import sys


def main():
    position = 50
    prev_position = 50

    zero_visits = 0
    zero_passes = 0

    for line in sys.stdin:
        if match := re.match(r'^([LR])(\d+)$', line):
            direction, rotation = (
                -1 if match.group(1) == 'L' else 1,
                int(match.group(2)),
            )
            position += direction * rotation

            if rotation == 0:
                continue

            if position % 100 == 0:
                zero_visits += 1

            zero_passes += abs((position // 100) - (prev_position // 100))

            if direction == -1:
                if position % 100 == 0:
                    zero_passes += 1
                if prev_position % 100 == 0:
                    zero_passes -= 1

            prev_position = position

    print(zero_visits)
    print(zero_passes)


if __name__ == '__main__':
    main()
