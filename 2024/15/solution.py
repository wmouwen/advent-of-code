import sys
from queue import Queue
from typing import NamedTuple


class Grid:
    def __init__(self):
        self.walls = set()
        self.boxes = set()
        self.robot = None

    def find_horizontal_targets(self, dx, stretch):
        boxes_to_move = set()

        target = (self.robot[0] + dx * (1 if dx > 0 else stretch), self.robot[1])
        while target in self.boxes:
            boxes_to_move.add(target)
            target = (target[0] + dx * stretch, target[1])

        return boxes_to_move

    def find_vertical_targets(self, dy, stretch):
        boxes_to_move = set()

        queue = Queue()
        queue.put(self.robot)

        while not queue.empty():
            current = queue.get()
            for dx in range(-1 * stretch + 1, 1 if current == self.robot else stretch):
                target = (current[0] + dx, current[1] + dy)
                if target in self.boxes:
                    queue.put(target)
                    boxes_to_move.add(target)

        return boxes_to_move

    def blocked_by_wall_horizontally(self, boxes_to_move, dx, stretch):
        return ((self.robot[0] + dx, self.robot[1]) in self.walls
                or any((x + dx * (1 if dx < 0 else stretch), y) in self.walls for x, y in boxes_to_move))

    def blocked_by_wall_vertically(self, boxes_to_move, dy, stretch):
        return ((self.robot[0], self.robot[1] + dy) in self.walls
                or any((x + dx, y + dy) in self.walls for x, y in boxes_to_move for dx in range(stretch)))

    def move(self, instruction, stretch=1):
        if instruction == '<':
            boxes_to_move = self.find_horizontal_targets(dx=-1, stretch=stretch)
            if self.blocked_by_wall_horizontally(boxes_to_move, dx=-1, stretch=stretch): return
            self.boxes = self.boxes.difference(boxes_to_move).union((x - 1, y) for x, y in boxes_to_move)
            self.robot = (self.robot[0] - 1, self.robot[1])

        elif instruction == '>':
            boxes_to_move = self.find_horizontal_targets(dx=1, stretch=stretch)
            if self.blocked_by_wall_horizontally(boxes_to_move, dx=1, stretch=stretch): return
            self.boxes = self.boxes.difference(boxes_to_move).union((x + 1, y) for x, y in boxes_to_move)
            self.robot = (self.robot[0] + 1, self.robot[1])

        elif instruction == '^':
            boxes_to_move = self.find_vertical_targets(dy=-1, stretch=stretch)
            if self.blocked_by_wall_vertically(boxes_to_move, dy=-1, stretch=stretch): return
            self.boxes = self.boxes.difference(boxes_to_move).union((x, y - 1) for x, y in boxes_to_move)
            self.robot = (self.robot[0], self.robot[1] - 1)

        elif instruction == 'v':
            boxes_to_move = self.find_vertical_targets(dy=1, stretch=stretch)
            if self.blocked_by_wall_vertically(boxes_to_move, dy=1, stretch=stretch): return
            self.boxes = self.boxes.difference(boxes_to_move).union((x, y + 1) for x, y in boxes_to_move)
            self.robot = (self.robot[0], self.robot[1] + 1)

dirs = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}


def build_grid(inp, stretch=1):
    grid = Grid()

    for y, row in enumerate(inp):
        for x, cell in enumerate(inp[y]):
            if cell == '#':
                for s in range(stretch):
                    grid.walls.add((x * stretch + s, y))

            if cell == 'O': grid.boxes.add((x * stretch, y))
            if cell == '@': grid.robot = (x * stretch, y)

    if grid.robot is None: raise Exception('No robot found')

    return grid




def main():
    inp = []
    for line in sys.stdin:
        if line.strip() == '': break
        inp.append(line.strip())

    instructions = list(instruction for line in sys.stdin for instruction in line.strip())

    grid = build_grid(inp)
    for instruction in instructions:
        grid.move(instruction)

    print(sum(b[0] + 100 * b[1] for b in grid.boxes))

    grid = build_grid(inp, stretch=2)
    for instruction in instructions:
        grid.move(instruction, stretch=2)

    print(sum(b[0] + 100 * b[1] for b in grid.boxes))


if __name__ == '__main__':
    main()
