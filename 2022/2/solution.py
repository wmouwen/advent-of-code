import sys

games: list[tuple] = []

for line in sys.stdin:
    opponent, self = line.strip().split(' ')
    games.append((ord(opponent) - ord('A'), ord(self) - ord('X')))

print(sum(3 * ((game[1] - game[0] + 1) % 3) + game[1] + 1 for game in games))
print(sum(3 * game[1] + ((game[0] + game[1] - 1) % 3) + 1 for game in games))
