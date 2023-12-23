import re
import sys

winning_numbers = []

for line in sys.stdin:
    match = re.match(r'Card\s+\d+: (?P<winners>[\d\s]+) \| (?P<numbers>[\d\s]+)', line)
    winners = re.findall(r'\d+', match['winners'])
    numbers = re.findall(r'\d+', match['numbers'])

    winning_numbers.append(sum(1 for number in numbers if number in winners))

print(sum(map(lambda x: pow(2, x - 1) if x > 1 else x, winning_numbers)))

cards = [1] * len(winning_numbers)
for c in range(len(cards)):
    for w in range(0, winning_numbers[c]):
        cards[c + w + 1] += cards[c]

print(sum(cards))
