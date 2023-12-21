import sys

adapters = [int(line) for line in sys.stdin]
adapters += [0, max(adapters) + 3]
adapters.sort()

differences = [0] * 4
flows = [1] + [0] * (len(adapters) - 1)

for i in range(0, len(adapters) - 1):
    differences[adapters[i + 1] - adapters[i]] += 1

    for j in range(i + 1, min(i + 4, len(flows))):
        flows[j] += flows[i] if adapters[j] - adapters[i] <= 3 else 0

print(differences[1] * differences[3])
print(flows[-1])
