import sys


def main():
    occurrences = 0
    total = 0

    for line in sys.stdin:
        digits, code = (
            [''.join(sorted(digit)) for digit in parts.split()]
            for parts in line.split('|')
        )

        mapping = {
            1: next(digit for digit in digits if len(digit) == 2),
            4: next(digit for digit in digits if len(digit) == 4),
            7: next(digit for digit in digits if len(digit) == 3),
            8: next(digit for digit in digits if len(digit) == 7),
        }

        occurrences += sum(1 for digit in code if digit in mapping.values())

        mapping.update(
            {
                3: next(
                    digit
                    for digit in digits
                    if len(digit) == 5 and all(char in digit for char in mapping[1])
                ),
                6: next(
                    digit
                    for digit in digits
                    if len(digit) == 6 and any(char not in digit for char in mapping[1])
                ),
                9: next(
                    digit
                    for digit in digits
                    if len(digit) == 6 and all(char in digit for char in mapping[4])
                ),
            }
        )
        mapping.update(
            {
                5: next(
                    digit
                    for digit in digits
                    if len(digit) == 5
                    and digit not in mapping.values()
                    and sum([char in digit for char in mapping[4]]) == 3
                ),
            }
        )
        mapping.update(
            {
                0: next(
                    digit
                    for digit in digits
                    if len(digit) == 6 and digit not in mapping.values()
                ),
                2: next(
                    digit
                    for digit in digits
                    if len(digit) == 5 and digit not in mapping.values()
                ),
            }
        )

        reverse_mapping = {value: key for key, value in mapping.items()}
        total += int(
            ''.join(str(reverse_mapping[digit]) for i, digit in enumerate(code))
        )

    print(occurrences)
    print(total)


if __name__ == '__main__':
    main()
