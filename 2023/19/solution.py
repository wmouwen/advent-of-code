import re
import sys
from typing import NamedTuple


class Rule(NamedTuple):
    category: str
    operator: str
    threshold: int
    target: str


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s


def is_accepted(part: Part) -> bool:
    current_rule = 'in'

    while current_rule not in ['A', 'R']:
        for rule in workflows[current_rule]:
            if isinstance(rule, str):
                current_rule = rule
                break

            assert isinstance(rule, Rule)
            ref = getattr(part, rule.category)
            if (rule.operator == '>' and ref > rule.threshold) or (rule.operator == '<' and ref < rule.threshold):
                current_rule = rule.target
                break

    return current_rule == 'A'


workflows = {}
for line in sys.stdin:
    if not line.strip():
        break

    name, rules = re.match(r'^(?P<name>\w+)\{(?P<rules>.*?)}$', line.strip()).groups()
    workflows[name] = []
    for rule in rules.split(','):
        if match := re.match(r'^(?P<category>\w+)(?P<operator>[<>])(?P<threshold>\w+):(?P<target>\w+)$', rule):
            workflows[name].append(Rule(
                category=match.group('category'),
                operator=match.group('operator'),
                threshold=int(match.group('threshold')),
                target=match.group('target')
            ))
        else:
            workflows[name].append(rule)

parts = []
for line in sys.stdin:
    match = re.match(r'^\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$', line.strip())
    parts.append(Part(
        x=int(match.group('x')),
        m=int(match.group('m')),
        a=int(match.group('a')),
        s=int(match.group('s'))
    ))

print(sum(part.rating for part in parts if is_accepted(part)))
