#include <utility>
#include <vector>
#include <sstream>
#include <iostream>
#include <cmath>

using namespace std;

class Intcode {
    vector<int> initialMemory;
    vector<int> workingMemory;

public:
    explicit Intcode(vector<int> memory) {
        initialMemory = move(memory);
    }

    void init() {
        workingMemory = initialMemory;
    }

    void run(int userID) {
        int ip = 0x00;
        int opcode, instruction, paramA, paramB, paramC;

        while (0x00 <= ip && ip < workingMemory.size()) {

            opcode = workingMemory[ip];
            instruction = opcode % 100;

            switch (instruction) {
                case 1:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    paramC = getParameter(workingMemory, ip, 3);
                    workingMemory[paramC] = workingMemory[paramA] + workingMemory[paramB];
                    ip = ip + 4;
                    continue;

                case 2:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    paramC = getParameter(workingMemory, ip, 3);
                    workingMemory[paramC] = workingMemory[paramA] * workingMemory[paramB];
                    ip = ip + 4;
                    continue;

                case 3:
                    paramA = getParameter(workingMemory, ip, 1);
                    workingMemory[paramA] = readInput(userID);
                    ip = ip + 2;
                    continue;

                case 4:
                    paramA = getParameter(workingMemory, ip, 1);
                    if (workingMemory[paramA] != 0) {
                        writeOutput(workingMemory[paramA]);
                    }
                    ip = ip + 2;
                    continue;

                case 5:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    ip = workingMemory[paramA] != 0 ? workingMemory[paramB] : ip + 3;
                    continue;

                case 6:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    ip = workingMemory[paramA] == 0 ? workingMemory[paramB] : ip + 3;
                    continue;

                case 7:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    paramC = getParameter(workingMemory, ip, 3);
                    workingMemory[paramC] = workingMemory[paramA] < workingMemory[paramB] ? 1 : 0;
                    ip = ip + 4;
                    continue;

                case 8:
                    paramA = getParameter(workingMemory, ip, 1);
                    paramB = getParameter(workingMemory, ip, 2);
                    paramC = getParameter(workingMemory, ip, 3);
                    workingMemory[paramC] = workingMemory[paramA] == workingMemory[paramB] ? 1 : 0;
                    ip = ip + 4;
                    continue;

                case 99:
                    return;

                default:
                    throw logic_error("Unknown operation");
            }
        }

        throw logic_error("Invalid memory address");
    }

private:
    static int getMode(int opcode, int offset) {
        int base = pow(10, offset + 1);
        return (opcode / base) % 10;
    }

    static int getParameter(vector<int> &memory, int ip, int offset) {
        switch (getMode(memory[ip], offset)) {
            case 0:
                return memory[ip + offset];

            case 1:
                return ip + offset;

            default:
                throw logic_error("Unknown parameter mode");
        }
    }

    static int readInput(int userID) {
        return userID;
    }

    static void writeOutput(int output) {
        cout << output << endl;
    }
};

vector<int> getInput() {
    vector<int> memory;

    string line;
    getline(cin, line);
    stringstream ss(line);
    string number;
    while (getline(ss, number, ',')) {
        memory.push_back(stoi(number));
    }

    return memory;
}

int main() {
    Intcode intcode(getInput());

    intcode.init();
    intcode.run(1);

    intcode.init();
    intcode.run(5);

    return 0;
}
