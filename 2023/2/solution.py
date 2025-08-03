import re
import sys

cubes_available = {'red': 12, 'green': 13, 'blue': 14}

part1 = 0
part2 = 0

for line in sys.stdin:
    match = re.match(r'Game (?P<id>\d+): (?P<game>.+)', line)
    valid_game = True
    cubes_minimal = {'red': 0, 'green': 0, 'blue': 0}

    for game_set in match['game'].split('; '):
        for cubes in game_set.split(', '):
            cube_parts = cubes.split(' ')
            if int(cube_parts[0]) > cubes_available[cube_parts[1]]:
                valid_game = False

            cubes_minimal[cube_parts[1]] = max(
                cubes_minimal[cube_parts[1]], int(cube_parts[0])
            )

    if valid_game:
        part1 += int(match['id'])

    part2 += cubes_minimal['red'] * cubes_minimal['green'] * cubes_minimal['blue']

print(part1)
print(part2)
