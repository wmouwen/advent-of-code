import re
import sys
from copy import deepcopy
from enum import Enum
from typing import Self


class Party(Enum):
    IMMUNE_SYSTEM = 'immune_system'
    INFECTION = 'infection'


class Group:
    @classmethod
    def from_string(cls, party: Party, line: str) -> Self:
        match = re.match(
            r'(\d+) units each with (\d+) hit points (\(.+\))?\s?with an attack that does (\d+) (\w+) damage at initiative (\d+)',
            line.strip()
        )

        weaknesses, immunities = [], []
        for power, types in re.findall('(weak|immune) to ([^;)]*)', match.group(3) or ''):
            (weaknesses if power == 'weak' else immunities).extend(types.split(', '))

        return cls(
            party=party, units=int(match.group(1)), hit_points=int(match.group(2)),
            initiative=int(match.group(6)), attack_damage=int(match.group(4)), attack_type=match.group(5),
            weaknesses=weaknesses, immunities=immunities,
        )

    def __init__(
            self, party: Party, units: int, hit_points: int,
            initiative: int, attack_damage: int, attack_type: str,
            weaknesses: list[str], immunities: list[str]
    ):
        # State
        self.party = party
        self.units = units
        self.hit_points = hit_points

        # Attack
        self.initiative = initiative
        self.attack_damage = attack_damage
        self.attack_type = attack_type

        # Defense
        self.weaknesses = weaknesses
        self.immunities = immunities

    @property
    def effective_power(self) -> int:
        return self.units * self.attack_damage

    def power_against(self, target: Self) -> int:
        if self.attack_type in target.immunities: return 0
        if self.attack_type in target.weaknesses: return 2 * self.effective_power
        return self.effective_power

    def __repr__(self):
        return f'Group({self.party}, units={self.units}, hit_points={self.hit_points}, attack_type={self.attack_type}, immunities=[{', '.join(self.immunities)}])'


def select_targets(groups: list[Group]) -> dict[Group, Group]:
    targets = dict()

    for attacker in sorted(groups, key=lambda group: (group.effective_power, group.initiative), reverse=True):
        defenders = [
            defender
            for defender in groups
            if (attacker.party != defender.party and
                attacker.attack_type not in defender.immunities and
                defender not in targets.values())
        ]

        if not defenders:
            continue

        targets[attacker] = sorted(
            defenders,
            key=lambda defender: (attacker.power_against(defender), defender.effective_power, defender.initiative),
            reverse=True
        )[0]

    return targets


def fight(groups: list[Group]) -> list[Group]:
    targets = select_targets(groups)

    for attacker in sorted(groups, key=lambda group: group.initiative, reverse=True):
        if attacker.units <= 0 or attacker not in targets.keys():
            continue

        target = targets[attacker]
        target.units -= attacker.power_against(target) // target.hit_points

    return list(filter(lambda group: group.units > 0, groups))


def combat(groups: list[Group], boost: int = 0) -> list[Group]:
    groups = deepcopy(groups)

    for group in groups:
        if group.party == Party.IMMUNE_SYSTEM:
            group.attack_damage += boost

    prev_total_units = sum(group.units for group in groups)
    while len(set(group.party for group in groups)) > 1:
        groups = fight(groups)

        # Infinite loop preventions
        total_units = sum(group.units for group in groups)
        if prev_total_units == total_units: break
        prev_total_units = total_units

    return groups


def main():
    groups: list[Group] = []

    sys.stdin.readline()
    for line in sys.stdin:
        if line.strip() == '': break
        groups.append(Group.from_string(Party.IMMUNE_SYSTEM, line))

    sys.stdin.readline()
    for line in sys.stdin:
        if line.strip() == '': break
        groups.append(Group.from_string(Party.INFECTION, line))

    survivors = combat(groups)
    print(sum(survivor.units for survivor in survivors))

    boost_min, boost_max = 0, 1 << 31
    while boost_min < boost_max:
        boost = boost_min + (boost_max - boost_min) // 2
        survivors = combat(groups, boost=boost)

        if any(survivor.party == Party.INFECTION for survivor in survivors):
            boost_min = boost + 1
        else:
            boost_max = boost

    survivors = combat(groups, boost=boost_min)
    assert not any(survivor.party == Party.INFECTION for survivor in survivors)
    print(sum(survivor.units for survivor in survivors))


if __name__ == '__main__':
    main()
