import re
import sys
from collections import Counter
from itertools import chain, combinations
from queue import Queue
from typing import NamedTuple, Any, Generator


class Component(NamedTuple):
    element: str
    type: str


Floor = set[Component]


class State(NamedTuple):
    moves: int
    elevator: int
    floors: list[Floor]


def allowed_floor(floor: Floor) -> bool:
    if len(set(component.type for component in floor)) != 2:
        return True

    for component in floor:
        if (
            component.type == 'microchip'
            and Component(element=component.element, type='generator') not in floor
        ):
            return False

    return True


def move(state: State) -> Generator[State, Any, None]:
    possible_moves = chain(
        combinations(state.floors[state.elevator], r=2),
        combinations(state.floors[state.elevator], r=1),
    )

    for move in possible_moves:
        for direction in [-1, 1]:
            next_elevator = state.elevator + direction

            if not 0 <= next_elevator < len(state.floors):
                continue

            floors = state.floors.copy()
            floors[state.elevator] = floors[state.elevator].difference(move)
            floors[next_elevator] = floors[next_elevator].union(move)

            if not allowed_floor(floors[state.elevator]) or not allowed_floor(
                floors[next_elevator]
            ):
                continue

            yield State(moves=state.moves + 1, elevator=next_elevator, floors=floors)


def hash_state(state: State):
    return tuple(
        tuple(Counter(component.type for component in floor).most_common())
        for floor in state.floors
    ), state.elevator


def least_moves(floors):
    visited = set()
    queue = Queue()
    queue.put(State(moves=0, elevator=0, floors=floors))

    while not queue.empty():
        current_state = queue.get()

        for next_state in move(current_state):
            state_hash = hash_state(next_state)
            if state_hash in visited:
                continue

            if all(len(floor) == 0 for floor in next_state.floors[:-1]):
                return next_state.moves

            visited.add(state_hash)
            queue.put(next_state)


def main():
    floors = [
        {
            Component(element=element, type=type)
            for element, type in re.findall(
                r'(\w+)(?:-compatible)? (microchip|generator)', line.strip()
            )
        }
        for line in sys.stdin
    ]

    print(least_moves(floors))

    floors[0] |= {
        Component(element='elerium', type='generator'),
        Component(element='elerium', type='microchip'),
        Component(element='dilithium', type='generator'),
        Component(element='dilithium', type='microchip'),
    }

    print(least_moves(floors))


if __name__ == '__main__':
    main()
