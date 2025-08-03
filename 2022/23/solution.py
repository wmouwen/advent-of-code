import sys
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int


class Grove:
    elves: set[Vector] = set()
    rounds_passed: int = 0

    def run(self):
        legal_moves = [
            [Vector(-1, -1), Vector(0, -1), Vector(1, -1)],  # North
            [Vector(-1, 1), Vector(0, 1), Vector(1, 1)],  # South
            [Vector(-1, -1), Vector(-1, 0), Vector(-1, 1)],  # West
            [Vector(1, -1), Vector(1, 0), Vector(1, 1)],  # East
        ]

        proposals = dict()
        for elf in self.elves:
            proposal = elf

            if any(
                Vector(elf.x + d.x, elf.y + d.y) in self.elves
                for move in legal_moves
                for d in move
            ):
                for i in range(len(legal_moves)):
                    attempt = legal_moves[(i + self.rounds_passed) % len(legal_moves)]
                    if any(
                        Vector(elf.x + d.x, elf.y + d.y) in self.elves for d in attempt
                    ):
                        continue

                    proposal = Vector(elf.x + attempt[1].x, elf.y + attempt[1].y)
                    break

            if proposal not in proposals:
                proposals[proposal] = set()
            proposals[proposal].add(elf)

        self.elves = set()
        for proposal, candidates in proposals.items():
            if len(candidates) > 1:
                for candidate in candidates:
                    # Old spot
                    self.elves.add(candidate)
            else:
                # New spot
                self.elves.add(proposal)

        self.rounds_passed += 1

    def size(self):
        min_x = min_y = sys.maxsize
        max_x = max_y = -sys.maxsize - 1

        for elf in self.elves:
            min_x = min(min_x, elf.x)
            max_x = max(max_x, elf.x)
            min_y = min(min_y, elf.y)
            max_y = max(max_y, elf.y)

        return (max_x - min_x + 1) * (max_y - min_y + 1)

    def state(self):
        return '|'.join(str(elf.x) + '-' + str(elf.y) for elf in sorted(self.elves))


def main():
    grove = Grove()

    for y, line in enumerate(sys.stdin):
        for x, cell in enumerate(line.strip()):
            if cell == '#':
                grove.elves.add(Vector(x=x, y=y))

    while grove.rounds_passed < 10:
        grove.run()

    print(grove.size() - len(grove.elves))

    previous_state = grove.state()
    while True:
        grove.run()
        if grove.state() == previous_state:
            break
        previous_state = grove.state()

    print(grove.rounds_passed)


if __name__ == '__main__':
    main()
