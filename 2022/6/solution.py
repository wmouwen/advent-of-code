import sys


def find_marker_pos(datastream: str, length: int) -> int:
    for marker in range(length, len(datastream)):
        if len(set(datastream[marker - length:marker])) == length:
            return marker
    raise Exception("No markers found")


datastream = sys.stdin.readline().strip()
print(find_marker_pos(datastream, 4))
print(find_marker_pos(datastream, 14))
