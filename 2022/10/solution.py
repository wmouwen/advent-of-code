import sys

cycle = 0
instruction = None
x = 1

signal_strengths = []
crt = [['.' for cx in range(40)] for cy in range(6)]

while True:
    cycle += 1

    if instruction is None:
        line = sys.stdin.readline()
        if not line:
            break
        instruction = [cycle, *line.strip().split(' ')]

    if not (cycle - 20) % 40:
        signal_strengths.append(cycle * x)

    if x - 1 <= ((cycle - 1) % 40) <= x + 1:
        crt[cycle // 40][cycle % 40] = '#'

    if instruction[1] == 'noop':
        instruction = None
    elif instruction[1] == 'addx' and instruction[0] == cycle - 1:
        x += int(instruction[2])
        instruction = None

print(sum(signal_strengths))

for row in crt:
    print(''.join(row))
