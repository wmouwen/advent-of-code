#include <vector>
#include <sstream>
#include <iostream>
#include <cmath>
#include <deque>
#include <map>
#include <algorithm>

using namespace std;

using Memory = map<long, long>;
using MemPair = pair<long, long>;
using IO = deque<long>;

class Intcode {
public:
    Memory memory{};
    IO input{};
    IO output{};

    long ip;
    long opcode;
    long instruction;
    bool blocked;
    bool halted;

    void init() {
        ip = 0x00l;
        opcode = 0l;
        instruction = 0l;
        relativeBase = 0l;
        halted = false;
    }

    void run() {
        blocked = false;

        while (true) {
            opcode = lookup(ip);
            instruction = opcode % 100;

            switch (instruction) {
                case 1:
                    store(addr(ip, 3), lookup(addr(ip, 1)) + lookup(addr(ip, 2)));
                    ip = ip + 4;
                    continue;

                case 2:
                    store(addr(ip, 3), lookup(addr(ip, 1)) * lookup(addr(ip, 2)));
                    ip = ip + 4;
                    continue;

                case 3:
                    if (input.empty()) {
                        blocked = true;
                        return;
                    }

                    store(addr(ip, 1), input.front());
                    input.pop_front();
                    ip = ip + 2;
                    continue;

                case 4:
                    output.push_back(lookup(addr(ip, 1)));
                    ip = ip + 2;
                    continue;

                case 5:
                    ip = lookup(addr(ip, 1)) != 0 ? lookup(addr(ip, 2)) : ip + 3;
                    continue;

                case 6:
                    ip = lookup(addr(ip, 1)) == 0 ? lookup(addr(ip, 2)) : ip + 3;
                    continue;

                case 7:
                    store(addr(ip, 3), lookup(addr(ip, 1)) < lookup(addr(ip, 2)) ? 1 : 0);
                    ip = ip + 4;
                    continue;

                case 8:
                    store(addr(ip, 3), lookup(addr(ip, 1)) == lookup(addr(ip, 2)) ? 1 : 0);
                    ip = ip + 4;
                    continue;

                case 9:
                    updateRelativeBase(lookup(addr(ip, 1)));
                    ip = ip + 2;
                    continue;

                case 99:
                    halted = true;
                    return;

                default:
                    throw logic_error("Unknown operation");
            }
        }
    }

private:
    long relativeBase = 0l;

    void updateRelativeBase(long increment) {
        relativeBase += increment;
    }

    long mode(long opcode, long offset) {
        long base = pow(10, offset + 1);
        return (opcode / base) % 10;
    }

    long addr(long base, long offset = 0) {
        switch (mode(lookup(base), offset)) {
            case 0: // Position mode
                return lookup(base + offset);

            case 1: // Immediate mode
                return base + offset;

            case 2: // Relative mode
                return relativeBase + lookup(base + offset);

            default:
                throw logic_error("Unknown parameter mode");
        }
    }

    long lookup(long addr) {
        try {
            return memory.at(addr);
        } catch (const out_of_range &e) {
            return 0;
        }
    }

    void store(long addr, long value) {
        auto it = memory.find(addr);
        if (it != memory.end()) {
            memory.erase(it);
        }
        memory.insert(MemPair(addr, value));
    }
};

Memory getInput() {
    Memory memory;

    string input;
    getline(cin, input);
    stringstream ss(input);
    long i = 0;
    while (getline(ss, input, ',')) {
        memory.insert(MemPair(i++, stol(input)));
    }

    return memory;
}

int main() {
    Memory memory = getInput();

    Intcode intcode{};
    intcode.memory = memory;
    intcode.input = IO{1};
    intcode.output = IO{};
    intcode.init();
    intcode.run();

    cout << intcode.output[0] << endl;

    intcode.memory = memory;
    intcode.input = IO{2};
    intcode.output = IO{};
    intcode.init();
    intcode.run();

    cout << intcode.output[0] << endl;

    return 0;
}
