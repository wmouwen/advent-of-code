import re
import sys
from typing import NamedTuple


class Coord(NamedTuple):
    y: int
    x: int

    def above(self):
        return Coord(y=self.y - 1, x=self.x)

    def below(self):
        return Coord(y=self.y + 1, x=self.x)

    def left(self):
        return Coord(y=self.y, x=self.x - 1)

    def right(self):
        return Coord(y=self.y, x=self.x + 1)


def main():
    walls = list()
    water = list([Coord(y=0, x=500)])
    water_still = list()

    # Input parsing
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue

        if matches := re.match(r'x=(\d+), y=(\d+)\.\.(\d+)$', line):
            for y in range(int(matches[2]), int(matches[3]) + 1):
                walls.append(Coord(y=y, x=int(matches[1])))
        elif matches := re.match(r'y=(\d+), x=(\d+)\.\.(\d+)$', line):
            for x in range(int(matches[2]), int(matches[3]) + 1):
                walls.append(Coord(y=int(matches[1]), x=x))

    x_min, x_max = min(wall.x for wall in walls) - 1, max(wall.x for wall in walls) + 1
    y_min, y_max = min(wall.y for wall in walls), max(wall.y for wall in walls)

    while True:
        # Find free endpoint
        endpoints = [
            flow
            for flow in water
            if flow.below() not in walls
               and flow.below() not in water
               and (flow.below() not in water_still
                    or (flow.left() not in walls and flow.left() not in water)
                    or (flow.right() not in walls and flow.right() not in water))
               and flow.y < y_max
        ]
        if len(endpoints) == 0:
            break

        current_flow = endpoints[0]
        print(current_flow)
        next_flow = current_flow.below()

        # Move downwards
        while next_flow not in walls and next_flow not in water and next_flow not in water_still and next_flow.y <= y_max:
            water.append(next_flow)
            current_flow = next_flow
            next_flow = next_flow.below()

        # Early break when bottom has been reached
        if current_flow.y >= y_max:
            continue

        # Fill bucket, repetitive sideways search
        while True:
            flow_left = current_flow.left()
            while flow_left not in walls:
                water.append(flow_left)
                if flow_left.below() not in walls and flow_left.below() not in water_still:
                    break
                flow_left = flow_left.left()

            flow_right = current_flow.right()
            while flow_right not in walls:
                water.append(flow_right)
                if flow_right.below() not in walls and flow_right.below() not in water_still:
                    break
                flow_right = flow_right.right()

            # Convert to still water if trapped
            if flow_left not in walls or flow_right not in walls:
                break

            flow_left = current_flow
            while flow_left in water:
                water.remove(flow_left)
                water_still.append(flow_left)
                flow_left = flow_left.left()

            flow_right = current_flow.right()
            while flow_right in water:
                water.remove(flow_right)
                water_still.append(flow_right)
                flow_right = flow_right.right()

            # If still water, repeat sideways search one row up.
            if current_flow.above() not in water:
                break
            current_flow = current_flow.above()

    print(sum(1
              for y in range(y_min, y_max + 1)
              for x in range(x_min, x_max + 1)
              if Coord(y=y, x=x) in water
              or Coord(y=y, x=x) in water_still
              ))

    # Debugging
    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            print(
                '+' if y == 0 and x == 500
                else '|' if Coord(y=y, x=x) in water
                else '~' if Coord(y=y, x=x) in water_still
                else '#' if Coord(y=y, x=x) in walls
                else '.',
                end='')
        print()


if __name__ == '__main__':
    main()
