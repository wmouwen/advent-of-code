import math
import re
import sys


class Rule:
    def __init__(self, field: str):
        self.field = field
        self.ranges = []

    def passes(self, value: int) -> bool:
        return any(rule_range[0] <= value <= rule_range[1] for rule_range in self.ranges)

    def __repr__(self) -> str:
        return self.field


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
    candidate_order = [rules.copy() for _ in your_ticket.fields]

    # TODO Filter fields which exist in just 1 candidate field
    for index, field_rules in enumerate(candidate_order):
        for rule in field_rules:
            if any(not rule.passes(ticket.fields[index]) for ticket in valid_nearby_tickets):
                field_rules.remove(rule)

    while any(len(field_rules) > 1 for field_rules in candidate_order):
        assigned = [
            field_rule
            for field_rules in candidate_order
            if len(field_rules) == 1
            for field_rule in field_rules
        ]

        for field_rules in candidate_order:
            if len(field_rules) <= 1:
                continue

            for rule in assigned:
                if rule in field_rules:
                    field_rules.remove(rule)

    field_order = [field_rule for field_rules in candidate_order for field_rule in field_rules]

    print(math.prod(
        value
        for index, value in enumerate(your_ticket.fields)
        if field_order[index].field.startswith('departure')
    ))


if __name__ == '__main__':
    main()
