import re
import sys
from math import inf


def combo(operand, registers):
    return registers[operand - 4] if 0 <= operand - 4 < len(registers) else operand


def run(registers, instructions):
    ip = 0
    output = []

    while 0 <= ip < len(instructions):
        opcode, literal_operand = instructions[ip:ip + 2]
        combo_operand = combo(literal_operand, registers)

        ip += 2

        if opcode == 0: registers[0] = registers[0] // pow(2, combo_operand)
        if opcode == 1: registers[1] = registers[1] ^ literal_operand
        if opcode == 2: registers[1] = combo_operand % 8
        if opcode == 3 and registers[0] > 0: ip = literal_operand
        if opcode == 4: registers[1] = registers[1] ^ registers[2]
        if opcode == 5: output.append(combo_operand % 8)
        if opcode == 6: registers[1] = registers[0] // pow(2, combo_operand)
        if opcode == 7: registers[2] = registers[0] // pow(2, combo_operand)

    return output


def main():
    registers = [int(re.findall(r'\d+', sys.stdin.readline())[0]) for _ in range(3)]
    sys.stdin.readline()
    instructions = list(map(int, re.findall(r'\d+', sys.stdin.readline())))

    output = run(registers.copy(), instructions)
    print(','.join(map(str, output)))

    for i in range(pow(2, 100)):
        registers[0] = i

        output = run(registers.copy(), instructions)

        if output == instructions:
            print(i)
            break


if __name__ == '__main__':
    main()
