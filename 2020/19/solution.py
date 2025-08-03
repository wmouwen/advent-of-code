import re
import sys

Rules = dict[str, str | list[list[str]]]


def get_rules() -> Rules:
    rules = {}

    for line in sys.stdin:
        if line.strip() == '':
            break

        nr, rule = re.match(r'^(\d+): (.*?)$', line).groups()

        if rule.startswith('"'):
            rules[nr] = rule[1]
        else:
            rules[nr] = [subrule.split(' ') for subrule in rule.split(' | ')]

    return rules


def solve(message: str, rules: Rules, current: str) -> list[str]:
    rule = rules[current]

    if isinstance(rule, str):
        return [message[len(rule) :]] if message[: len(rule)] == rule else []

    all_options = []

    for rule_part in rule:
        options = [message]

        for next_rule in rule_part:
            next_options = []
            for option in options:
                next_options.extend(solve(option, rules, next_rule))

            options = next_options

        all_options.extend(options)

    return all_options


def main():
    rules = get_rules()
    messages = [line.strip() for line in sys.stdin]

    print(sum(1 if '' in solve(message, rules, '0') else 0 for message in messages))

    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]

    print(sum(1 if '' in solve(message, rules, '0') else 0 for message in messages))


if __name__ == '__main__':
    main()
