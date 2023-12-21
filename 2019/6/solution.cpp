#include <vector>
#include <sstream>
#include <iostream>
#include <map>

using namespace std;

using OrbitMap = std::map<string, string>;
using DistanceMap = std::map<string, int>;

OrbitMap getInput() {
    OrbitMap orbitMap;

    string line;
    while (getline(cin, line)) {
        stringstream ss(line);
        string parent, child;
        getline(ss, parent, ')');
        getline(ss, child, ')');

        orbitMap.emplace(child, parent);
    }

    return orbitMap;
}

int orbitSum(OrbitMap orbitMap) {
    int sum = 0;

    for (const auto &mapping: orbitMap) {
        string current = mapping.second;
        sum++;

        while (true) {
            try {
                current = orbitMap.at(current);
                sum++;
            } catch (const out_of_range &e) {
                break;
            }
        }
    }

    return sum;
}

int orbitDistanceBetween(OrbitMap orbitMap, string a, string b) {
    DistanceMap distanceMap{};

    int distance = 0;
    string current = orbitMap.at(a);

    while (true) {
        try {
            distanceMap.emplace(current, distance++);
            current = orbitMap.at(current);
        } catch (const out_of_range &e) {
            break;
        }
    }

    distance = 0;
    current = orbitMap.at(b);

    while (true) {
        try {
            int match = distanceMap.at(current);
            return match + distance;
        } catch (const out_of_range &e) {
            try {
                current = orbitMap.at(current);
                distance++;
            } catch (const out_of_range &e) {
                throw logic_error("No shared parent");
            }
        }
    }
}

int main() {
    OrbitMap orbitMap = getInput();

    cout << orbitSum(orbitMap) << endl;
    cout << orbitDistanceBetween(orbitMap, "YOU", "SAN") << endl;

    return 0;
}
