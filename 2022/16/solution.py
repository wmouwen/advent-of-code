import re
import sys
from itertools import combinations
from math import ceil
from typing import NamedTuple


class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnels: dict[str, int]


class Network:
    def __init__(self):
        self.valves: dict[str, Valve] = {}

    def remove_empty_nodes(self, exceptions: list[str]):
        valves = list(self.valves.values())
        for valve in valves:
            if valve.flow_rate > 0 or valve.name in exceptions:
                continue

            for a in valve.tunnels.keys():
                for b in valve.tunnels.keys():
                    if b != a:
                        self.valves[a].tunnels[b] = valve.tunnels[a] + valve.tunnels[b]
                self.valves[a].tunnels.pop(valve.name)

            self.valves.pop(valve.name)

    def add_missing_edges(self):
        while any(
            len(valve.tunnels) + 1 < len(self.valves) for valve in self.valves.values()
        ):
            for valve in self.valves.values():
                tunnels = list(valve.tunnels.items())
                for a, a_dist in tunnels:
                    for b, b_dist in self.valves[a].tunnels.items():
                        if valve.name == b:
                            continue

                        if b in valve.tunnels and valve.tunnels[b] < a_dist + b_dist:
                            continue

                        valve.tunnels[b] = a_dist + b_dist


def pressure_release(
    network: Network,
    location: str,
    time_remaining: int,
    open_valves: set[str],
    released_pressure: int = 0,
) -> int:
    max_pressure = released_pressure

    for new_location, distance in network.valves[location].tunnels.items():
        if new_location in open_valves:
            continue

        new_time_remaining = time_remaining - distance - 1
        if new_time_remaining < 0:
            continue

        max_pressure = max(
            max_pressure,
            pressure_release(
                network=network,
                location=new_location,
                time_remaining=new_time_remaining,
                open_valves=open_valves.union({location}),
                released_pressure=released_pressure
                + network.valves[new_location].flow_rate * new_time_remaining,
            ),
        )

    return max_pressure


def solo_walk(network, start):
    return pressure_release(
        network, location=start, time_remaining=30, open_valves={start}
    )


def duo_walk(network, start):
    targets = set(
        valve.name for valve in network.valves.values() if valve.name != start
    )
    max_pressure = 0

    for size in range(ceil(len(targets) / 2) + 1):
        for combination in combinations(targets, size):
            player = pressure_release(
                network,
                location=start,
                time_remaining=26,
                open_valves=set(combination).union({start}),
            )
            elephant = pressure_release(
                network,
                location=start,
                time_remaining=26,
                open_valves=set(targets - set(combination)).union({start}),
            )

            max_pressure = max(max_pressure, player + elephant)

    return max_pressure


def main():
    network = Network()
    start = 'AA'

    for line in sys.stdin:
        if match := re.match(
            r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)$',
            line.strip(),
        ):
            valve = Valve(
                name=match.group(1),
                flow_rate=int(match.group(2)),
                tunnels={key: 1 for key in match.group(3).split(', ')},
            )
            network.valves[valve.name] = valve
        else:
            raise Exception('Failed to read line: ' + line.strip())

    if network.valves[start].flow_rate != 0:
        raise Exception('Unhandled edge case')

    network.remove_empty_nodes(exceptions=[start])
    network.add_missing_edges()

    print(solo_walk(network, start))
    print(duo_walk(network, start))


if __name__ == '__main__':
    main()
