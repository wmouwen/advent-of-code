import sys
from dataclasses import dataclass
from queue import Queue

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


@dataclass(frozen=True)
class SideRoom:
    key: str
    depth: int
    pods: tuple[str, ...]

    def unfold(self, inserts: list[str]) -> 'SideRoom':
        return SideRoom(
            key=self.key,
            depth=self.depth + len(inserts),
            pods=(self.pods[0], *inserts, *self.pods[1:]),
        )

    @property
    def organized(self) -> bool:
        return all(pod == self.key for pod in self.pods)

    def pop(self) -> tuple['SideRoom', str]:
        return (
            SideRoom(key=self.key, depth=self.depth, pods=self.pods[1:]),
            self.pods[0],
        )

    def push(self, pod: str) -> 'SideRoom':
        return SideRoom(key=self.key, depth=self.depth, pods=(pod, *self.pods))

    def __len__(self) -> int:
        return len(self.pods)


@dataclass(frozen=True)
class Hallway:
    situation: tuple[SideRoom | str | None, ...]

    def unfold(self) -> 'Hallway':
        return Hallway(
            situation=(
                None,
                None,
                self.situation[2].unfold(['D', 'D']),
                None,
                self.situation[4].unfold(['C', 'B']),
                None,
                self.situation[6].unfold(['B', 'A']),
                None,
                self.situation[8].unfold(['A', 'C']),
                None,
                None,
            )
        )

    @property
    def organized(self) -> bool:
        return all(
            cell is None or (isinstance(cell, SideRoom) and cell.organized)
            for cell in self.situation
        )

    def can_move_from_room(self, room_index: int, hallway_index: int) -> bool:
        room = self.situation[room_index]

        if not isinstance(room, SideRoom) or room.organized:
            return False

        if self.situation[hallway_index] is not None:
            return False

        for i in range(
            min(room_index, hallway_index),
            max(room_index, hallway_index) + 1,
        ):
            if isinstance(self.situation[i], str):
                return False

        return True

    def move_from_room(self, room_index: int, hallway_index: int) -> 'Hallway':
        assert self.can_move_from_room(room_index, hallway_index)

        room, element = self.situation[room_index].pop()

        situation = list(self.situation)
        situation[room_index] = room
        situation[hallway_index] = element

        return Hallway(situation=tuple(situation))

    def can_move_to_room(self, hallway_index: int, room_index: int) -> bool:
        room = self.situation[room_index]
        element = self.situation[hallway_index]

        if not isinstance(room, SideRoom) or not room.organized:
            return False

        if not isinstance(element, str) or element != room.key:
            return False

        for i in range(
            min(room_index, hallway_index),
            max(room_index, hallway_index) + 1,
        ):
            if  i != hallway_index and isinstance(self.situation[i], str):
                return False

        return True

    def move_to_room(self, hallway_index: int, room_index: int) -> 'Hallway':
        assert self.can_move_to_room(hallway_index, room_index)

        element = self.situation[hallway_index]
        room = self.situation[room_index].push(element)

        situation = list(self.situation)
        situation[room_index] = room
        situation[hallway_index] = None

        return Hallway(situation=tuple(situation))


def read_input() -> Hallway:
    situation = sys.stdin.readlines()

    return Hallway(
        situation=(
            None,
            None,
            SideRoom(key='A', depth=2, pods=(situation[2][3], situation[3][3])),
            None,
            SideRoom(key='B', depth=2, pods=(situation[2][5], situation[3][5])),
            None,
            SideRoom(key='C', depth=2, pods=(situation[2][7], situation[3][7])),
            None,
            SideRoom(key='D', depth=2, pods=(situation[2][9], situation[3][9])),
            None,
            None,
        )
    )


def min_energy(hallway: Hallway) -> int | None:
    best = None

    visited: dict[Hallway, int] = dict()
    queue: Queue[tuple[int, Hallway]] = Queue()
    queue.put((0, hallway))

    while not queue.empty():
        energy, current = queue.get()

        if current.organized:
            if best is None or energy < best:
                best = energy
            continue

        if current in visited and energy >= visited[current]:
            continue
        visited[current] = energy

        for room_index in (2, 4, 6, 8):
            for hallway_index in (0, 1, 3, 5, 7, 9, 10):
                if current.can_move_from_room(
                    room_index=room_index,
                    hallway_index=hallway_index,
                ):
                    next_hallway = current.move_from_room(
                        room_index=room_index,
                        hallway_index=hallway_index,
                    )

                    element = next_hallway.situation[hallway_index]
                    horizontal_move = abs(room_index - hallway_index)
                    room = next_hallway.situation[room_index]
                    vertical_move = room.depth - len(room)
                    energy_addition = ENERGY[element] * (
                        horizontal_move + vertical_move
                    )

                    queue.put((energy + energy_addition, next_hallway))

                if current.can_move_to_room(
                    hallway_index=hallway_index,
                    room_index=room_index,
                ):
                    next_hallway = current.move_to_room(
                        hallway_index=hallway_index,
                        room_index=room_index,
                    )

                    element = current.situation[hallway_index]
                    horizontal_move = abs(room_index - hallway_index)
                    room = current.situation[room_index]
                    vertical_move = room.depth - len(room)
                    energy_addition = ENERGY[element] * (
                        horizontal_move + vertical_move
                    )

                    queue.put((energy + energy_addition, next_hallway))

    return best


def main():
    hallway = read_input()
    print(min_energy(hallway))

    hallway = hallway.unfold()
    print(min_energy(hallway))


if __name__ == '__main__':
    main()
