import re
import sys

Rules = dict[str, str | list[str]]


def compile_regex(rules: Rules, nr: str) -> str:
    if isinstance(rules[nr], str):
        return rules[nr]

    subregex = '|'.join([''.join(compile_regex(rules, item) for item in subrule) for subrule in rules[nr]])

    return f'({subregex})'


def main():
    rules: Rules = {}

    for line in sys.stdin:
        if line.strip() == '':
            break

        nr, rule = re.match(r'^(\d+): (.*?)$', line).groups()

        if rule.startswith('"'):
            rules[nr] = rule[1]
        else:
            rules[nr] = [subrule.split(' ') for subrule in rule.split(' | ')]

    regex = '^' + compile_regex(rules, '0') + '$'

    valid = 0
    for line in sys.stdin:
        if re.match(regex, line.strip()):
            valid += 1
    print(valid)

    # TODO Convert to state machine for part 2, or apply some regex trickery specifically for rules 8 and 11


if __name__ == '__main__':
    main()
