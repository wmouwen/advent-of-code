import sys

floor = 0
movements = sys.stdin.readline().strip()

sys.stdout.write(str(movements.count('(') - movements.count(')')) + '\n')

for i in range(len(movements)):
    floor += {
        '(': 1,
        ')': -1,
    }[movements[i]]

    if floor == -1:
        sys.stdout.write(str(i + 1) + '\n')
        break
