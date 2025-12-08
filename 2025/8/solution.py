import sys
from itertools import combinations
from math import prod
from typing import Self, NamedTuple


class Box(NamedTuple):
    x: int
    y: int
    z: int

    def dist(self, o: Self) -> int:
        return (self.x - o.x) ** 2 + (self.y - o.y) ** 2 + (self.z - o.z) ** 2


def main():
    boxes = [Box(*map(int, line.strip().split(','))) for line in sys.stdin]
    edges = sorted((a.dist(b), a, b) for a, b in combinations(boxes, 2))

    circuits = [{box} for box in boxes]

    i_source, i_target = int, int
    for i_edge, (_, source, target) in enumerate(edges):
        for i_circuit in range(len(circuits)):
            if source in circuits[i_circuit]:
                i_source = i_circuit
            if target in circuits[i_circuit]:
                i_target = i_circuit

        if i_source != i_target:
            circuits[i_source].update(circuits[i_target])
            circuits.pop(i_target)

            if len(circuits) == 1:
                print(source.x * target.x)
                break

        if i_edge + 1 == (10 if len(boxes) < 100 else 1000):
            lengths = sorted((len(circuit) for circuit in circuits), reverse=True)
            print(prod(lengths[:3]))


if __name__ == '__main__':
    main()
