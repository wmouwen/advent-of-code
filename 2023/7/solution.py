import re
import sys

face_values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
face_values_with_joker = [
    'A',
    'K',
    'Q',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    'J',
]


def hand_value(cards: list[str]) -> int:
    value = sum(
        (
            pow(len(face_values), len(cards) - i - 1)
            * (len(cards) - face_values.index(cards[i]) - 1)
        )
        for i in range(len(cards))
    )

    buckets = {}
    for card in cards:
        buckets[card] = buckets[card] + 1 if card in buckets else 1

    sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)

    if sorted_buckets[0][1] == 5:
        value += pow(len(face_values), len(cards) + 5)
    elif sorted_buckets[0][1] == 4:
        value += pow(len(face_values), len(cards) + 4)
    elif sorted_buckets[0][1] == 3 and sorted_buckets[1][1] == 2:
        value += pow(len(face_values), len(cards) + 3)
    elif sorted_buckets[0][1] == 3:
        value += pow(len(face_values), len(cards) + 2)
    elif sorted_buckets[0][1] == 2 and sorted_buckets[1][1] == 2:
        value += pow(len(face_values), len(cards) + 1)
    elif sorted_buckets[0][1] == 2:
        value += pow(len(face_values), len(cards))

    return value


def joker_value(cards: list[str]) -> int:
    value = sum(
        (
            pow(len(face_values_with_joker), len(cards) - i - 1)
            * (len(cards) - face_values_with_joker.index(cards[i]) - 1)
        )
        for i in range(len(cards))
    )

    buckets = {}
    for card in cards:
        buckets[card] = buckets[card] + 1 if card in buckets else 1

    jokers = buckets.pop('J') if 'J' in buckets else 0
    sorted_buckets = sorted(buckets.items(), key=lambda x: x[1], reverse=True)

    if jokers == 5 or sorted_buckets[0][1] + jokers >= 5:
        value += pow(len(face_values_with_joker), len(cards) + 5)
    elif sorted_buckets[0][1] + jokers == 4:
        value += pow(len(face_values_with_joker), len(cards) + 4)
    elif sorted_buckets[0][1] + jokers == 3 and sorted_buckets[1][1] == 2:
        value += pow(len(face_values_with_joker), len(cards) + 3)
    elif sorted_buckets[0][1] + jokers == 3:
        value += pow(len(face_values_with_joker), len(cards) + 2)
    elif sorted_buckets[0][1] + jokers == 2 and sorted_buckets[1][1] == 2:
        value += pow(len(face_values_with_joker), len(cards) + 1)
    elif sorted_buckets[0][1] + jokers == 2:
        value += pow(len(face_values_with_joker), len(cards))

    return value


class Hand:
    def __init__(self, hand: str, bid: int):
        self.hand_value = hand_value(list(hand))
        self.joker_value = joker_value(list(hand))
        self.bid: int = bid


hands = []
for line in sys.stdin:
    match = re.match(r'(?P<hand>\w+) (?P<bid>\d+)', line.strip())
    hands.append(Hand(match['hand'], int(match['bid'])))

hands.sort(key=lambda hand: hand.hand_value)
print(sum(hands[rank].bid * (rank + 1) for rank in range(len(hands))))

hands.sort(key=lambda hand: hand.joker_value)
print(sum(hands[rank].bid * (rank + 1) for rank in range(len(hands))))
