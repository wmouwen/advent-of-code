import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, Operation, ExecutionsExceededException, LoopException


def main():
    ip_register = None
    instructions = []

    for line in sys.stdin:
        if match := re.match(r'^#ip (-?\d+)$', line.strip()):
            ip_register = int(match.group(1))

        if match := re.match(r'^(\w+) (-?\d+) (-?\d+) (-?\d+)$', line.strip()):
            instructions.append(
                (Operation[match.group(1)], int(match.group(2)), int(match.group(3)), int(match.group(4)))
            )

    # Locate correct number manually with reverse engineering. The `eqrr` line is key.
    for i in range(1, 317368400):
        try:
            device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
            device.registers[0] = i
            device.run(break_on_loop=True, max_executions=20000)
            print(device.executions)
        except ExecutionsExceededException:
            continue
        except LoopException:
            continue

        print(i)
        break


if __name__ == '__main__':
    main()
