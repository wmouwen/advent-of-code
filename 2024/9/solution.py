import sys
from typing import NamedTuple

DiskMap = list[int]


class File(NamedTuple):
    id: int
    size: int


Disk = list[File | None]


def build_disk(disk_map: DiskMap) -> Disk:
    disk = []

    for key, value in enumerate(disk_map):
        if key % 2 == 0:
            file = File(id=key // 2, size=value)
            disk.extend([file] * file.size)
        else:
            disk.extend([None] * int(value))

    return disk


def checksum(disk: Disk) -> int:
    return sum(index * file.id for index, file in enumerate(disk) if file is not None)


def defragment_blocks(disk: Disk) -> Disk:
    index = 0

    while index < len(disk):
        while disk[index] is None:
            disk[index] = disk.pop()

        index += 1
        while disk[-1] is None:
            disk.pop()

    return disk


def defragment_files(disk: Disk) -> Disk:
    index = len(disk) - 1

    while index >= 0:
        if isinstance(disk[index], File) and (
            disk[index - 1] is None or disk[index - 1].id != disk[index].id
        ):
            for candidate_start in range(index):
                if not all(
                    disk[candidate_start + b] is None for b in range(disk[index].size)
                ):
                    continue

                for b in range(disk[index].size):
                    disk[candidate_start + b] = disk[index + b]
                    disk[index + b] = None
                break

        index -= 1

    return disk


def main():
    disk = build_disk(list(map(int, sys.stdin.readline().strip())))

    print(checksum(defragment_blocks(disk.copy())))
    print(checksum(defragment_files(disk.copy())))


if __name__ == '__main__':
    main()
