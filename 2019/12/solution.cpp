#include <iostream>
#include <utility>
#include <vector>
#include <regex>

#define DIMENSIONS 3

using namespace std;

struct Moon {
    vector<long> position;
    vector<long> velocity = {0, 0, 0};

    explicit Moon(vector<long> position) {
        this->position = std::move(position);
    }

    long potentialEnergy() {
        long energy = 0;
        for (auto &p: position) {
            energy += abs(p);
        }
        return energy;
    }

    long kineticEnergy() {
        long energy = 0;
        for (auto &v: velocity) {
            energy += abs(v);
        }
        return energy;
    }
};

long lcm(long a, long b) {
    long m, n;

    m = a;
    n = b;

    while (m != n) {
        if (m < n) {
            m = m + a;
        } else {
            n = n + b;
        }
    }

    return m;
}

int main() {
    vector<Moon> moons{};
    vector<Moon> initial{};

    long repeat[]{0, 0, 0};

    string input;
    regex search(R"(<x=(-?\d+),\s*y=(-?\d+),\s*z=(-?\d+)>)");
    while (getline(cin, input)) {
        smatch matches;
        if (regex_search(input, matches, search)) {
            vector<long>position{stol(matches[1]), stol(matches[2]), stol(matches[3])};
            moons.emplace_back(position);
            initial.emplace_back(position);
        }
    }

    for (long steps = 1; true; steps++) {
        for (int dimension = 0; dimension < DIMENSIONS; dimension++) {
            for (auto &moon: moons) {
                for (auto &other: moons) {
                    if (moon.position[dimension] != other.position[dimension]) {
                        moon.velocity[dimension] += moon.position[dimension] < other.position[dimension] ? 1 : -1;
                    }
                }
            }

            bool repeats = true;
            for (int i = 0; i < moons.size(); i++) {
                moons[i].position[dimension] += moons[i].velocity[dimension];

                repeats = repeats
                          && moons[i].position[dimension] == initial[i].position[dimension]
                          && moons[i].velocity[dimension] == initial[i].velocity[dimension];
            }
            if (repeat[dimension] == 0 && repeats) {
                repeat[dimension] = steps;
            }
        }

        if (steps == 1000) {
            long energy = 0;
            for (auto &moon: moons) {
                energy += moon.potentialEnergy() * moon.kineticEnergy();
            }
            cout << energy << endl;
        }

        if (repeat[0] != 0 && repeat[1] != 0 && repeat[2] != 0) {
            cout << lcm(repeat[0], lcm(repeat[1], repeat[2])) << endl;
            return 0;
        }
    }
}