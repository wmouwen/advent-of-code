import re
import sys
from dataclasses import dataclass
from functools import cache
from math import prod
from typing import Self


@dataclass(frozen=True)
class Inventory:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other: Self):
        return Inventory(
            ore=self.ore + other.ore,
            clay=self.clay + other.clay,
            obsidian=self.obsidian + other.obsidian,
            geode=self.geode + other.geode,
        )

    def __sub__(self, other: Self):
        return Inventory(
            ore=self.ore - other.ore,
            clay=self.clay - other.clay,
            obsidian=self.obsidian - other.obsidian,
            geode=self.geode - other.geode,
        )

    def can_afford(self, costs: Self) -> bool:
        return (
            costs.ore <= self.ore
            and costs.clay <= self.clay
            and costs.obsidian <= self.obsidian
            and costs.geode <= self.geode
        )


@dataclass(frozen=True)
class Blueprint:
    id: int

    ore: Inventory
    clay: Inventory
    obsidian: Inventory
    geode: Inventory

    @property
    def max_ore(self):
        return max(self.ore.ore, self.clay.ore, self.obsidian.ore, self.geode.ore)


@cache
def max_geodes(
    blueprint: Blueprint,
    inventory: Inventory,
    robots: Inventory,
    minutes: int,
    ignore: tuple = (),
):
    if minutes == 0:
        return inventory.geode

    best = inventory.geode + robots.geode * minutes

    if inventory.can_afford(blueprint.geode) and minutes > 1 and 'geode' not in ignore:
        best = max(
            best,
            max_geodes(
                blueprint=blueprint,
                inventory=inventory + robots - blueprint.geode,
                robots=robots + Inventory(geode=1),
                minutes=minutes - 1,
                ignore=tuple(),
            ),
        )

    if (
        inventory.can_afford(blueprint.obsidian)
        and robots.obsidian < blueprint.geode.obsidian
        and minutes > 2
        and 'obsidian' not in ignore
    ):
        best = max(
            best,
            max_geodes(
                blueprint=blueprint,
                inventory=inventory + robots - blueprint.obsidian,
                robots=robots + Inventory(obsidian=1),
                minutes=minutes - 1,
                ignore=tuple(),
            ),
        )

    if (
        inventory.can_afford(blueprint.clay)
        and robots.clay < blueprint.obsidian.clay
        and minutes > 2
        and 'clay' not in ignore
    ):
        best = max(
            best,
            max_geodes(
                blueprint=blueprint,
                inventory=inventory + robots - blueprint.clay,
                robots=robots + Inventory(clay=1),
                minutes=minutes - 1,
                ignore=tuple(),
            ),
        )

    if (
        inventory.can_afford(blueprint.ore)
        and robots.ore < blueprint.max_ore
        and minutes > 2
        and 'ore' not in ignore
    ):
        best = max(
            best,
            max_geodes(
                blueprint=blueprint,
                inventory=inventory + robots - blueprint.ore,
                robots=robots + Inventory(ore=1),
                minutes=minutes - 1,
                ignore=tuple(),
            ),
        )

    if inventory.ore <= blueprint.max_ore + 1 and minutes > 2:
        best = max(
            best,
            max_geodes(
                blueprint=blueprint,
                inventory=inventory + robots,
                robots=robots,
                minutes=minutes - 1,
                ignore=tuple(
                    [
                        'ore' if inventory.can_afford(blueprint.ore) else None,
                        'clay' if inventory.can_afford(blueprint.clay) else None,
                        'obsidian'
                        if inventory.can_afford(blueprint.obsidian)
                        else None,
                        'geode' if inventory.can_afford(blueprint.geode) else None,
                    ]
                ),
            ),
        )

    return best


def main():
    blueprints = []
    for line in sys.stdin:
        if not line.strip():
            break

        costs = re.findall(r'\d+', line.strip())

        blueprints.append(
            Blueprint(
                id=int(costs[0]),
                ore=Inventory(ore=int(costs[1])),
                clay=Inventory(ore=int(costs[2])),
                obsidian=Inventory(ore=int(costs[3]), clay=int(costs[4])),
                geode=Inventory(ore=int(costs[5]), obsidian=int(costs[6])),
            )
        )

    print(
        sum(
            blueprint.id
            * max_geodes(
                blueprint, inventory=Inventory(), robots=Inventory(ore=1), minutes=24
            )
            for blueprint in blueprints
        )
    )

    print(
        prod(
            max_geodes(
                blueprint, inventory=Inventory(), robots=Inventory(ore=1), minutes=32
            )
            for blueprint in blueprints
            if blueprint.id <= 3
        )
    )


if __name__ == '__main__':
    main()
