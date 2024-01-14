import re
import sys


class Food:
    def __init__(self, ingredients: set[str], allergens: set[str]):
        self.ingredients = ingredients
        self.allergens = allergens


def main():
    foods: list[Food] = []
    ingredients: set = set()
    allergens: dict = {}

    for line in sys.stdin:
        match = re.match(r'([\w\s]+) \(contains ([\w\s,]+)\)', line.strip())

        food = Food(
            ingredients=set(match.group(1).split(' ')),
            allergens=set(match.group(2).split(', '))
        )
        foods.append(food)

        ingredients |= food.ingredients
        for allergen in food.allergens:
            if allergen in allergens:
                allergens[allergen] &= food.ingredients
            else:
                allergens[allergen] = food.ingredients.copy()

    allergen_free = ingredients
    for candidates in allergens.values():
        allergen_free -= candidates

    print(sum(len(allergen_free & food.ingredients) for food in foods))

    allergen_known = set()
    while any(len(candidates) > 1 for candidates in allergens.values()):
        for allergen in sorted(allergens, key=lambda a: len(allergens[a])):
            if len(allergens[allergen]) > 1:
                allergens[allergen] -= allergen_known
            assert len(allergens[allergen]) > 0
            if len(allergens[allergen]) == 1:
                allergen_known |= allergens[allergen]

    print(','.join(next(iter(allergens[allergen])) for allergen in sorted(allergens.keys())))


if __name__ == '__main__':
    main()
