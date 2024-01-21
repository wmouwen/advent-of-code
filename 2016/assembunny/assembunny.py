from copy import deepcopy
from typing import NamedTuple, Callable

MemoryAddress = str
Instruction = list[str]
Registers = dict[MemoryAddress, int]

OutputCallback = Callable[[int], None]

TOGGLE_MAP = {
    'inc': 'dec',
    'dec': 'inc',
    'tgl': 'inc',
    'out': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz'
}


class DetectedFunction(NamedTuple):
    target: MemoryAddress
    result: int
    registers_to_clear: list[MemoryAddress]
    skip: int


def is_numeric(arg: str) -> bool:
    return arg.lstrip('-').isnumeric()


class AssembunnyComputer:
    def __init__(self, instructions: list[Instruction], output_callback: OutputCallback = None):
        self._instructions: list[Instruction] = deepcopy(instructions)
        self._output_callback: OutputCallback = output_callback

        self._registers: Registers = {}
        self._ip: int = 0x00
        self._interrupted: bool = False

    def interrupt(self) -> None:
        self._interrupted = True

    def write(self, addr: MemoryAddress, value: int) -> None:
        self._registers[addr] = value

    def read(self, addr: MemoryAddress) -> int:
        if addr not in self._registers.keys():
            self._registers[addr] = 0

        return self._registers[addr]

    def _read_arg(self, argument: str) -> int:
        return int(argument) if is_numeric(argument) else self.read(argument)

    def _detect_addition(self, instructions: list[Instruction], offset: int) -> DetectedFunction | None:
        if not 0 <= offset <= len(instructions) - 3:
            return None

        instructions = instructions[offset:offset + 3]

        if (instructions[0][0] == 'inc' and
                instructions[1][0] == 'dec' and
                instructions[2] == ['jnz', instructions[1][1], '-2']):
            return DetectedFunction(
                target=instructions[0][1],
                result=self.read(instructions[1][1]),
                registers_to_clear=[instructions[1][1]],
                skip=3
            )

        return None

    def _detect_multiplication(self, instructions: list[Instruction], offset: int) -> DetectedFunction | None:
        if not 0 <= offset <= len(instructions) - 6:
            return None

        instructions = instructions[offset:offset + 6]

        if (instructions[0][0] == 'cpy' and
                instructions[1][0] == 'inc' and
                instructions[2] == ['dec', instructions[0][2]] and
                instructions[3] == ['jnz', instructions[0][2], '-2'] and
                instructions[4][0] == 'dec' and
                instructions[5] == ['jnz', instructions[4][1], '-5']):
            return DetectedFunction(
                target=instructions[1][1],
                result=self._read_arg(instructions[0][1]) * self.read(instructions[5][1]),
                registers_to_clear=[instructions[0][2], instructions[5][1]],
                skip=6
            )

        return None

    def run(self) -> None:
        while not self._interrupted and 0 <= self._ip < len(self._instructions):
            if multiplication := self._detect_multiplication(self._instructions, self._ip):
                self.write(multiplication.target, self.read(multiplication.target) + multiplication.result)
                for register in multiplication.registers_to_clear:
                    self.write(register, 0)
                self._ip += multiplication.skip - 1

            elif addition := self._detect_addition(self._instructions, self._ip):
                self.write(addition.target, self.read(addition.target) + addition.result)
                for register in addition.registers_to_clear:
                    self.write(register, 0)
                self._ip += addition.skip - 1

            else:
                instruction, *args = self._instructions[self._ip]
                match instruction:
                    case 'cpy':
                        if not is_numeric(args[1]):
                            self.write(args[1], self._read_arg(args[0]))

                    case 'inc':
                        if not is_numeric(args[0]):
                            self.write(args[0], self.read(args[0]) + 1)

                    case 'dec':
                        if not is_numeric(args[0]):
                            self.write(args[0], self.read(args[0]) - 1)

                    case 'jnz':
                        if self._read_arg(args[0]) != 0:
                            self._ip += self._read_arg(args[1]) - 1

                    case 'tgl':
                        target = self._ip + self._read_arg(args[0])

                        if 0 <= target < len(self._instructions):
                            self._instructions[target][0] = TOGGLE_MAP[self._instructions[target][0]]

                    case 'out':
                        self._output_callback(self._read_arg(args[0]))

                    case _:
                        raise Exception('Unhandled instruction')

                self._ip += 1
