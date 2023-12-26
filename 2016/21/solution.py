import sys


def scramble(input: str, instructions: list[list[str]]) -> str:
    password: list[str] = list(input)

    for instr in instructions:
        print(''.join(password))
        print(instr)

        if instr[0] == "swap" and instr[1] == "position":
            tmp = password[int(instr[2])]
            password[int(instr[2])] = password[int(instr[5])]
            password[int(instr[5])] = tmp

        elif instr[0] == "swap" and instr[1] == "letter":
            tmp = password.index(instr[2])
            password[password.index(instr[5])] = instr[2]
            password[tmp] = instr[5]

        elif instr[0] == "rotate" and instr[1] in ["left", "right"]:
            # TODO FIX
            index = int(instr[2])
            if instr[1] == "right":
                index = len(password) - index
            password = password[index:] + password[:index]

        elif instr[0] == "rotate" and instr[1] == "based":
            # TODO FIX
            index = len(password) - (password.index(instr[6]))
            password = password[-1:] + password[:-1]
            password = password[index:] + password[:index]

        elif instr[0] == "reverse":
            x = int(instr[2])
            y = int(instr[4]) + 1
            password = password[:x] + list(reversed(password[x:y])) + password[y:]

        elif instr[0] == "move":
            index = int(instr[2])
            letter = password[index]
            password.remove(letter)
            password.insert(int(instr[5]), letter)

    return ''.join(password)


instructions = [line.strip().split(' ') for line in sys.stdin]
print(scramble('abcde', instructions))
