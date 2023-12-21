#include <iostream>

using namespace std;

int fuelRequired(int weight) {
    return max(0, (weight / 3) - 2);
}

int main() {
    string line;
    int partOne = 0;
    int partTwo = 0;

    while (getline(cin, line)) {
        int fuel = stoi(line);

        partOne += fuelRequired(fuel);

        do {
            fuel = fuelRequired(fuel);
            partTwo += fuel;
        } while (fuel > 0);
    }

    cout << partOne << endl;
    cout << partTwo << endl;

    return 0;
}
