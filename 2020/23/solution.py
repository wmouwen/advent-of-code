import collections
import sys


def crab_move(deque):
    current = deque[0]
    label_max = len(deque)

    # Pick 3 cups
    deque.rotate(-1)
    picks = [deque.popleft() for _ in range(3)]

    # Determine destination
    destination = current
    while True:
        destination = destination - 1 if destination > 1 else label_max
        if destination not in picks:
            break

    # Reinsert picked cups
    deque.rotate(-1 * (deque.index(destination) + 1))
    deque.extendleft(reversed(picks))

    # Move next target to front of deque
    deque.rotate(-1 * (deque.index(current) + 1))

    return deque


def main():
    initial_list = list(map(int, list(sys.stdin.readline().strip())))

    deque = collections.deque(initial_list)
    for _ in range(100):
        deque = crab_move(deque)

    deque.rotate(-1 * (deque.index(1)))
    print(''.join(map(str, list(deque)[1:])))


if __name__ == "__main__":
    main()
