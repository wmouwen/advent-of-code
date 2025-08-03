import re
import sys


def main():
    enabled = True
    total = 0
    total_enabled = 0

    for line in sys.stdin:
        for command in re.findall(r'(mul\((\d+),(\d+)\)|do\(\)|don\'t\(\))', line):
            if command[0][:3] == 'mul':
                total += int(command[1]) * int(command[2])
                if enabled:
                    total_enabled += int(command[1]) * int(command[2])
            elif command[0] == "don't()":
                enabled = False
            elif command[0] == 'do()':
                enabled = True

    print(total)
    print(total_enabled)


if __name__ == '__main__':
    main()
