import re
import sys


def masked_value(value: int, mask: str) -> int:
    binary = list(f'{value:0{len(mask)}b}')
    assert len(binary) == len(mask)

    for i in range(len(mask)):
        if mask[i] != 'X':
            binary[i] = mask[i]

    return int(''.join(binary), 2)


def fill_memory_v1(lines: list[str]) -> dict[int, int]:
    memory = dict()
    mask = ''

    for line in lines:
        if match := re.match(r'mask = ([01X]{36})', line):
            mask = match.group(1)

        elif match := re.match(r'mem\[(\d+)] = (\d+)', line):
            assert len(mask) == 36
            memory[int(match.group(1))] = masked_value(int(match.group(2)), mask)

    return memory


def fill_mask(mask: list[str]) -> list[str]:
    if 'X' not in mask:
        return [''.join(mask)]

    x_index = mask.index('X')

    return [
        *fill_mask(mask[:x_index] + ['0'] + mask[x_index + 1:]),
        *fill_mask(mask[:x_index] + ['1'] + mask[x_index + 1:])
    ]


def masked_addresses(value: int, mask: str) -> list[int]:
    binary = list(f'{value:0{len(mask)}b}')
    assert len(binary) == len(mask)

    for i in range(len(mask)):
        if mask[i] == 'X':
            binary[i] = 'X'
        elif mask[i] == '1':
            binary[i] = '1'

    addresses = fill_mask(binary)

    return [int(address, 2) for address in addresses]


def fill_memory_v2(lines: list[str]) -> dict[int, int]:
    memory = dict()
    mask = ''

    for line in lines:
        if match := re.match(r'mask = ([01X]{36})', line):
            mask = match.group(1)

        elif match := re.match(r'mem\[(\d+)] = (\d+)', line):
            assert len(mask) == 36

            for address in masked_addresses(int(match.group(1)), mask):
                memory[address] = int(match.group(2))

    return memory


def main():
    lines = [line.strip() for line in sys.stdin]

    print(sum(fill_memory_v1(lines).values()))
    print(sum(fill_memory_v2(lines).values()))


if __name__ == '__main__':
    main()
