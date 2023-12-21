#include <vector>
#include <sstream>
#include <iostream>

using namespace std;

vector<int> intcode(vector<int> memory) {
    int ip = 0x00;

    while (0x00 <= ip && ip < memory.size()) {
        switch (memory[ip]) {
            case 1:
                memory[memory[ip + 3]] = memory[memory[ip + 1]] + memory[memory[ip + 2]];
                ip = ip + 4;
                continue;

            case 2:
                memory[memory[ip + 3]] = memory[memory[ip + 1]] * memory[memory[ip + 2]];
                ip = ip + 4;
                continue;

            case 99:
                return memory;

            default:
                throw logic_error("Unknown operation");
        }
    }

    throw logic_error("Invalid memory address");
}

vector<int> getInput() {
    string line;
    getline(cin, line);

    vector<int> memory;

    stringstream ss(line);
    string number;
    while (getline(ss, number, ',')) {
        memory.push_back(stoi(number));
    }

    return memory;
}

int main() {
    vector<int> memory = getInput();
    vector<int> output;

    // Part 1
    memory[0x01] = 12;
    memory[0x02] = 02;

    output = intcode(memory);
    cout << output[0x00] << endl;

    // Part 2
    for (int attempt = 0; attempt < 10000; attempt++) {
        memory[0x01] = attempt / 100;
        memory[0x02] = attempt % 100;

        output = intcode(memory);
        if (output[0x00] == 19690720) {
            cout << attempt << endl;
            break;
        }
    }

    return 0;
}
