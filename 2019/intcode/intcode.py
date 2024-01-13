from typing import Self


class IntcodeComputer:
    def __init__(self, program: list[int]):
        self.memory = program
        self.ip = 0x00

    @classmethod
    def from_csv(cls, input: str) -> Self:
        return cls(
            program=list(map(int, input.split(',')))
        )

    def read(self, addr: int) -> int:
        return self.memory[addr]

    def write(self, addr: int, value: int) -> None:
        self.memory[addr] = value

    def run(self):
        while self.memory[self.ip] != 99:
            match self.memory[self.ip]:
                case 1:
                    self.write(
                        addr=self.memory[self.ip + 3],
                        value=self.read(addr=self.memory[self.ip + 1]) + self.read(addr=self.memory[self.ip + 2])
                    )
                    self.ip += 4

                case 2:
                    self.write(
                        addr=self.memory[self.ip + 3],
                        value=self.read(addr=self.memory[self.ip + 1]) * self.read(addr=self.memory[self.ip + 2])
                    )
                    self.ip += 4

                case _:
                    self.ip += 1
