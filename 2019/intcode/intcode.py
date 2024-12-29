from enum import Enum
from typing import Callable


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Opcode(Enum):
    ADD = 1
    MUL = 2
    IN = 3
    OUT = 4
    JNZ = 5
    JZ = 6
    LT = 7
    EQ = 8
    RB = 9
    EXIT = 99


MemoryAddress = int
Instruction = int
Memory = dict[int, Instruction | int]

InputCallback = Callable[[], int]
OutputCallback = Callable[[int], None]


class IntcodeComputer:
    @staticmethod
    def _split_instruction(instruction: Instruction) -> tuple[Opcode, tuple[ParameterMode, ...]]:
        opcode = Opcode(instruction % 100)
        modes = (
            ParameterMode((instruction // 100) % 10),
            ParameterMode((instruction // 1000) % 10),
            ParameterMode((instruction // 10000) % 10),
        )

        return opcode, modes

    def __init__(
            self,
            program: list[Instruction | int],
            input_callback: InputCallback = None,
            output_callback: OutputCallback = None
    ):
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
                case _:
                    raise Exception(f"Unknown parameter mode: {mode}")

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
            opcode, modes = self._split_instruction(self.read(self.ip, ParameterMode.IMMEDIATE))

            match opcode:
                case Opcode.ADD:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) + self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case Opcode.MUL:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) * self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case Opcode.IN:
                    self.write(
                        addr=self.read(self.ip + 0x01, modes[0], target_write=True),
                        value=self.input_callback()
                    )
                    self.ip += 0x02

                case Opcode.OUT:
                    self.output_callback(self.read(self.ip + 0x01, modes[0]))
                    self.ip += 0x02

                case Opcode.JNZ:
                    if self.read(self.ip + 0x01, modes[0]) != 0:
                        self.ip = self.read(self.ip + 0x02, modes[1])
                    else:
                        self.ip += 0x03

                case Opcode.JZ:
                    if self.read(self.ip + 0x01, modes[0]) == 0:
                        self.ip = self.read(self.ip + 0x02, modes[1])
                    else:
                        self.ip += 0x03

                case Opcode.LT:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) < self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case Opcode.EQ:
                    self.write(
                        addr=self.read(self.ip + 0x03, modes[2], target_write=True),
                        value=self.read(self.ip + 0x01, modes[0]) == self.read(self.ip + 0x02, modes[1])
                    )
                    self.ip += 0x04

                case Opcode.RB:
                    self.relative_base += self.read(self.ip + 0x01, modes[0])
                    self.ip += 0x02

                case Opcode.EXIT:
                    return
