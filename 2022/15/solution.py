import re
import sys
from typing import NamedTuple, Generator, Any


class Vector(NamedTuple):
    x: int
    y: int


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

    def position_is_in_range(self, position: Vector) -> int:
        return abs(self.x - position.x) + abs(self.y - position.y) <= self.distance_to_beacon()

    def x_in_range_for_y(self, y: int) -> tuple[int, int] | None:
        range_offset = self.distance_to_beacon() - self.distance_to_row(y)
        return (self.x - range_offset, self.x + range_offset) if range_offset >= 0 else None

    def unreachable_edge(self) -> Generator[Vector, Any, None]:
        offset_x = self.distance_to_beacon() + 1
        offset_y = 0

        while offset_x > 0:
            yield Vector(x=self.x + offset_x, y=self.y + offset_y)
            offset_x -= 1
            offset_y += 1

        while offset_y > 0:
            yield Vector(x=self.x + offset_x, y=self.y + offset_y)
            offset_y -= 1
            offset_x -= 1

        while offset_x < 0:
            yield Vector(x=self.x + offset_x, y=self.y + offset_y)
            offset_x += 1
            offset_y -= 1

        while offset_y < 0:
            yield Vector(x=self.x + offset_x, y=self.y + offset_y)
            offset_y += 1
            offset_x += 1


class Grid:
    beacons: set[Beacon] = set()
    sensors: set[Sensor] = set()

    def ranges_for_row(self, y: int) -> list[tuple[int, int]]:
        return sorted(filter(
            lambda value: value is not None,
            [sensor.x_in_range_for_y(y) for sensor in self.sensors]
        ))

    def beacons_in_range(self, y: int) -> int:
        ranges = self.ranges_for_row(y)

        return len([
            1
            for beacon in self.beacons
            if beacon.y == y and any(r[0] <= beacon.x <= r[1] for r in ranges)
        ])

    def free_positions_in_row(self, y: int) -> int:
        ranges = self.ranges_for_row(y)

        positions_in_range = 0
        x_current = ranges[0][0] - 1
        for i in range(len(ranges)):
            if ranges[i][1] <= x_current:
                continue

            positions_in_range += ranges[i][1] - max(x_current + 1, ranges[i][0]) + 1
            x_current = ranges[i][1]

        return positions_in_range - self.beacons_in_range(y)


def main():
    grid = Grid()

    for line in sys.stdin:
        match = re.match(
            r'Sensor at x=(?P<s_x>\d+), y=(?P<s_y>\d+): closest beacon is at x=(?P<b_x>\d+), y=(?P<b_y>\d+)',
            line.strip()
        )
        if match:
            grid.beacons.add(beacon := Beacon(y=int(match.group('b_y')), x=int(match.group('b_x'))))
            grid.sensors.add(Sensor(y=int(match.group('s_y')), x=int(match.group('s_x')), beacon=beacon))

    # y_target = 10
    y_target = 2000000

    print(grid.free_positions_in_row(y_target))

    for sensor in grid.sensors:
        for position in sensor.unreachable_edge():
            if not (0 <= position.x <= y_target * 2 and 0 <= position.y <= y_target * 2):
                continue

            if any(other.position_is_in_range(position) for other in grid.sensors):
                continue

            print(position.x * 4000000 + position.y)
            return


if __name__ == '__main__':
    main()
