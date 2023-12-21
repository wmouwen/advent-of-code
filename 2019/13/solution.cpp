#include <set>
#include <utility>
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
using Coordinate = pair<long, long>;
using IO = deque<long>;

enum Direction {
    UP = 0, RIGHT = 1, DOWN = 2, LEFT = 3
};

class Intcode {
public:
    Memory memory{};
    IO input{};
    IO output{};

    long ip{};
    long opcode{};
    long instruction{};
    bool blocked{};
    bool halted{};

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

    long mode(long code, long offset) {
        long base = pow(10, offset + 1);
        return (code / base) % 10;
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
        if (memory.count(addr)) {
            memory.erase(addr);
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

void draw(int field[21][36]) {
    for (int fy = 0; fy < 21; fy++) {
        for (int fx = 0; fx < 36; fx++) {
            cout << field[fy][fx];
        }
        cout << endl;
    }
}

int main() {
    Memory memory = getInput();

    Intcode intcode = Intcode();
    intcode.memory = memory;
    intcode.init();
    intcode.run();

    int x = 0, y = 0, type = 0;
    int blocks = 0;
//    int field[21][36];

    while (!intcode.output.empty()) {
        x = intcode.output.front();
        intcode.output.pop_front();
        y = intcode.output.front();
        intcode.output.pop_front();
        type = intcode.output.front();
        intcode.output.pop_front();

//        field[y][x] = type;

        if (type == 2) {
            blocks++;
        }
    }

    cout << blocks << endl;

    intcode = Intcode();
    intcode.memory = memory;
    intcode.memory[0] = 2;
    intcode.init();

    int ballX = 0, paddleX = 0, score = 0;

    do {
        intcode.run();

        while (!intcode.output.empty()) {
            x = intcode.output.front();
            intcode.output.pop_front();
            y = intcode.output.front();
            intcode.output.pop_front();
            type = intcode.output.front();
            intcode.output.pop_front();

            if (x == -1) {
                score = type;
            } else {
//                field[y][x] = type;
                if (type == 3) {
                    paddleX = x;
                }
                if (type == 4) {
                    ballX = x;
                }
            }
        }

//        draw(field);

        intcode.input.push_back(ballX == paddleX ? 0 : (ballX < paddleX ? -1 : 1));
    } while (!intcode.halted);

    cout << score << endl;

    return 0;
}
