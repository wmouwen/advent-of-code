import re
import sys

seeds = list(map(int, re.findall(r'\d+', sys.stdin.readline())))
mappings = []

for line in sys.stdin:
    if line.strip() == '':
        continue

    match = re.match(r'^(?P<source>\w+)-to-(?P<destination>\w+) map:$', line)
    if match is not None:
        mappings.append([])
        continue

    mappings[-1].append(re.match(r'^(?P<destination>\d+) (?P<start>\d+) (?P<length>\d+)', line))

best = sys.maxsize
for location in seeds:
    for mapping in mappings:
        for match in mapping:
            if int(match['start']) <= location < int(match['start']) + int(match['length']):
                location += int(match['destination']) - int(match['start'])
                break

    best = min(best, location)

print(best)

# TODO Improve performance
best = sys.maxsize
for s in range(0, len(seeds), 2):
    for location in range(seeds[s], seeds[s] + seeds[s + 1]):
        for mapping in mappings:
            for match in mapping:
                if int(match['start']) <= location < int(match['start']) + int(match['length']):
                    location += int(match['destination']) - int(match['start'])
                    break

        best = min(best, location)

print(best)
