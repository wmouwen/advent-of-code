MemoryAddress = int
Instruction = list[str]
Registers = dict[str, int]


class AssembunnyComputer:
    def __init__(self, instructions: list[Instruction]):
        self.registers: Registers = dict()
        self.instructions: list[Instruction] = instructions

        self.ip: MemoryAddress = 0x00

    def argval(self, argument: str) -> int:
        if argument.lstrip('-').isnumeric():
            return int(argument)

        if argument not in self.registers.keys():
            self.registers[argument] = 0

        return self.registers[argument]

    def run(self):
        while 0 <= self.ip < len(self.instructions):
            instruction, *args = self.instructions[self.ip]

            match instruction:
                case 'cpy':
                    self.registers[args[1]] = self.argval(args[0])

                case 'inc':
                    if args[0] not in self.registers.keys():
                        self.registers[args[0]] = 0

                    self.registers[args[0]] += 1

                case 'dec':
                    if args[0] not in self.registers.keys():
                        self.registers[args[0]] = 0

                    self.registers[args[0]] -= 1

                case 'jnz':
                    if self.argval(args[0]) != 0:
                        self.ip += self.argval(args[1]) - 1

            self.ip += 1
