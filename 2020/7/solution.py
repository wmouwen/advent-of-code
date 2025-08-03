import collections
import re
import sys

from typing import Dict


def reachable_bags(tree: Dict[str, dict], current_node: str) -> collections.Counter:
    counter = collections.Counter()

    for child_node, weight in tree[current_node].items():
        counter[child_node] += weight

        if child_node not in tree:
            continue

        for reachable, subweight in reachable_bags(tree, child_node).items():
            counter[reachable] += weight * subweight

    return counter


tree_outwards = {}
tree_inwards = {}

for line in sys.stdin:
    outer_bag = re.search(r'^(.*?) bags contain', line).group(1)
    tree_inwards[outer_bag] = {}

    if re.search(r'contain no other bags\.', line):
        continue

    for link in re.findall(r'(\d+) (.*?) bag', line):
        inner_bag = link[1]
        if inner_bag not in tree_outwards:
            tree_outwards[inner_bag] = {}

        tree_outwards[inner_bag][outer_bag] = int(link[0])
        tree_inwards[outer_bag][inner_bag] = int(link[0])

print(len(reachable_bags(tree_outwards, 'shiny gold')))
print(sum(reachable_bags(tree_inwards, 'shiny gold').values()))
