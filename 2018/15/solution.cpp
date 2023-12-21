#include <iostream>
#include <vector>

using namespace std;

int main() {

    vector<string> grid;

    // You scan the area,
    // generating a map of the walls (`#`), open cavern (`.`), and starting position of every Goblin (`G`) and Elf (`E`) (your puzzle input).
    string line;
    while (getline(cin, line)) {
        grid.push_back(line);
    }

    for (int y = 0; y < grid.size(); y++) {
        for (int x = 0; x < grid[y].length(); x++) {
            cout << grid[y][x] << " ";
        }
        cout << endl;
    }

    // Combat proceeds in rounds; in each round, each unit that is still alive takes a turn,
    // resolving all of its actions before the next unit's turn begins. On each unit's turn,

    // it tries to move into range of an enemy (if it isn't already)
    // and then attack (if it is in range).

    // Each unit begins its turn by identifying all possible targets (enemy units).
    // If no targets remain, combat ends.

    // Then, the unit identifies all of the open squares (`.`) that are in range of each target;
    // these are the squares which are adjacent (immediately up, down, left, or right) to any target
    // and which aren't already occupied by a wall or another unit.
    // Alternatively, the unit might already be in range of a target.
    // If the unit is not already in range of a target, and there are no open squares which are in range
    // of a target, the unit ends its turn.

    // If the unit is already in range of a target, it does not move, but continues its turn with an attack.
    // Otherwise, since it is not in range of a target, it moves.

    // To move, the unit first considers the squares that are in range and determines which of those squares
    // it could reach in the fewest steps. A step is a single movement to any adjacent
    // (immediately up, down, left, or right) open (`.`) square.
    // Units cannot move into walls or other units.
    // The unit does this while considering the current positions of units and does not do any prediction
    // about where units will be later. If the unit cannot reach (find an open path to) any of the squares
    // that are in range, it ends its turn. If multiple squares are in range and tied for being reachable
    // in the fewest steps, the square which is first in reading order is chosen. For example:

    return 0;
}
