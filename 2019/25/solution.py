import os
import re
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))

    instructions = [
        # Hull Breach, NE
        'north',
        # Corridor, S
        # 'take infinite loop',
        'south',
        # Hull Breach, NE
        'east',
        # Engineering, EW
        'east',
        # Warp Drive Maintenance, NEW
        'take semiconductor',
        'north',
        # Gift Wrapping Center, NSW
        'take planetoid',
        'north',
        # Stables, SW
        'take antenna',
        'west',
        # Navigation, E
        'east',
        # Stables, SW
        'south',
        # Gift Wrapping Center, NSW
        'west',
        # Hot Chocolate Fountain, NEW
        'take food ration',
        'west',
        # Observatory, EW
        'west',
        # Arcade, E
        'take monolith',
        'east',
        # Observatory, EW
        'east',
        # Hot Chocolate Fountain, NEW
        'north',
        # Sick Bay, NES
        'take space law space brochure',
        'east',
        # Crew Quarters, W
        'take jam',
        'west',
        # Sick Bay, NES
        'north',
        # Storage, NS
        'north',
        # Kitchen, S
        'take weather machine',
        'south',
        # Storage, NS
        'south',
        # Sick Bay, NES
        'south',
        # Hot Chocolate Fountain, NEW
        'east',
        # Gift Wrapping Center, NSW
        'south',
        # Warp Drive Maintenance, NEW
        'east',
        # Hallway, NSW
        # 'take giant electromagnet',
        'north',
        # Science Lab
        # 'take molten lava',
        'south',
        # Hallway, NSW
        'south',
        # Holodeck, NS
        # 'take escape pod',
        'south',
        # Passages, NE
        # 'take photons',
        'east',
        # Security Checkpoint, EW
    ]

    instructions = list(map(ord, '\n'.join(instructions) + '\n'))
    output = []
    computer = IntcodeComputer(
        program=program,
        input_callback=lambda: instructions.pop(0) if instructions else None,
        output_callback=lambda value: output.append(value),
    )
    computer.run()

    output = []

    items = [
        'food ration',
        'weather machine',
        'antenna',
        'space law space brochure',
        'jam',
        'semiconductor',
        'planetoid',
        'monolith',
    ]

    for perm in range(1 << len(items)):
        instructions = [
            f'take {item}' if (1 << i) & perm else f'drop {item}'
            for i, item in enumerate(items)
        ]
        instructions.append('east')
        instructions = list(map(ord, '\n'.join(instructions) + '\n'))

        computer.run()

        str_output = ''.join(map(lambda x: chr(x) if x < 255 else str(x), output))
        if match := re.search(r'by typing (\d+) on the keypad', str_output):
            print(match.group(1))
            break


if __name__ == '__main__':
    main()
