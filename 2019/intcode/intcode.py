from enum import Enum
from typing import Callable, Self


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


MemoryAddress = int
Instruction = int
Opcode = int
Memory = list[Instruction | int]

InputCallback = Callable[[], int]
OutputCallback = Callable[[int], None]


def split_instruction(instruction: Instruction) -> tuple[Opcode, list[ParameterMode]]:
    opcode = Opcode(instruction % 100)
    parameter_modes = [
        ParameterMode((instruction // 100) % 10),
        ParameterMode((instruction // 1000) % 10),
        ParameterMode((instruction // 10000) % 10),
    ]

    return opcode, parameter_modes


class IntcodeComputer:
    def __init__(self, program: Memory, input_callback: InputCallback = None, output_callback: OutputCallback = None):
        self.memory: Memory = program
        self.ip: MemoryAddress = 0x00
        self.input_callback: InputCallback = input_callback
        self.output_callback: OutputCallback = output_callback

    def read(self, addr: MemoryAddress, mode: ParameterMode) -> Instruction | int:
        match mode:
            case ParameterMode.POSITION:
                return self.memory[self.memory[addr]]
            case ParameterMode.IMMEDIATE:
                return self.memory[addr]

    def write(self, addr: MemoryAddress, value: int) -> None:
        self.memory[addr] = value

    def run(self):
        while True:
            opcode, modes = split_instruction(self.memory[self.ip])

            match opcode:
                case 1:
                    self.write(
                        addr=self.read(self.ip + 0x03, ParameterMode.IMMEDIATE),
                        value=self.read(self.ip + 0x01, modes[0]) + self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 2:
                    self.write(
                        addr=self.read(self.ip + 0x03, ParameterMode.IMMEDIATE),
                        value=self.read(self.ip + 0x01, modes[0]) * self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 3:
                    self.write(
                        addr=self.read(self.ip + 0x01, ParameterMode.IMMEDIATE),
                        value=self.input_callback()
                    )
                    self.ip += 0x02

                case 4:
                    self.output_callback(self.read(self.ip + 0x01, modes[0]))
                    self.ip += 0x02

                case 5:
                    if self.read(self.ip + 0x01, modes[0]) != 0:
                        self.ip = self.read(self.ip + 0x02, modes[1])
                    else:
                        self.ip += 0x03

                case 6:
                    if self.read(self.ip + 0x01, modes[0]) == 0:
                        self.ip = self.read(self.ip + 0x02, modes[1])
                    else:
                        self.ip += 0x03

                case 7:
                    self.write(
                        addr=self.read(self.ip + 0x03, ParameterMode.IMMEDIATE),
                        value=self.read(self.ip + 0x01, modes[0]) < self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 8:
                    self.write(
                        addr=self.read(self.ip + 0x03, ParameterMode.IMMEDIATE),
                        value=self.read(self.ip + 0x01, modes[0]) == self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 99:
                    # End of program
                    return

                case _:
                    self.ip += 0x01
