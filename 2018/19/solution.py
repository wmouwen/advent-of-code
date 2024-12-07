import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, Operation


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

    device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
    device.run()
    print(device.registers[0])

    device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
    device.registers[0] = 1
    device.run()
    print(device.registers[0])


if __name__ == '__main__':
    main()
