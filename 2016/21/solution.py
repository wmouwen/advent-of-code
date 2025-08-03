import itertools
import sys


def scramble(password: list[str], instructions: list[list[str]]) -> str:
    for instr in instructions:
        if instr[0] == 'swap' and instr[1] == 'position':
            tmp = password[int(instr[2])]
            password[int(instr[2])] = password[int(instr[5])]
            password[int(instr[5])] = tmp

        elif instr[0] == 'swap' and instr[1] == 'letter':
            tmp = password.index(instr[2])
            password[password.index(instr[5])] = instr[2]
            password[tmp] = instr[5]

        elif instr[0] == 'rotate' and instr[1] in ['left', 'right']:
            index = (
                int(instr[2]) if instr[1] == 'left' else len(password) - int(instr[2])
            )
            password = password[index:] + password[:index]

        elif instr[0] == 'rotate' and instr[1] == 'based':
            index = password.index(instr[6])
            index = len(password) - (index + 1 if index >= 4 else index)
            password = password[-1:] + password[:-1]
            password = password[index:] + password[:index]

        elif instr[0] == 'reverse':
            x = int(instr[2])
            y = int(instr[4]) + 1
            password = password[:x] + list(reversed(password[x:y])) + password[y:]

        elif instr[0] == 'move':
            letter = password[int(instr[2])]
            password.remove(letter)
            password.insert(int(instr[5]), letter)

    return ''.join(password)


instructions = [line.strip().split(' ') for line in sys.stdin]

result = scramble(list('abcdefgh'), instructions)
print(result)

for permutation in itertools.permutations('abcdefgh'):
    result = scramble(list(permutation), instructions)

    if result == 'fbgdceah':
        print(''.join(permutation))
        break
