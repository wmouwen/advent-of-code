import sys


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.directories = {}
        self.files = {}

    def size(self) -> int:
        return sum(file.size for file in self.files.values()) + sum(
            dir.size() for dir in self.directories.values()
        )

    def sum_small_dirs(self) -> int:
        sum = 0

        for dir in self.directories.values():
            sum += (dir.size() if dir.size() <= 100000 else 0) + dir.sum_small_dirs()

        return sum

    def smallest_dir_above(self, target: int) -> int:
        best_so_far = sys.maxsize

        for dir in self.directories.values():
            best_so_far = min(best_so_far, dir.smallest_dir_above(target=target))

            if target <= dir.size() < best_so_far:
                best_so_far = dir.size()

        return best_so_far


filesystem = Directory(name='/')
cwd = filesystem

for line in sys.stdin:
    parts = line.strip().split()

    if parts[0] == '$':
        if parts[1] == 'ls':
            continue
        elif parts[1] == 'cd':
            if parts[2] == '/':
                cwd = filesystem
            elif parts[2] == '..':
                cwd = cwd.parent
            else:
                cwd = cwd.directories[parts[2]]

    elif parts[0] == 'dir':
        cwd.directories[parts[1]] = Directory(name=parts[1], parent=cwd)

    else:
        cwd.files[parts[1]] = File(name=parts[1], size=int(parts[0]))

print(filesystem.sum_small_dirs())
print(filesystem.smallest_dir_above(target=filesystem.size() - 40000000))
