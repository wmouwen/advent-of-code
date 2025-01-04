import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../device')))
from device import Device, parse_instructions


def main():
    instructions, ip_register = parse_instructions(sys.stdin.readlines())

    device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
    device.run()
    print(device.registers[0])

    device = Device(register_count=6, instructions=instructions, ip_register=ip_register)
    device.registers[0] = 1
    device.run()
    print(device.registers[0])


if __name__ == '__main__':
    main()
