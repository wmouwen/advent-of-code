from dataclasses import dataclass
import re
import sys
from functools import cache, cached_property
from itertools import combinations, permutations
from queue import Queue
from statistics import mode
from typing import Iterable

MIN_OVERLAP = 12


@dataclass(frozen=True)
class Vector:
    x: int
    y: int
    z: int

    @cached_property
    def _orientations(self) -> list['Vector']:
        def roll(v: Vector):
            return Vector(x=v.x, y=v.z, z=-v.y)

        def turn_cw(v: Vector):
            return Vector(x=v.y, y=-v.x, z=v.z)

        def turn_ccw(v: Vector):
            return Vector(x=-v.y, y=v.x, z=v.z)

        all_orientations = []
        current = self

        for roll_index in range(6):
            current = roll(current)
            all_orientations.append(current)

            for turn_index in range(3):
                current = turn_cw(current) if roll_index % 2 else turn_ccw(current)
                all_orientations.append(current)

        return all_orientations

    @cache
    def oriented(self, orientation: int):
        return self._orientations[orientation]

    @cache
    def distance(self, other: 'Vector') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    @cache
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    @cache
    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)


class Scanner:
    def __init__(self, id: int, beacons: set[Vector]):
        self.id: int = id
        self._beacons: set[Vector] = beacons

    @cache
    def beacons(self, orientation: int = 0) -> set[Vector]:
        return {beacon.oriented(orientation) for beacon in self._beacons}

    @cache
    def beacon_gaps(self, orientation: int = 0) -> set[Vector]:
        beacons = self.beacons(orientation)
        return {source - target for source, target in permutations(beacons, 2)}


@dataclass(frozen=True)
class ScannerPlacement:
    scanner: Scanner
    position: Vector
    orientation: int

    @cache
    def beacons(self) -> set[Vector]:
        return {
            self.position + beacon
            for beacon in self.scanner.beacons(orientation=self.orientation)
        }


def read_input() -> dict[int, Scanner]:
    scanners = dict()
    scanner_id, beacons = None, set()

    for line in sys.stdin:
        if match := re.match(r'--- scanner (-?\d+) ---', line):
            if scanner_id is not None and beacons:
                scanners[scanner_id] = Scanner(id=scanner_id, beacons=beacons)
            scanner_id, beacons = int(match.group(1)), set()

        if match := re.match(r'(-?\d+),(-?\d+),(-?\d+)', line):
            beacon = Vector(
                x=int(match.group(1)),
                y=int(match.group(2)),
                z=int(match.group(3)),
            )
            beacons.add(beacon)

    if scanner_id is not None and beacons:
        scanners[scanner_id] = Scanner(id=scanner_id, beacons=beacons)

    return scanners


def find_matching_orientation(
    source: ScannerPlacement,
    target_scanner: Scanner,
) -> int | None:
    source_beacon_gaps = source.scanner.beacon_gaps(source.orientation)

    for orientation in range(24):
        target_beacon_gaps = target_scanner.beacon_gaps(orientation)
        overlap = source_beacon_gaps.intersection(target_beacon_gaps)
        if len(overlap) >= (MIN_OVERLAP * (MIN_OVERLAP - 1)):
            return orientation

    return None


def map_neighbors(scanners: Iterable[Scanner]) -> dict[Scanner, set[Scanner]]:
    neighbors = {scanner: set() for scanner in scanners}

    for source, target in combinations(scanners, 2):
        source_placement = ScannerPlacement(
            scanner=source,
            position=Vector(0, 0, 0),
            orientation=0,
        )
        orientation = find_matching_orientation(
            source=source_placement,
            target_scanner=target,
        )

        if orientation:
            neighbors[source].add(target)
            neighbors[target].add(source)

    return neighbors


def find_matching_position(
    source: ScannerPlacement,
    target_scanner: Scanner,
    target_orientation: int,
) -> Vector:
    source_beacons = source.scanner.beacons(source.orientation)
    target_beacons = target_scanner.beacons(target_orientation)

    offsets = (
        source - target for source in source_beacons for target in target_beacons
    )

    return source.position + mode(offsets)


def find_scanner_placements(
    scanners: dict[int, Scanner],
) -> dict[int, ScannerPlacement]:
    neighbors = map_neighbors(scanners=scanners.values())
    origin = scanners[0]

    scanner_placements = {
        origin.id: ScannerPlacement(
            scanner=origin,
            position=Vector(0, 0, 0),
            orientation=0,
        )
    }

    queue: Queue[tuple[ScannerPlacement, Scanner]] = Queue()
    for neighbor in neighbors[origin]:
        queue.put((scanner_placements[origin.id], neighbor))

    while not queue.empty():
        source, target_scanner = queue.get()

        if target_scanner.id in scanner_placements:
            continue

        target_orientation = find_matching_orientation(
            source=source,
            target_scanner=target_scanner,
        )
        target_position = find_matching_position(
            source=source,
            target_scanner=target_scanner,
            target_orientation=target_orientation,
        )

        scanner_placements[target_scanner.id] = ScannerPlacement(
            scanner=target_scanner,
            position=target_position,
            orientation=target_orientation,
        )

        for neighbor in neighbors[target_scanner]:
            queue.put((scanner_placements[target_scanner.id], neighbor))

    return scanner_placements


def main():
    scanners = read_input()
    scanner_placements = find_scanner_placements(scanners=scanners)

    beacons = {
        beacon
        for placement in scanner_placements.values()
        for beacon in placement.beacons()
    }
    print(len(beacons))

    scanner_positions = {
        placement.position for placement in scanner_placements.values()
    }
    print(max(a.distance(b) for a, b in combinations(scanner_positions, 2)))


if __name__ == '__main__':
    main()
