from copy import deepcopy

MemoryAddress = str
Instruction = list[str]
Registers = dict[MemoryAddress, int]

tgl_map = {
    'inc': 'dec',
    'dec': 'inc',
    'tgl': 'inc',
    'out': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz'
}


def is_numeric(arg: str) -> bool:
    return arg.lstrip('-').isnumeric()


class AssembunnyComputer:
    def __init__(self, instructions: list[Instruction]):
        self._registers: Registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self._instructions: list[Instruction] = deepcopy(instructions)
        self._ip: int = 0x00

    def write(self, addr: MemoryAddress, value: int) -> None:
        self._registers[addr] = value

    def read(self, addr: MemoryAddress) -> int:
        if addr not in self._registers.keys():
            self._registers[addr] = 0

        return self._registers[addr]

    def _read_arg(self, argument: str) -> int:
        return int(argument) if is_numeric(argument) else self.read(argument)

    def run(self):
        while 0 <= self._ip < len(self._instructions):
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
                        self._instructions[target][0] = tgl_map[self._instructions[target][0]]

                case 'out':
                    # TODO: 2016 day 25
                    pass

                case _:
                    raise Exception('Unhandled instruction')

            self._ip += 1
