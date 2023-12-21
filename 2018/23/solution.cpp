#include <iostream>
#include <regex>
#include <vector>

using namespace std;

using Coordinate = tuple<long, long, long>;

struct Nanobot {
    Coordinate coordinate;
    long signalRadius;

    Nanobot(Coordinate coordinate, long signalRadius) {
        this->coordinate = coordinate;
        this->signalRadius = signalRadius;
    }
};

long manhattan(Coordinate a, Coordinate b) {
    return abs(get<0>(a) - get<0>(b))
           + abs(get<1>(a) - get<1>(b))
           + abs(get<2>(a) - get<2>(b));
}

int main() {
    vector<Nanobot> nanobots{};

    string line;
    smatch match;
    regex inputRegex(R"(^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$)");

    Coordinate coordinate{}, strongestCoordinate{};
    long signal, strongestSignal = -1;

    while (getline(cin, line)) {
        regex_match(line, match, inputRegex);

        coordinate = Coordinate{stol(match[1]), stol(match[2]), stol(match[3])};
        signal = stol(match[4]);

        nanobots.emplace_back(coordinate, signal);

        if (signal > strongestSignal) {
            strongestSignal = signal;
            strongestCoordinate = coordinate;
        }
    }

    int withinRange = 0;

    for (auto &nanobot: nanobots) {
        if (manhattan(strongestCoordinate, nanobot.coordinate) <= strongestSignal) {
            withinRange++;
        }
    }

    cout << withinRange << endl;

    return 0;
}
