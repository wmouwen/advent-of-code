import sys


def val(arg, variables):
    return variables[arg] if arg in variables else int(arg)


def run_raw_alu(instructions: list[list[str]], candidate: str):
    candidate = list(map(int, candidate))
    variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    for op, *args in instructions:
        if op == 'inp': variables[args[0]] = candidate.pop(0)
        if op == 'add': variables[args[0]] += val(args[1], variables)
        if op == 'mul': variables[args[0]] *= val(args[1], variables)
        if op == 'div': variables[args[0]] = variables[args[0]] // val(args[1], variables)
        if op == 'mod': variables[args[0]] %= val(args[1], variables)
        if op == 'eql': variables[args[0]] = int(variables[args[0]] == val(args[1], variables))

    return variables['z']


def run_optimized(short_instructions: list[tuple[int, int, int]], candidate: list[int]):
    output = 0

    for i in range(len(candidate)):
        a, b, c = short_instructions[i]
        output = next_z(candidate[i], a, b, c, output)

    return output


def next_z(digit, a, b, c, z):
    if (z % 26) + b == digit:
        return z // a

    return (z // a) * 26 + digit + c


def solve(instructions: list[tuple[int, int, int]], direction=-1, candidate: list[int] = None, z: int = 0) -> str | None:
    if candidate is None:
        candidate = []

    if len(candidate) == len(instructions):
        return ''.join(map(str, candidate)) if z == 0 else None

    a, b, c = instructions[len(candidate)]
    if a == 26:
        digit = (z % 26) + b
        if 1 <= digit <= 9:
            answer = solve(instructions, direction, candidate + [digit], next_z(digit, a, b, c, z))
            if answer is not None: return answer

    else:
        for digit in (range(9, 0, -1) if direction == -1 else range(1, 10)):
            answer = solve(instructions, direction, candidate + [digit], next_z(digit, a, b, c, z))
            if answer is not None: return answer

    return None


# Observations:
# - Puzzle input is crafted to have 14 repetitions of a similar subprogram.
# - The most significant digit of the input, i.e. the first digit, only influences itself.
# - Lesser significant digits are dependent on themselves and more significant digits.
# - z is the only variable keeping state in between digits
# - Each repetition has three different numbers (a, b, c) in the input file, mapping to two different scenarios.
#   - Let's call the scenarios 'increase' and 'decrease'
#   - For increase, a ==  1, b > 0 and c > 0
#   - For decrease, a == 26, b < 0 and c doesn't matter
#   - #(increases) == #(decreases)
#   - decrease only happens if it matches f(z, b, digit) == 0 with f() reverse engineered. If this fails, continue the search.
def main():
    instructions = [line.strip().split(' ') for line in sys.stdin]
    assert len(instructions) == 18 * 14

    short_instructions = [
        (int(instructions[offset + 4][2]), int(instructions[offset + 5][2]), int(instructions[offset + 15][2]))
        for offset in range(0, len(instructions), 18)
    ]

    print(solve(short_instructions))
    print(solve(short_instructions, direction=1))


if __name__ == '__main__':
    main()
