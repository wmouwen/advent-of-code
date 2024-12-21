import re
import sys
from functools import cache
from typing import NamedTuple


class V(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return V(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return V(x=self.x - other.x, y=self.y - other.y)


NUMPAD = {
    '7': V(x=0, y=0),
    '8': V(x=1, y=0),
    '9': V(x=2, y=0),
    '4': V(x=0, y=1),
    '5': V(x=1, y=1),
    '6': V(x=2, y=1),
    '1': V(x=0, y=2),
    '2': V(x=1, y=2),
    '3': V(x=2, y=2),
    '0': V(x=1, y=3),
    'A': V(x=2, y=3),
}
KEYPAD = {
    '^': V(x=1, y=0),
    'A': V(x=2, y=0),
    '<': V(x=0, y=1),
    'v': V(x=1, y=1),
    '>': V(x=2, y=1),
}


def calc_paths(pad: dict):
    paths = {a: {b: [] for b in pad.keys()} for a in pad.keys()}

    for a in pad.keys():
        for b in pad.keys():
            if a == b:
                paths[a][b].append('')
                continue

            d = pad[b] - pad[a]
            if d.x != 0 and pad[a] + V(x=d.x, y=0) in pad.values():
                paths[a][b].append(('>' if d.x > 0 else '<') * abs(d.x) + ('v' if d.y > 0 else '^') * abs(d.y))

            if d.y != 0 and pad[a] + V(x=0, y=d.y) in pad.values():
                paths[a][b].append(('v' if d.y > 0 else '^') * abs(d.y) + ('>' if d.x > 0 else '<') * abs(d.x))

    return paths


NUMPAD_PATHS = calc_paths(NUMPAD)
KEYPAD_PATHS = calc_paths(KEYPAD)


def control_numpad(buttons_to_press):
    paths = ['']
    current_position = 'A'

    for button in buttons_to_press:
        paths = [
            history + addition + 'A'
            for history in paths
            for addition in NUMPAD_PATHS[current_position][button]
        ]
        current_position = button

    return paths


@cache
def control_keypad(buttons_to_press):
    paths = ['']
    current_position = 'A'

    for button in buttons_to_press:
        paths = [
            history + addition + 'A'
            for history in paths
            for addition in KEYPAD_PATHS[current_position][button]
        ]
        current_position = button

    return paths


def main():
    complexity_sum_two = 0
    complexity_sum_twentyfive = 0

    for line in sys.stdin:
        code = line.strip()
        numeric_part = int(re.search(r'[1-9]\d+', line.strip()).group(0))

        paths = control_numpad(code)

        for i in range(2):
            paths = [
                new_path
                for old_path in paths
                for new_path in control_keypad(old_path)
            ]

        complexity_sum_two += numeric_part * min(len(path) for path in paths)

        # for i in range(23):
        #     shortest = min(len(p) for p in paths)
        #
        #     paths = [
        #         new_path
        #         for old_path in filter(lambda path: len(path) == shortest, paths)
        #         for new_path in control_keypad(old_path)
        #     ]
        #
        # complexity_sum_twentyfive += numeric_part * min(len(path) for path in paths)

    print(complexity_sum_two)
    print(complexity_sum_twentyfive)


if __name__ == '__main__':
    main()
