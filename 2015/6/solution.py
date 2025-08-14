import re
import sys
from dataclasses import dataclass
from enum import StrEnum


class Action(StrEnum):
    TURN_ON = 'turn on'
    TURN_OFF = 'turn off'
    TOGGLE = 'toggle'


@dataclass(frozen=True)
class Instruction:
    action: Action
    x: range
    y: range


type Grid = list[list[int]]


def read_input() -> list[Instruction]:
    instructions = []
    regex = r'^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)$'

    for line in sys.stdin:
        if match := re.match(regex, line.strip()):
            instruction = Instruction(
                action=Action(match.group(1)),
                x=range(int(match.group(2)), int(match.group(4))),
                y=range(int(match.group(3)), int(match.group(5))),
            )
            instructions.append(instruction)

    return instructions


def switch_lights(grid: Grid, instructions: list[Instruction]) -> Grid:
    for instruction in instructions:
        for y in range(instruction.y.start, instruction.y.stop + 1):
            for x in range(instruction.x.start, instruction.x.stop + 1):
                match instruction.action:
                    case Action.TURN_ON:
                        grid[y][x] = 1
                    case Action.TURN_OFF:
                        grid[y][x] = 0
                    case Action.TOGGLE:
                        grid[y][x] = 1 - grid[y][x]

    return grid


def control_brightness(grid: Grid, instructions: list[Instruction]) -> Grid:
    for instruction in instructions:
        for y in range(instruction.y.start, instruction.y.stop + 1):
            for x in range(instruction.x.start, instruction.x.stop + 1):
                match instruction.action:
                    case Action.TURN_ON:
                        grid[y][x] += 1
                    case Action.TURN_OFF:
                        grid[y][x] = max(0, grid[y][x] - 1)
                    case Action.TOGGLE:
                        grid[y][x] += 2

    return grid


def main():
    instructions = read_input()

    grid = switch_lights([[0] * 1000 for _ in range(1000)], instructions)
    print(sum(cell for row in grid for cell in row))

    grid = control_brightness([[0] * 1000 for _ in range(1000)], instructions)
    print(sum(cell for row in grid for cell in row))


if __name__ == '__main__':
    main()
