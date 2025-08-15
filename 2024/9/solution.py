import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class File:
    id: int
    position: int
    length: int

    def checksum(self) -> int:
        return sum(self.id * (self.position + i) for i in range(self.length))


@dataclass(frozen=True)
class Disk:
    files: list[File]

    def checksum(self) -> int:
        return sum(file.checksum() for file in self.files)

    def defragment_blocks(self) -> 'Disk':
        files = sorted(self.files, key=lambda f: f.position)

        # Loop through the gaps in between files. Use a while-loop as the length of
        # the files list will grow as we move files into gaps.
        gap_index = 0
        while gap_index < len(files) - 1:
            gap_position = files[gap_index].position + files[gap_index].length
            gap_length = files[gap_index + 1].position - gap_position

            if gap_length > 0:
                # Move the last file into the gap, split the file if necessary
                move_file = files.pop()

                new_file = File(
                    id=move_file.id,
                    position=gap_position,
                    length=min(gap_length, move_file.length),
                )
                files.insert(gap_index + 1, new_file)

                if move_file.length > gap_length:
                    new_file = File(
                        id=move_file.id,
                        position=move_file.position,
                        length=move_file.length - gap_length,
                    )
                    files.append(new_file)

            gap_index += 1

        return Disk(files=files)

    def defragment_files(self) -> 'Disk':
        files = sorted(self.files, key=lambda f: f.position)

        # Track the first occurrence of each file length to optimize gap finding
        first_gaps = defaultdict(int)

        # Loop backwards through files
        for move_index in range(len(files) - 1, 0, -1):
            move_file = files[move_index]

            # Find the first gap that can accommodate the current file
            for gap_index in range(first_gaps[move_file.length], move_index):
                gap_position = files[gap_index].position + files[gap_index].length
                gap_length = files[gap_index + 1].position - gap_position

                if move_file.length <= gap_length:
                    # Move the new file in its entirety
                    files.pop(move_index)
                    new_file = File(
                        id=move_file.id,
                        position=gap_position,
                        length=move_file.length,
                    )
                    files.insert(gap_index + 1, new_file)

                    first_gaps[move_file.length] = gap_index + 1
                    break

        return Disk(files=files)


def read_input() -> Disk:
    disk_map = tuple(map(int, sys.stdin.readline().strip()))

    files, position = [], 0
    for key, value in enumerate(disk_map):
        if not key & 1:
            files.append(File(id=key >> 1, position=position, length=value))

        position += value

    return Disk(files=files)


def main():
    disk = read_input()
    print(disk.defragment_blocks().checksum())
    print(disk.defragment_files().checksum())


if __name__ == '__main__':
    main()
