import re
import sys
from typing import NamedTuple


class SeedRange:
    def __init__(self, start: int, length: int, offset: int):
        self.start = start
        self.length = length
        self.offset = offset

    @property
    def end(self) -> int:
        """ Last element of range, inclusive """
        return self.start + self.length - 1

    @property
    def target_start(self) -> int:
        return self.start + self.offset

    @property
    def target_end(self) -> int:
        return self.end + self.offset


class MapRange(NamedTuple):
    start: int
    length: int
    destination: int

    @property
    def end(self):
        """ Last element of range, inclusive """
        return self.start + self.length - 1

    @property
    def offset(self):
        return self.destination - self.start


def find_lowest_location(seed_ranges: list[SeedRange], category_maps: list[list[MapRange]]) -> int:
    for category_map in category_maps:
        breakpoints = sorted(set(map(lambda map_range: map_range.start, category_map)) |
                             set(map(lambda map_range: map_range.end + 1, category_map)))

        for seed_range in seed_ranges:
            for breakpoint in breakpoints:
                if seed_range.target_start < breakpoint <= seed_range.target_end:
                    split_length = seed_range.target_end - breakpoint + 1
                    seed_ranges.append(SeedRange(
                        start=seed_range.end - split_length + 1,
                        length=split_length,
                        offset=seed_range.offset
                    ))
                    seed_range.length -= split_length
                    break

        for seed_range in seed_ranges:
            for map_range in category_map:
                if map_range.start <= seed_range.target_start <= map_range.end:
                    assert map_range.start <= seed_range.target_start <= seed_range.target_end <= map_range.end
                    seed_range.offset += map_range.offset
                    break

    return min(seed_range.target_start for seed_range in seed_ranges)


def read_input() -> (list[int], list[list[MapRange]]):
    seeds = list(map(int, re.findall(r'\d+', sys.stdin.readline())))
    category_maps = []

    for line in sys.stdin:
        if line.strip() == '':
            continue

        if re.match(r'^(\w+)-to-(\w+) map:$', line):
            category_maps.append([])
            continue

        match = re.match(r'^(?P<destination>\d+) (?P<start>\d+) (?P<length>\d+)', line)
        category_maps[-1].append(MapRange(
            start=int(match['start']),
            length=int(match['length']),
            destination=int(match['destination'])
        ))

    return seeds, category_maps


seeds, category_maps = read_input()

seed_ranges = [SeedRange(start=seed, length=1, offset=0) for seed in seeds]
print(find_lowest_location(seed_ranges, category_maps))

seed_ranges = [SeedRange(start=seeds[i], length=seeds[i + 1], offset=0) for i in range(0, len(seeds), 2)]
print(find_lowest_location(seed_ranges, category_maps))
