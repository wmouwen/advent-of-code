import re
import sys


def get_value(nodes, key):
    if key not in nodes:
        raise Exception('Key not found')

    if isinstance(nodes[key], int):
        return nodes[key]

    left, op, right = nodes[key]

    if op == 'AND':
        return get_value(nodes, left) & get_value(nodes, right)
    if op == 'XOR':
        return get_value(nodes, left) ^ get_value(nodes, right)
    if op == 'OR':
        return get_value(nodes, left) | get_value(nodes, right)

    raise Exception('Unknown operator')


def main():
    nodes: dict[str, int | tuple[str, str, str]] = dict()

    for line in sys.stdin:
        match = re.match(r'([0-9a-z]{3}): (\d)', line.strip())
        if not match:
            break

        key, value = match.groups()
        nodes[key] = int(value)

    for line in sys.stdin:
        match = re.match(
            r'([0-9a-z]{3}) (AND|XOR|OR) ([0-9a-z]{3}) -> ([0-9a-z]{3})', line.strip()
        )
        if not match:
            break

        left, op, right, key = match.groups()
        nodes[key] = (left, op, right)

    z_dict = {
        int(key[1:]): get_value(nodes, key)
        for key in nodes.keys()
        if key.startswith('z')
    }

    print(sum(value << key for key, value in z_dict.items()))


if __name__ == '__main__':
    main()
