import math
import re
import sys
from queue import Queue
from typing import NamedTuple


class Rule(NamedTuple):
    category: str
    operator: str
    threshold: int
    target: str


def is_accepted(part: dict[str, int]) -> bool:
    current_rule = 'in'

    while current_rule not in ['A', 'R']:
        for rule in workflows[current_rule]:
            if isinstance(rule, str):
                current_rule = rule
                break

            assert isinstance(rule, Rule)
            ref = part[rule.category]
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

sum_ratings = 0
for line in sys.stdin:
    match = re.match(r'^\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$', line.strip())
    part = {'x': int(match.group('x')),
            'm': int(match.group('m')),
            'a': int(match.group('a')),
            's': int(match.group('s'))}

    if is_accepted(part):
        sum_ratings += sum(part.values())
print(sum_ratings)

combinations = 0
queue = Queue()
queue.put(({'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}, 'in'))

while not queue.empty():
    part, name = queue.get()

    if name == 'A':
        combinations += math.prod(map(lambda cat: cat[1] - cat[0] + 1, part.values()))
    elif name != 'R':
        for rule in workflows[name]:
            if isinstance(rule, Rule):
                if rule.operator == '<':
                    if rule.threshold <= part[rule.category][0]:
                        # Condition not met
                        continue
                    if rule.threshold <= part[rule.category][1]:
                        # Condition partially met
                        new_part = part.copy()
                        new_part[rule.category] = (part[rule.category][0], rule.threshold - 1)
                        queue.put((new_part, rule.target))
                        part[rule.category] = (rule.threshold, part[rule.category][1])
                        continue
                    # Condition fully met
                    queue.put((part, rule.target))
                    break
                if rule.operator == '>':
                    if rule.threshold >= part[rule.category][1]:
                        # Condition not met
                        continue
                    if rule.threshold >= part[rule.category][0]:
                        # Condition partially met
                        new_part = part.copy()
                        new_part[rule.category] = (rule.threshold + 1, part[rule.category][1])
                        queue.put((new_part, rule.target))
                        part[rule.category] = (part[rule.category][0], rule.threshold)
                        continue
                    # Condition fully met
                    queue.put((part, rule.target))
                    break

            queue.put((part, rule))

print(combinations)
