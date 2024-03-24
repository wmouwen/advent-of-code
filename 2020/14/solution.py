import re
import sys


def masked_value(value: int, mask: str) -> int:
    binary = list(f'{value:0{len(mask)}b}')
    assert len(binary) == len(mask)

    for i in range(len(mask)):
        if mask[i] != 'X':
            binary[i] = mask[i]

    return int(''.join(binary), 2)


def fill_memory_v1(input: list[str]) -> dict[int, int]:
    memory = dict()
    mask = ''

    for line in input:
        if match := re.match(r'mask = ([01X]{36})', line):
            mask = match.group(1)

        elif match := re.match(r'mem\[(\d+)] = (\d+)', line):
            assert len(mask) == 36
            memory[int(match.group(1))] = masked_value(int(match.group(2)), mask)

    return memory


def main():
    lines = [line.strip() for line in sys.stdin]

    print(sum(fill_memory_v1(lines).values()))


if __name__ == '__main__':
    main()
