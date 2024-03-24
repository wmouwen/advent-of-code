import re
import sys


class Rule:
    def __init__(self, field: str):
        self.field = field
        self.ranges = []

    def passes(self, value: int) -> bool:
        return any(rule_range[0] <= value <= rule_range[1] for rule_range in self.ranges)


class Ticket:
    def __init__(self, fields: list[int]):
        self.fields = fields

    def sum_invalid(self, rules: list[Rule]) -> int:
        return sum(field for field in self.fields if not any(rule.passes(field) for rule in rules))


def main():
    rules = []
    while rule_match := re.match(r'([^:]+): (.+)', sys.stdin.readline().strip()):
        rules.append(Rule(field=rule_match.group(1)))
        for rule_range in rule_match.group(2).split(' or '):
            rules[-1].ranges.append([int(val) for val in rule_range.split('-')])

    sys.stdin.readline()
    your_ticket = Ticket(fields=[int(val) for val in sys.stdin.readline().strip().split(',')])

    sys.stdin.readline()
    sys.stdin.readline()
    nearby_tickets = [Ticket([int(val) for val in line.strip().split(',')]) for line in sys.stdin.readlines()]

    print(sum(ticket.sum_invalid(rules) for ticket in nearby_tickets))

    valid_nearby_tickets = [ticket for ticket in nearby_tickets if not ticket.sum_invalid(rules)]

    # TODO


if __name__ == '__main__':
    main()
