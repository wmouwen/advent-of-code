import itertools
import math
import sys


def quantum_entanglement(packages, groups):
    target = sum(packages) // groups

    for size in range(1, len(packages)):
        best = None

        for combi in itertools.combinations(packages, size):
            if sum(combi) == target:
                best = min(math.prod(combi), best if best is not None else sys.maxsize)

        if best is not None:
            return best

    return None


packages = [int(line.strip()) for line in sys.stdin]
packages.sort()

print(quantum_entanglement(packages, 3))
print(quantum_entanglement(packages, 4))
