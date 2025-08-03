import itertools
import sys


def has_combination(numbers: list, target: int) -> bool:
    for combination in itertools.combinations(numbers, 2):
        if sum(combination) == target:
            return True
    return False


def first_invalid_number(numbers: list, set_size: int = 25) -> int:
    for i in range(set_size, len(numbers)):
        candidates = numbers[i - set_size : i]
        if has_combination(candidates, numbers[i]):
            continue

        return numbers[i]

    raise Exception


def subset_for_sum(numbers: list, target: int) -> list:
    for low in range(len(numbers) - 1):
        for high in range(low + 2, len(numbers)):
            subset = numbers[low:high]
            if sum(subset) > target:
                break
            elif sum(subset) == target:
                return subset

    raise Exception


numbers = [int(line) for line in sys.stdin]

target = first_invalid_number(numbers)
print(target)

subset = subset_for_sum(numbers, target)
print(min(subset) + max(subset))
