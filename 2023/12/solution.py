import sys


def arrangements(pattern: str, groups: list[int]) -> int:
    states = '.' + '.'.join(('#' * group for group in groups)) + '.'
    tokens = {0: 1}

    for char in pattern:
        new_tokens = {}

        for state, count in tokens.items():
            if char == '?':
                if state + 1 < len(states):
                    new_tokens[state + 1] = new_tokens.get(state + 1, 0) + count
                if states[state] == '.':
                    new_tokens[state] = new_tokens.get(state, 0) + count
            elif char == '#':
                if state + 1 < len(states) and states[state + 1] == '#':
                    new_tokens[state + 1] = new_tokens.get(state + 1, 0) + count
            elif char == '.':
                if state + 1 < len(states) and states[state + 1] == '.':
                    new_tokens[state + 1] = new_tokens.get(state + 1, 0) + count
                if states[state] == '.':
                    new_tokens[state] = new_tokens.get(state, 0) + count

        tokens = new_tokens

    return tokens.get(len(states) - 1, 0) + tokens.get(len(states) - 2, 0)


part1 = part2 = 0

for line in sys.stdin:
    pattern, groups = line.strip().split(' ')
    groups = [int(group) for group in groups.split(',')]

    part1 += arrangements(pattern, groups)
    part2 += arrangements('?'.join((pattern for _ in range(5))), groups * 5)

print(part1)
print(part2)
