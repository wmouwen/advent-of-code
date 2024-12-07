import sys

type Equation = tuple[int, list[int]]


def calibrate(equations: list[Equation], with_concatenation: bool) -> int:
    calibration_result = 0

    for (target, numbers) in equations:
        outcomes = [numbers[0]]

        for i in range(1, len(numbers)):
            intermediates = []

            for outcome in outcomes:
                if outcome > target:
                    continue

                intermediates.append(outcome + numbers[i])
                intermediates.append(outcome * numbers[i])

                if with_concatenation:
                    intermediates.append(int(str(outcome) + str(numbers[i])))

            outcomes = intermediates

        if target in outcomes:
            calibration_result += target

    return calibration_result


def main():
    equations: list[Equation] = []

    for line in sys.stdin:
        line_parts = line.strip().split(': ')
        equations.append((
            int(line_parts[0]),
            list(map(int, line_parts[1].split(' ')))
        ))

    print(calibrate(equations, False))
    print(calibrate(equations, True))


if __name__ == '__main__':
    main()
