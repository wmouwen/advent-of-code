import sys

seats = [int(bp.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2) for bp in sys.stdin]

print(max(seats))
print(next(filter(lambda s: s + 1 not in seats and s + 2 in seats, seats)) + 1)
