import sys


def main():
    earliest_departure = int(sys.stdin.readline())
    busses = [
        int(bus) if bus != 'x' else None
        for bus in sys.stdin.readline().strip().split(',')
    ]

    earliest_departure_bus = None
    earliest_departure_delay = sys.maxsize

    for bus in busses:
        if bus is None:
            continue

        delay = int(bus) * (((earliest_departure - 1) // int(bus)) + 1) - earliest_departure

        if delay < earliest_departure_delay:
            earliest_departure_bus = bus
            earliest_departure_delay = delay

    print(earliest_departure_bus * earliest_departure_delay)


if __name__ == '__main__':
    main()
