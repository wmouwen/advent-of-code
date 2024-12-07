import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, Operation


def main():
    device = Device()

    opcodes = [{operation for operation in Operation}] * 16
    three_or_more_candidates_count = 0

    while True:
        before = re.match(r'^Before: \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)]$', sys.stdin.readline().strip())
        if not before:
            break

        before = list(map(int, before.groups()))
        instruction = list(map(int, re.match(
            r'^(-?\d+) (-?\d+) (-?\d+) (-?\d+)$',
            sys.stdin.readline().strip()).groups()))
        after = list(map(int, re.match(
            r'^After:  \[(-?\d+), (-?\d+), (-?\d+), (-?\d+)]$',
            sys.stdin.readline().strip()).groups()))

        # Clear empty line
        sys.stdin.readline()

        candidates = set()
        for operation in Operation:
            device.registers = before.copy()
            device.execute(operation, instruction[1], instruction[2], instruction[3])
            if device.registers == after:
                candidates.add(operation)

        three_or_more_candidates_count += int(len(candidates) >= 3)
        opcodes[instruction[0]] = opcodes[instruction[0]] & candidates

    print(three_or_more_candidates_count)

    while any(len(candidates) > 1 for candidates in opcodes):
        for opcode, candidates in enumerate(opcodes):
            if len(candidates) > 1:
                continue

            needle = list(candidates)[0]
            for other in range(len(opcodes)):
                if opcode == other:
                    continue
                if needle in opcodes[other]:
                    opcodes[other].remove(needle)

    opcode_map = {opcode: list(candidates)[0] for opcode, candidates in enumerate(opcodes)}

    device = Device()
    for line in sys.stdin:
        if match := re.match(r'^(-?\d+) (-?\d+) (-?\d+) (-?\d+)$', line.strip()):
            operation = opcode_map[int(match.group(1))]
            device.execute(operation, int(match.group(2)), int(match.group(3)), int(match.group(4)))

    print(device.registers[0])


if __name__ == '__main__':
    main()
