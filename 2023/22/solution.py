import sys


class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Brick:
    def __init__(self, head: Vector, tail: Vector):
        self.head = head
        self.tail = tail

    @property
    def distance_to_ground(self) -> int:
        return min(self.head.z, self.tail.z) - 1

    def fall(self) -> None:
        self.head.z -= 1
        self.tail.z -= 1

    def blocks(self):
        for x in range(min(self.head.x, self.tail.x), max(self.head.x, self.tail.x) + 1):
            for y in range(min(self.head.y, self.tail.y), max(self.head.y, self.tail.y) + 1):
                for z in range(min(self.head.z, self.tail.z), max(self.head.z, self.tail.z) + 1):
                    yield Vector(x=x, y=y, z=z)

    def supports(self, other) -> bool:
        for block in other.blocks():
            if (self.head.x <= block.x <= self.tail.x and
                    self.head.y <= block.y <= self.tail.y and
                    self.head.z <= block.z - 1 <= self.tail.z):
                return True
        return False


bricks = []

for line in sys.stdin:
    head, tail = map(lambda coord: coord.split(','), line.strip().split('~'))
    bricks.append(Brick(
        head=Vector(x=int(head[0]), y=int(head[1]), z=int(head[2])),
        tail=Vector(x=int(tail[0]), y=int(tail[1]), z=int(tail[2]))
    ))

bricks.sort(key=lambda brick: brick.distance_to_ground)
settled = False

while not settled:
    settled = True

    for i, brick in enumerate(bricks):
        if brick.distance_to_ground == 0:
            continue

        if not any(other.supports(brick) for other in bricks[:i]):
            brick.fall()
            settled = False

safe_to_remove_count = 0
for i, brick in enumerate(bricks):
    safe_to_remove = True
    for j, other in enumerate(bricks):
        if brick == other:
            continue
        if brick.supports(other):
            safe_to_remove = False
            for k, third in enumerate(bricks):
                if brick == third or other == third:
                    continue
                if third.supports(other):
                    safe_to_remove = True
                    break
            if not safe_to_remove:
                break
    if safe_to_remove:
        safe_to_remove_count += 1

print(safe_to_remove_count)
