import re
import sys
from typing import NamedTuple, Union


class Beacon(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    x: int
    y: int
    beacon: Beacon

    def distance_to_beacon(self) -> int:
        return abs(self.x - self.beacon.x) + abs(self.y - self.beacon.y)

    def distance_to_row(self, y: int) -> int:
        return abs(self.y - y)

    def x_in_range_for_y(self, y: int) -> tuple[int, int] | None:
        range_offset = self.distance_to_beacon() - self.distance_to_row(y)

        if range_offset >= 0:
            return self.x - range_offset, self.x + range_offset

        return None


def main():
    beacons = set()
    sensors = set()
    target_row = 2000000

    for line in sys.stdin:
        match = re.match(
            r'Sensor at x=(?P<x_s>\d+), y=(?P<y_s>\d+): closest beacon is at x=(?P<x_b>\d+), y=(?P<y_b>\d+)',
            line.strip()
        )
        if match:
            beacons.add(beacon := Beacon(y=int(match.group('y_b')), x=int(match.group('x_b'))))
            sensors.add(Sensor(y=int(match.group('y_s')), x=int(match.group('x_s')), beacon=beacon))

    ranges = sorted(filter(
        lambda value: value is not None,
        [sensor.x_in_range_for_y(target_row) for sensor in sensors]
    ))

    position_count = ranges[0][1] - ranges[0][0] + 1
    max_x = ranges[0][1]
    for i in range(1, len(ranges)):
        if ranges[i][1] <= max_x:
            continue

        position_count += ranges[i][1] - max(max_x + 1, ranges[i][0]) + 1
        max_x = ranges[i][1]

    position_count -= len([
        1
        for beacon in beacons
        if beacon.y == target_row and any(r[0] <= beacon.x <= r[1] for r in ranges)
    ])

    print(position_count)


if __name__ == '__main__':
    main()
