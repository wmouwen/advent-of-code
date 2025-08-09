import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../intcode'))
)
from intcode import IntcodeComputer


Packet = tuple[int, int]


class NetworkInterfaceController(IntcodeComputer):
    def __init__(self, identifier: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.input_buffer: list[int] = [identifier]
        self.input_callback = (
            lambda: self.input_buffer.pop(0) if self.input_buffer else None
        )

        self.output_buffer: list[int] = []
        self.output_callback = lambda value: self.output_buffer.append(value)

    def run(self):
        self.input_buffer.append(-1)
        super().run()

    def queue_packet(self, packet: Packet) -> None:
        self.input_buffer.extend(packet)

    def get_packets(self) -> list[tuple[int, Packet]]:
        assert len(self.output_buffer) % 3 == 0
        packets: list[tuple[int, Packet]] = [
            (
                self.output_buffer[i],
                (self.output_buffer[i + 1], self.output_buffer[i + 2]),
            )
            for i in range(0, len(self.output_buffer), 3)
        ]
        self.output_buffer = []
        return packets


def main():
    program = list(map(int, sys.stdin.readline().strip().split(',')))
    nics = tuple(
        NetworkInterfaceController(program=program, identifier=identifier)
        for identifier in range(50)
    )

    first_packet_to_nat = None
    last_packet_to_nat = None
    redelivered_y_values = set()

    while True:
        idle = True
        identifier = 0
        while True:
            nics[identifier].run()

            for destination, packet in nics[identifier].get_packets():
                idle = False

                if destination == 255:
                    last_packet_to_nat = packet
                    if first_packet_to_nat is None:
                        first_packet_to_nat = packet
                else:
                    nics[destination].queue_packet(packet)

            identifier = (identifier + 1) % len(nics)
            if identifier == 0:
                if idle:
                    break
                idle = True

        if last_packet_to_nat is None:
            raise Exception

        if last_packet_to_nat[1] in redelivered_y_values:
            print(first_packet_to_nat[1])
            print(last_packet_to_nat[1])
            break

        redelivered_y_values.add(last_packet_to_nat[1])
        nics[0].queue_packet(last_packet_to_nat)


if __name__ == '__main__':
    main()
