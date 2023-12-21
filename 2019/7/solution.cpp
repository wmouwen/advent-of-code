#include <vector>
#include <sstream>
#include <iostream>
#include <cmath>
#include <deque>
#include <algorithm>
#include <map>

using namespace std;

using Memory = map<int, int>;
using IO = deque<int>;

class Intcode {
public:
    Memory memory{};
    IO input{};
    IO output{};

    int ip;
    int opcode;
    int instruction;
    bool blocked;
    bool halted;

    void init() {
        ip = 0x00;
        opcode = 0;
        instruction = 0;
        halted = false;
    }

    void run() {
        blocked = false;

        while (0x00 <= ip && ip < memory.size()) {
            opcode = memory[ip];
            instruction = opcode % 100;

            switch (instruction) {
                case 1:
                    memory[param(memory, ip, 3)] = memory[param(memory, ip, 1)] + memory[param(memory, ip, 2)];
                    ip = ip + 4;
                    continue;

                case 2:
                    memory[param(memory, ip, 3)] = memory[param(memory, ip, 1)] * memory[param(memory, ip, 2)];
                    ip = ip + 4;
                    continue;

                case 3:
                    if (input.empty()) {
                        blocked = true;
                        return;
                    }

                    memory[param(memory, ip, 1)] = input.front();
                    input.pop_front();
                    ip = ip + 2;
                    continue;

                case 4:
                    output.push_back(memory[param(memory, ip, 1)]);
                    ip = ip + 2;
                    continue;

                case 5:
                    ip = memory[param(memory, ip, 1)] != 0 ? memory[param(memory, ip, 2)] : ip + 3;
                    continue;

                case 6:
                    ip = memory[param(memory, ip, 1)] == 0 ? memory[param(memory, ip, 2)] : ip + 3;
                    continue;

                case 7:
                    memory[param(memory, ip, 3)] = memory[param(memory, ip, 1)] < memory[param(memory, ip, 2)] ? 1 : 0;
                    ip = ip + 4;
                    continue;

                case 8:
                    memory[param(memory, ip, 3)] = memory[param(memory, ip, 1)] == memory[param(memory, ip, 2)] ? 1 : 0;
                    ip = ip + 4;
                    continue;

                case 99:
                    halted = true;
                    return;

                default:
                    throw logic_error("Unknown operation");
            }
        }

        throw logic_error("Invalid memory address");
    }

private:
    static int mode(int opcode, int offset) {
        int base = pow(10, offset + 1);
        return (opcode / base) % 10;
    }

    static int param(Memory &memory, int ip, int offset) {
        switch (mode(memory[ip], offset)) {
            case 0:
                return memory[ip + offset];

            case 1:
                return ip + offset;

            default:
                throw logic_error("Unknown parameter mode");
        }
    }
};

Memory getInput() {
    Memory memory;

    string input;
    getline(cin, input);
    stringstream ss(input);
    while (getline(ss, input, ',')) {
        memory.insert(pair<int, int>(memory.size(), stoi(input)));
    }

    return memory;
}

int computeSinglePass(const Memory &memory, const int phases[]) {
    Intcode intcode{};
    int signal = 0;

    for (int i = 0; i < 5; i++) {
        intcode.memory = memory;
        intcode.input = IO{phases[i], signal};
        intcode.output = IO{};
        intcode.init();
        intcode.run();
        signal = intcode.output.front();
    }

    return signal;
}

int computeFeedbackLoop(const Memory &memory, const int phases[]) {
    Intcode intcode[]{Intcode{}, Intcode{}, Intcode{}, Intcode{}, Intcode{}};

    for (int i = 0; i < 5; i++) {
        intcode[i].memory = memory;
        intcode[i].input = IO{phases[i]};
        intcode[i].output = IO{};
        intcode[i].init();
    }

    intcode[0].input.push_back(0);

    do {
        for (int i = 0; i < 5; i++) {
            intcode[i].run();
            for (auto & out: intcode[i].output) {
                intcode[(i + 1) % 5].input.push_back(out);
            }
            intcode[i].output = IO{};
        }
    } while (!intcode[0].halted);

    return intcode[0].input.back();
}

int main() {
    Memory memory = getInput();

    int maxSignal = 0;
    int phases[]{0, 1, 2, 3, 4};
    do {
        maxSignal = max(maxSignal, computeSinglePass(memory, phases));
    } while (next_permutation(phases, phases + 5));
    cout << maxSignal << endl;

    maxSignal = 0;
    int feedbackPhases[]{5, 6, 7, 8, 9};
    do {
        maxSignal = max(maxSignal, computeFeedbackLoop(memory, feedbackPhases));
    } while (next_permutation(feedbackPhases, feedbackPhases + 5));
    cout << maxSignal << endl;

    return 0;
}
