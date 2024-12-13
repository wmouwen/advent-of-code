import re
import sys
from collections import defaultdict
from typing import TypedDict

Costs = TypedDict('Costs', {
    'ore': dict[str, int],
    'clay': dict[str, int],
    'obsidian': dict[str, int],
    'geode': dict[str, int]
})


class Blueprint:
    def __init__(self, id: int, costs: Costs):
        self.id = id
        self.costs = costs

    def max_geodes(self, minutes: int, resources=defaultdict(int), robots=defaultdict(int, {'ore': 1})):
        if minutes == 0:
            if resources['geode'] > 1:
                print(resources.items())
            return resources['geode']

        incremented_resources = resources.copy()
        for key, count in robots.items():
            incremented_resources[key] += count

        max_geodes = self.max_geodes(minutes - 1, incremented_resources, robots.copy())

        if resources['ore'] >= self.costs['ore']['ore']:
            next_resources = incremented_resources.copy()
            next_resources['ore'] -= self.costs['ore']['ore']
            next_robots = robots.copy()
            next_robots['ore'] += 1
            max_geodes = max(max_geodes, self.max_geodes(minutes - 1, next_resources, next_robots))

        if resources['ore'] >= self.costs['clay']['ore']:
            next_resources = incremented_resources.copy()
            next_resources['ore'] -= self.costs['clay']['ore']
            next_robots = robots.copy()
            next_robots['clay'] += 1
            max_geodes = max(max_geodes, self.max_geodes(minutes - 1, next_resources, next_robots))

        if resources['ore'] >= self.costs['obsidian']['ore'] and resources['clay'] >= self.costs['obsidian']['clay']:
            next_resources = incremented_resources.copy()
            next_resources['ore'] -= self.costs['obsidian']['ore']
            next_resources['clay'] -= self.costs['obsidian']['clay']
            next_robots = robots.copy()
            next_robots['obsidian'] += 1
            max_geodes = max(max_geodes, self.max_geodes(minutes - 1, next_resources, next_robots))

        if resources['ore'] >= self.costs['geode']['ore'] and resources['obsidian'] >= self.costs['geode']['obsidian']:
            next_resources = incremented_resources.copy()
            next_resources['ore'] -= self.costs['geode']['ore']
            next_resources['obsidian'] -= self.costs['geode']['obsidian']
            next_robots = robots.copy()
            next_robots['geode'] += 1
            max_geodes = max(max_geodes, self.max_geodes(minutes - 1, next_resources, next_robots))

        return max_geodes

    def quality(self, minutes: int):
        max_geodes = self.max_geodes(minutes)
        print(self.id, max_geodes)
        return self.id * max_geodes


def main():
    blueprints = []

    for line in sys.stdin:
        if match := re.match(
                r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.',
                line.strip()
        ):
            blueprints.append(Blueprint(int(match.group(1)), {
                'ore': {
                    'ore': int(match.group(2))
                },
                'clay': {
                    'ore': int(match.group(3))
                },
                'obsidian': {
                    'ore': int(match.group(4)),
                    'clay': int(match.group(5))
                },
                'geode': {
                    'ore': int(match.group(6)),
                    'obsidian': int(match.group(7))
                }
            }))

    print(sum(blueprint.quality(minutes=24) for blueprint in blueprints))


if __name__ == '__main__':
    main()
