from enum import Enum


class Operation(Enum):
    addr = 'addr'
    addi = 'addi'
    mulr = 'mulr'
    muli = 'muli'
    banr = 'banr'
    bani = 'bani'
    borr = 'borr'
    bori = 'bori'
    setr = 'setr'
    seti = 'seti'
    gtir = 'gtir'
    gtri = 'gtri'
    gtrr = 'gtrr'
    eqir = 'eqir'
    eqri = 'eqri'
    eqrr = 'eqrr'


type Instruction = (Operation, int, int, int)


class Device:
    registers: list[int]

    _instructions: list[Instruction]
    _instruction_pointer: int = 0
    _bind_instruction_pointer: int

    def __init__(self, register_count: int, instructions: list[Instruction] = None, ip_register: int = None):
        self.registers = [0] * register_count
        self._instructions = instructions if instructions is not None else []
        self._bind_instruction_pointer = ip_register

    def run(self):
        while 0 <= self._instruction_pointer < len(self._instructions):
            if self._bind_instruction_pointer is not None:
                self.registers[self._bind_instruction_pointer] = self._instruction_pointer

            # print(self.registers, self._instructions[self._instruction_pointer], self._instruction_pointer)
            self.execute(*self._instructions[self._instruction_pointer])

            if self._bind_instruction_pointer is not None:
                self._instruction_pointer = self.registers[self._bind_instruction_pointer]
            self._instruction_pointer += 1

    def execute(self, operation: Operation, a: int, b: int, c: int):
        match operation:
            case Operation.addr:
                self.registers[c] = self.registers[a] + self.registers[b]
            case Operation.addi:
                self.registers[c] = self.registers[a] + b
            case Operation.mulr:
                self.registers[c] = self.registers[a] * self.registers[b]
            case Operation.muli:
                self.registers[c] = self.registers[a] * b
            case Operation.banr:
                self.registers[c] = self.registers[a] & self.registers[b]
            case Operation.bani:
                self.registers[c] = self.registers[a] & b
            case Operation.borr:
                self.registers[c] = self.registers[a] | self.registers[b]
            case Operation.bori:
                self.registers[c] = self.registers[a] | b
            case Operation.setr:
                self.registers[c] = self.registers[a]
            case Operation.seti:
                self.registers[c] = a
            case Operation.gtir:
                self.registers[c] = int(a > self.registers[b])
            case Operation.gtri:
                self.registers[c] = int(self.registers[a] > b)
            case Operation.gtrr:
                self.registers[c] = int(self.registers[a] > self.registers[b])
            case Operation.eqir:
                self.registers[c] = int(a == self.registers[b])
            case Operation.eqri:
                self.registers[c] = int(self.registers[a] == b)
            case Operation.eqrr:
                self.registers[c] = int(self.registers[a] == self.registers[b])
            case _:
                raise Exception(f'Unknown operation: "{operation}"')
