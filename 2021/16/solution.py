import math
import sys
from enum import Enum
from typing import Self


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


class Packet:
    def __init__(self, version: int, type: PacketType):
        self.version: int = version
        self.type: PacketType = type
        self.length: int | None = None
        self.literal_value: int | None = None
        self.subpackets: list[Packet] = []

    @classmethod
    def from_str(cls, message: str) -> Self:
        packet = cls(version=int(message[:3], 2), type=PacketType(int(message[3:6], 2)))
        packet.length = 6

        match packet.type:
            case PacketType.LITERAL:
                value = ''

                for pointer in range(6, len(message), 5):
                    value += message[pointer + 1 : pointer + 5]

                    packet.length += 5
                    if message[pointer] == '0':
                        break

                packet.literal_value = int(value, 2)

            case _:
                length_type = int(message[6], 2)
                packet.length += 1

                match length_type:
                    case 0:
                        length_subpackets = int(message[7:22], 2)
                        packet.length += 15

                        length_processed = 0
                        while length_processed < length_subpackets:
                            packet.subpackets.append(
                                cls.from_str(message[22 + length_processed :])
                            )
                            packet.length += packet.subpackets[-1].length
                            length_processed += packet.subpackets[-1].length

                    case 1:
                        count_subpackets = int(message[7:18], 2)
                        packet.length += 11

                        length_processed = 0
                        for _ in range(count_subpackets):
                            packet.subpackets.append(
                                cls.from_str(message[18 + length_processed :])
                            )
                            packet.length += packet.subpackets[-1].length
                            length_processed += packet.subpackets[-1].length

                    case _:
                        raise RuntimeError('Invalid packet type')

        return packet

    @property
    def sum_versions(self) -> int:
        return self.version + sum(
            subpacket.sum_versions for subpacket in self.subpackets
        )

    @property
    def value(self) -> int:
        match self.type:
            case PacketType.SUM:
                return sum(subpacket.value for subpacket in self.subpackets)

            case PacketType.PRODUCT:
                return math.prod(subpacket.value for subpacket in self.subpackets)

            case PacketType.MINIMUM:
                return min(subpacket.value for subpacket in self.subpackets)

            case PacketType.MAXIMUM:
                return max(subpacket.value for subpacket in self.subpackets)

            case PacketType.LITERAL:
                return self.literal_value

            case PacketType.GREATER_THAN:
                return int(self.subpackets[0].value > self.subpackets[1].value)

            case PacketType.LESS_THAN:
                return int(self.subpackets[0].value < self.subpackets[1].value)

            case PacketType.EQUAL_TO:
                return int(self.subpackets[0].value == self.subpackets[1].value)


def main():
    message_hexadecimal = sys.stdin.readline().strip()
    message_binary = '{input:{width}b}'.format(
        input=int(message_hexadecimal, 16), width=len(message_hexadecimal) * 4
    )

    packet = Packet.from_str(message_binary)
    print(packet.sum_versions)
    print(packet.value)


if __name__ == '__main__':
    main()
