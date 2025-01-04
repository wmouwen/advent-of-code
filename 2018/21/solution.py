import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, parse_instructions, MaxCyclesReachedException, LoopException


def main():
    instructions, ip_register = parse_instructions(sys.stdin.readlines())

    # Locate correct number manually with reverse engineering. The `eqrr` line is key.
    for i in range(1, 317368400):
        try:
            device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
            device.registers[0] = i
            device.run(raise_on_loop=True, halt_after_cycles=20000)
            print(device.executions)
        except MaxCyclesReachedException:
            continue
        except LoopException:
            continue

        print(i)
        break


if __name__ == '__main__':
    main()
