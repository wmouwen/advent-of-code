import math
import sys
from enum import Enum
from queue import Queue


class Pulse(Enum):
    LOW = 'low'
    HIGH = 'high'


class Module:
    def __init__(self, destinations: list[str]):
        self.destinations = destinations

    def trigger(self, name: str, pulse: Pulse) -> Pulse | None:
        pass

    def reset(self) -> None:
        pass


class FlipFlop(Module):
    def __init__(self, destinations: list[str]):
        super().__init__(destinations=destinations)
        self.memory: bool = False

    def trigger(self, name: str, pulse: Pulse) -> Pulse | None:
        if pulse == Pulse.HIGH:
            return None

        self.memory = not self.memory

        return Pulse.HIGH if self.memory else Pulse.LOW

    def reset(self) -> None:
        self.memory = False


class Conjunction(Module):
    def __init__(self, destinations: list[str]):
        super().__init__(destinations=destinations)
        self.memory: dict[str, Pulse] = {}

    def add_source(self, name: str) -> None:
        self.memory[name] = Pulse.LOW

    def trigger(self, name: str, pulse: Pulse) -> Pulse | None:
        self.memory[name] = pulse

        return Pulse.LOW if all(p == Pulse.HIGH for p in self.memory.values()) else Pulse.HIGH

    def reset(self) -> None:
        for name in self.memory:
            self.memory[name] = Pulse.LOW


class Broadcaster(Module):
    def trigger(self, name: str, pulse: Pulse) -> Pulse:
        return pulse


class Output(Module):
    def __init__(self):
        super().__init__(destinations=[])


modules = {}

for line in sys.stdin:
    name, destinations = line.strip().split(' -> ')

    if name == 'broadcaster':
        modules[name] = Broadcaster(destinations=destinations.split(', '))
    elif name[0] == '%':
        modules[name[1:]] = FlipFlop(destinations=destinations.split(', '))
    elif name[0] == '&':
        modules[name[1:]] = Conjunction(destinations=destinations.split(', '))

for name in [name for module in modules.values() for name in module.destinations if name not in modules]:
    modules[name] = Output()

for name, module in modules.items():
    for destination in module.destinations:
        if isinstance(modules[destination], Conjunction):
            modules[destination].add_source(name)

pulses = {Pulse.LOW: 0, Pulse.HIGH: 0}
button_press = 0

while True:
    button_press += 1

    queue = Queue()
    queue.put(('button', Pulse.LOW, 'broadcaster'))

    while not queue.empty():
        source, pulse, destination = queue.get()
        pulses[pulse] += 1

        # print(f"{source} -{pulse.value}-> {destination}")

        if destination == 'rx' and pulse == Pulse.LOW:
            print(button_press)
            exit(0)

        output = modules[destination].trigger(source, pulse)
        if output is not None:
            for next_destination in modules[destination].destinations:
                queue.put((destination, output, next_destination))

    if button_press == 1000:
        print(math.prod(pulses.values()))

# TODO Optimize.
