import re
import sys
from typing import List


class Instruction:
    def __init__(self, operation: str, argument: str):
        self.operation = operation
        self.argument = argument

    def __str__(self):
        return self.operation + ' ' + self.argument


class Program:
    def __init__(self, instructions: List[Instruction]):
        self.accumulator = 0
        self.instructions = instructions
        self.instructions_executed = [False] * len(instructions)
        self.instruction_pointer = 0
        self.terminated = 0

    def tick(self):
        instruction = self.instructions[self.instruction_pointer]

        if instruction.operation == 'acc':
            self.accumulator += int(instruction.argument)
        elif instruction.operation == 'jmp':
            self.instruction_pointer += int(instruction.argument) - 1
        elif instruction.operation == 'nop':
            pass

        self.instruction_pointer += 1

    def run(self):
        while not self.terminated:
            self.tick()

            if self.instruction_pointer not in range(len(self.instructions)):
                self.terminated = True

    def run_until_first_repetition(self):
        while not self.terminated:
            self.instructions_executed[self.instruction_pointer] = True

            self.tick()

            if self.instruction_pointer not in range(len(self.instructions)):
                self.terminated = True
            elif self.instructions_executed[self.instruction_pointer]:
                break


instructions = []
for line in sys.stdin:
    parts = re.search(r'^(\w+) ([+-]\d+)', line)
    instructions.append(Instruction(parts.group(1), parts.group(2)))

program = Program(instructions)
program.run_until_first_repetition()
print(program.accumulator)

for i in range(len(instructions)):
    if instructions[i].operation != 'jmp':
        continue

    instructions[i].operation = 'nop'

    program = Program(instructions)
    program.run_until_first_repetition()

    if program.terminated:
        print(program.accumulator)
        break

    instructions[i].operation = 'jmp'
