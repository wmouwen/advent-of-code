import re
import sys

seeds = list(map(int, re.findall(r'\d+', sys.stdin.readline())))
mappings = []

# source = None
# destination = None
for line in sys.stdin:
    if line.strip() == '':
        continue

    match = re.match(r'^(?P<source>\w+)-to-(?P<destination>\w+) map:$', line)
    if match is not None:
        # source = match['source']
        # destination = match['destination']
        mappings.append([])
        continue

    mappings[-1].append(re.match(r'^(?P<destination>\d+) (?P<start>\d+) (?P<length>\d+)', line))

locations = []
for i in range(0, len(seeds)):
    location = seeds[i]
    for mapping in mappings:
        for match in mapping:
            if int(match['start']) <= location < int(match['start']) + int(match['length']):
                location += int(match['destination']) - int(match['start'])
                break

    locations.append(location)

print(min(locations))
