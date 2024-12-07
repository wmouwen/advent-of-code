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
    registers: list[int] = [0, 0, 0, 0]

    def execute(self, operation: Operation | str, a: int, b: int, c: int):
        match operation.value if isinstance(operation, Operation) else operation:
            case Operation.addr.value:
                self.registers[c] = self.registers[a] + self.registers[b]
            case Operation.addi.value:
                self.registers[c] = self.registers[a] + b
            case Operation.mulr.value:
                self.registers[c] = self.registers[a] * self.registers[b]
            case Operation.muli.value:
                self.registers[c] = self.registers[a] * b
            case Operation.banr.value:
                self.registers[c] = self.registers[a] & self.registers[b]
            case Operation.bani.value:
                self.registers[c] = self.registers[a] & b
            case Operation.borr.value:
                self.registers[c] = self.registers[a] | self.registers[b]
            case Operation.bori.value:
                self.registers[c] = self.registers[a] | b
            case Operation.setr.value:
                self.registers[c] = self.registers[a]
            case Operation.seti.value:
                self.registers[c] = a
            case Operation.gtir.value:
                self.registers[c] = int(a > self.registers[b])
            case Operation.gtri.value:
                self.registers[c] = int(self.registers[a] > b)
            case Operation.gtrr.value:
                self.registers[c] = int(self.registers[a] > self.registers[b])
            case Operation.eqir.value:
                self.registers[c] = int(a == self.registers[b])
            case Operation.eqri.value:
                self.registers[c] = int(self.registers[a] == b)
            case Operation.eqrr.value:
                self.registers[c] = int(self.registers[a] == self.registers[b])
            case _:
                raise Exception(f'Unknown operation: "{operation}"')
