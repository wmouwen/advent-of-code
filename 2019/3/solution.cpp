#include <vector>
#include <sstream>
#include <iostream>
#include <cmath>
#include <climits>

using namespace std;

struct Location {
    int x, y, steps;
};

int main() {
    string line;

    vector<Location> grid;
    int x = 0, y = 0, totalSteps = 0;

    getline(cin, line);
    stringstream ss(line);
    string command;
    while (getline(ss, command, ',')) {
        int dx = 0, dy = 0;

        switch (command[0]) {
            case 'U':
                dy = 1;
                break;

            case 'R':
                dx = 1;
                break;

            case 'D':
                dy = -1;
                break;

            case 'L':
                dx = -1;
                break;
        }

        for (int steps = stoi(command.substr(1)); steps > 0; steps--) {
            totalSteps++;
            x += dx;
            y += dy;

            Location location;
            location.x = x;
            location.y = y;
            location.steps = totalSteps;
            grid.push_back(location);
        }
    }

    int bestDistance = INT_MAX;
    int bestSteps = INT_MAX;

    getline(cin, line);
    ss.str(line);
    ss.clear();
    x = 0;
    y = 0;
    totalSteps = 0;
    while (getline(ss, command, ',')) {
        int dx = 0, dy = 0;

        switch (command[0]) {
            case 'U':
                dy = 1;
                break;

            case 'R':
                dx = 1;
                break;

            case 'D':
                dy = -1;
                break;

            case 'L':
                dx = -1;
                break;
        }

        for (int steps = stoi(command.substr(1)); steps > 0; steps--) {
            totalSteps++;
            x += dx;
            y += dy;

            for (Location location: grid) {
                if (location.x == x && location.y == y) {
//                    cout << "overlap [" << x << ", " << y << "]"
//                         << " dist=" << (x + y)
//                         << " steps=" << (totalSteps + location.steps)
//                         << endl;
                    if (abs(x) + abs(y) < bestDistance) {
                        bestDistance = abs(x) + abs(y);
                    }
                    if (totalSteps + location.steps < bestSteps) {
                        bestSteps = totalSteps + location.steps;
                    }
                }
            }
        }
    }

    cout << bestDistance << endl;
    cout << bestSteps << endl;

    return 0;
}
