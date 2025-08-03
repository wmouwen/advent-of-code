import re
import sys


def combo(operand, registers):
    return registers[operand - 4] if 0 <= operand - 4 < len(registers) else operand


def run(registers, instructions):
    ip = 0
    output = []

    while 0 <= ip < len(instructions):
        opcode, literal_operand = instructions[ip : ip + 2]
        combo_operand = combo(literal_operand, registers)

        ip += 2

        if opcode == 0:
            registers[0] >>= combo_operand
        if opcode == 1:
            registers[1] ^= literal_operand
        if opcode == 2:
            registers[1] = combo_operand & 7
        if opcode == 3 and registers[0] > 0:
            ip = literal_operand
        if opcode == 4:
            registers[1] ^= registers[2]
        if opcode == 5:
            output.append(combo_operand & 7)
        if opcode == 6:
            registers[1] = registers[0] >> combo_operand
        if opcode == 7:
            registers[2] = registers[0] >> combo_operand

    return output


# Observations:
# - Puzzle input is handcrafted with a purpose in mind and can be reverse engineered into the below program.
#       while a > 0:
#         b = (a & 7) ^ 7
#         b = b ^ (a >> b) ^ 7
#         output.append(b & 7)
#         a = a >> 3
# - Puzzle input of registers B and C doesn't matter.
# - The value of register A is processed three bits at a time; each triplet adds one number to the output.
# - The least significant triplet of bits only influences the first number of the output.
# - The most significant triplet of bits solely determines the last number of the output.
# Given the observations, a DFS on bit triplets can be performed.
def search(instructions: list[int], attempt: list[int] = None, index: int = 0):
    if attempt is None:
        attempt = [0] * len(instructions)

    for i in range(8):
        attempt[index] = i
        reg_a = sum(val << 3 * (len(attempt) - i - 1) for i, val in enumerate(attempt))
        output = run([reg_a, 0, 0], instructions)

        if len(output) != len(instructions):
            continue

        if output[-(index + 1)] == instructions[-(index + 1)]:
            if index + 1 == len(instructions):
                return reg_a

            if (sub := search(instructions, attempt.copy(), index + 1)) is not None:
                return sub

    return None


def main():
    registers = [int(re.findall(r'\d+', sys.stdin.readline())[0]) for _ in range(3)]
    sys.stdin.readline()
    instructions = list(map(int, re.findall(r'\d+', sys.stdin.readline())))

    output = run(registers.copy(), instructions)
    print(','.join(map(str, output)))

    print(search(instructions))


if __name__ == '__main__':
    main()
