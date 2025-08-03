import math
import sys
from typing import Self


class Reaction:
    def __init__(self, name: str, output_quantity: int):
        self.name = name
        self.output_quantity = output_quantity
        self.ingredients = {}

    def ore_required(
        self,
        amount_required: int,
        reactions: dict[str, Self],
        remainders: dict[str, int] = None,
    ) -> int:
        if remainders is None:
            remainders = {}
        if self.name not in remainders:
            remainders[self.name] = 0

        if amount_required <= remainders[self.name]:
            remainders[self.name] -= amount_required
            return 0

        amount_required -= remainders[self.name]
        reaction_multiplier = math.ceil(amount_required / self.output_quantity)
        remainders[self.name] = (
            reaction_multiplier * self.output_quantity - amount_required
        )

        return sum(
            reaction_multiplier * self.ingredients[ingredient_name]
            if ingredient_name == 'ORE'
            else reactions[ingredient_name].ore_required(
                amount_required=reaction_multiplier * self.ingredients[ingredient_name],
                reactions=reactions,
                remainders=remainders,
            )
            for ingredient_name in self.ingredients
        )


def main():
    reactions = {}

    for line in sys.stdin:
        ingredients, output = line.strip().split(' => ')

        output_quantity, output_name = output.split(' ')
        reaction = Reaction(name=output_name, output_quantity=int(output_quantity))

        for ingredient in ingredients.split(', '):
            ingredient_quantity, ingredient_name = ingredient.split(' ')
            reaction.ingredients[ingredient_name] = int(ingredient_quantity)

        reactions[reaction.name] = reaction

    ore_for_single_fuel = reactions['FUEL'].ore_required(
        amount_required=1, reactions=reactions
    )
    print(ore_for_single_fuel)

    goal = 1000000000000
    left = goal // ore_for_single_fuel
    right = left * 2

    while left < right - 1:
        mid = (left + right) // 2
        if (
            reactions['FUEL'].ore_required(amount_required=mid, reactions=reactions)
            <= goal
        ):
            left = mid
        else:
            right = mid

    print(left)


if __name__ == '__main__':
    main()
