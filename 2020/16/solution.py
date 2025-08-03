import re
import sys


def main():
    rules = dict()
    while match := re.match(
        r'(?P<name>[^:]+): (?P<ranges>.+)', sys.stdin.readline().strip()
    ):
        rules[match['name']] = [
            tuple(map(int, rule_range.split('-')))
            for rule_range in match['ranges'].split(' or ')
        ]

    sys.stdin.readline()
    your_ticket = list(map(int, sys.stdin.readline().strip().split(',')))

    sys.stdin.readline()
    sys.stdin.readline()
    nearby_tickets = [
        list(map(int, line.strip().split(','))) for line in sys.stdin.readlines()
    ]

    print(
        sum(
            value
            for ticket in nearby_tickets
            for value in ticket
            if not any(a <= value <= b for rule in rules.values() for a, b in rule)
        )
    )

    valid_tickets = list(
        filter(
            lambda ticket: all(
                any(a <= value <= b for rule in rules.values() for a, b in rule)
                for value in ticket
            ),
            nearby_tickets,
        )
    )

    fields = [set(rules.keys()) for _ in rules]
    for i, field in enumerate(fields):
        for name, rule in rules.items():
            if not all(
                any(rule_range[0] <= ticket[i] <= rule_range[1] for rule_range in rule)
                for ticket in valid_tickets
            ):
                field.remove(name)

    while any(len(candidates) > 1 for candidates in fields):
        for field, candidates in enumerate(fields):
            if len(candidates) > 1:
                continue

            needle = list(candidates)[0]
            for other in range(len(fields)):
                if field == other:
                    continue
                if needle in fields[other]:
                    fields[other].remove(needle)

    output = 1
    for i, field in enumerate(fields):
        if list(field)[0].startswith('departure'):
            output *= your_ticket[i]

    print(output)


if __name__ == '__main__':
    main()
