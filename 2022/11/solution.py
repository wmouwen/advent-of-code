import math
import re
import sys
from queue import Queue


class Monkey:
    def __init__(self):
        self.items: Queue | None = Queue()
        self.operation_operator: str | None = None
        self.operation_value: str | None = None
        self.test_value: int | None = None
        self.target_true: int | None = None
        self.target_false: int | None = None


def copy_monkey(monkey: Monkey) -> Monkey:
    new_monkey = Monkey()
    for item in monkey.items.queue:
        new_monkey.items.put(item)
    new_monkey.operation_operator = monkey.operation_operator
    new_monkey.operation_value = monkey.operation_value
    new_monkey.test_value = monkey.test_value
    new_monkey.target_true = monkey.target_true
    new_monkey.target_false = monkey.target_false
    return new_monkey


def play(monkeys: list[Monkey], rounds: int, reduce_worry: bool):
    inspections = [0 for _ in monkeys]
    lcm = math.lcm(*(monkey.test_value for monkey in monkeys))

    for round in range(rounds):
        for id, monkey in enumerate(monkeys):
            while not monkey.items.empty():
                inspections[id] += 1

                # Get item
                item = monkey.items.get()

                # Inspect item
                value = (
                    int(monkey.operation_value)
                    if monkey.operation_value != 'old'
                    else item
                )
                if monkey.operation_operator == '*':
                    item *= value
                elif monkey.operation_operator == '+':
                    item += value

                # Decrease worry level
                if reduce_worry:
                    item //= 3
                else:
                    item %= lcm

                # Forward item
                if not item % monkey.test_value:
                    monkeys[monkey.target_true].items.put(item)
                else:
                    monkeys[monkey.target_false].items.put(item)

    inspections.sort()
    return inspections[-2] * inspections[-1]


monkeys: list[Monkey] = []

for line in sys.stdin:
    if re.match(r'Monkey (\d+):', line.strip()):
        monkeys.append(Monkey())

    if match := re.match(r'Starting items: ([\d,\s]+)', line.strip()):
        for item in match.group(1).split(', '):
            monkeys[-1].items.put(int(item))

    if match := re.match(r'Operation: new = old ([+*]) (\d+|old)', line.strip()):
        monkeys[-1].operation_operator = match.group(1)
        monkeys[-1].operation_value = match.group(2)

    if match := re.match(r'Test: divisible by (\d+)', line.strip()):
        monkeys[-1].test_value = int(match.group(1))

    if match := re.match(r'If true: throw to monkey (\d+)', line.strip()):
        monkeys[-1].target_true = int(match.group(1))

    if match := re.match(r'If false: throw to monkey (\d+)', line.strip()):
        monkeys[-1].target_false = int(match.group(1))

print(
    play(
        monkeys=[copy_monkey(monkey) for monkey in monkeys],
        rounds=20,
        reduce_worry=True,
    )
)
print(
    play(
        monkeys=[copy_monkey(monkey) for monkey in monkeys],
        rounds=10000,
        reduce_worry=False,
    )
)
