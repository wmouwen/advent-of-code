from enum import Enum
from typing import Callable, Self
from unittest import case


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


MemoryAddress = int
Instruction = int
Opcode = int
Memory = dict[int, Instruction | int]

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
    def __init__(self, program: list[Instruction | int], input_callback: InputCallback = None,
                 output_callback: OutputCallback = None):
        self.memory: Memory = dict(zip(range(len(program)), program))
        self.input_callback: InputCallback = input_callback
        self.output_callback: OutputCallback = output_callback

        self.ip: MemoryAddress = 0x00
        self.relative_base: int = 0x00

    def read(self, addr: MemoryAddress, mode: ParameterMode, target_write: bool = False) -> Instruction | int:
        if target_write:
            match mode:
                case ParameterMode.POSITION:
                    return self.memory[addr]
                case ParameterMode.IMMEDIATE:
                    return self.memory[addr]
                case ParameterMode.RELATIVE:
                    return self.relative_base + self.memory[addr]

        else:
            match mode:
                case ParameterMode.POSITION:
                    read_addr = self.memory[addr]
                case ParameterMode.IMMEDIATE:
                    read_addr = addr
                case ParameterMode.RELATIVE:
                    read_addr = self.relative_base + self.memory[addr]
                case _:
                    raise Exception(f"Unknown parameter mode: {mode}")

            return self.memory[read_addr] if read_addr in self.memory else 0

    def write(self, addr: MemoryAddress, value: int) -> None:
        self.memory[addr] = value

    def run(self):
        while True:
            opcode, modes = split_instruction(self.read(self.ip, ParameterMode.IMMEDIATE))

            # print("---", self.ip, self.read(self.ip, ParameterMode.IMMEDIATE))
            # print(self.read(1000, ParameterMode.IMMEDIATE))

            match opcode:
                case 1:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) + self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 2:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) * self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 3:
                    self.write(
                        addr=self.read(self.ip + 0x01, modes[0], target_write=True),
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
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) < self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 8:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) == self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case 9:
                    self.relative_base += self.read(self.ip + 0x01, modes[0])
                    self.ip += 0x02

                case 99:
                    # End of program
                    return

                case _:
                    self.ip += 0x01
