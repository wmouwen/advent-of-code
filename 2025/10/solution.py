import re
import sys
from queue import Queue


def shortest_path(target: int, buttons: set[int]) -> int | None:
    visited = {0}
    queue = Queue()
    queue.put((0, 0))

    while not queue.empty():
        state, steps = queue.get()

        if state == target:
            return steps

        for button in buttons:
            new_state = state ^ button
            if new_state not in visited:
                visited.add(new_state)
                queue.put((new_state, steps + 1))

    return None


def main():
    translation = str.maketrans({'.': '0', '#': '1'})

    button_presses = 0

    for line in sys.stdin:
        target_pattern = re.search(r'\[([.#]+)]', line).group(1)
        target = int(target_pattern.translate(translation), 2)

        buttons = set()
        for button_pattern in re.findall(r'\(([\d,]+)\)', line):
            button = 0
            for bit in button_pattern.split(','):
                button += 1 << len(target_pattern) - int(bit) - 1
            buttons.add(button)

        button_presses += shortest_path(target, buttons)

    print(button_presses)


if __name__ == '__main__':
    main()
