import ast
import math
import sys
from functools import cmp_to_key


def compare_order(left: list[int | list], right: list[int | list]) -> int:
    for i in range(min(len(left), len(right))):
        assert isinstance(left[i], (int, list)) and isinstance(right[i], (int, list))

        if isinstance(left[i], int) and isinstance(right[i], int):
            if left[i] < right[i]:
                return 1
            elif left[i] > right[i]:
                return -1
            else:
                continue

        sub_decision = compare_order(
            left=left[i] if isinstance(left[i], list) else [left[i]],
            right=right[i] if isinstance(right[i], list) else [right[i]]
        )

        if sub_decision != 0:
            return sub_decision

    if len(left) > len(right):
        return -1
    elif len(left) < len(right):
        return 1
    else:
        return 0


part1 = 0
lines = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    lines.append(ast.literal_eval(line))

    if not len(lines) % 2:
        if compare_order(lines[-2], lines[-1]) == 1:
            part1 += len(lines) // 2

print(part1)

dividers = ([[2]], [[6]])
lines.extend(dividers)
sorted_lines = sorted(lines, key=cmp_to_key(lambda a, b: compare_order(b, a)))

print(math.prod(i + 1 for i, line in enumerate(sorted_lines) if line in dividers))
