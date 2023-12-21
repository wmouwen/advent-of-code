#include <vector>
#include <sstream>
#include <iostream>
#include <cmath>
#include <deque>
#include <map>
#include <array>

using namespace std;

using Address = long;
using Value = long;
using Memory = map<Address, Value>;
using IO = deque<Value>;

class Intcode {
private:
    enum Instruction {
        ADD = 0x01,
        MUL = 0x02,
        READ = 0x03,
        WRITE = 0x04,
        JNZ = 0x05,
        JZ = 0x06,
        JL = 0x07,
        JE = 0x08,
        BASE = 0x09,
        HALT = 0x63
    };

    enum ParameterMode {
        POSITION = 0,
        IMMEDIATE = 1,
        RELATIVE = 2
    };

public:
    Memory memory{};
    IO input{};
    IO output{};

private:
    Address instructionPointer = 0x00;
    Address relativeBase = 0x00;
    bool blocked = false;
    bool halted = false;

public:
    void init() {
        this->instructionPointer = 0x00;
        this->relativeBase = 0x00;
        this->halted = false;
    }

    void run() {
        this->blocked = false;

        while (!this->blocked && !this->halted) {
            switch (this->instruction()) {
                case Instruction::ADD:
                    this->write(this->param(3), this->read(this->param(1)) + this->read(this->param(2)));
                    this->instructionPointer += 4;
                    break;

                case Instruction::MUL:
                    this->write(this->param(3), this->read(this->param(1)) * this->read(this->param(2)));
                    this->instructionPointer += 4;
                    break;

                case Instruction::READ:
                    if (this->input.empty()) {
                        this->blocked = true;
                    } else {
                        this->write(this->param(1), this->input.front());
                        this->input.pop_front();
                        this->instructionPointer += 2;
                    }
                    break;

                case Instruction::WRITE:
                    this->output.push_back(this->read(this->param(1)));
                    this->instructionPointer += 2;
                    break;

                case Instruction::JNZ:
                    if (this->read(this->param(1))) {
                        this->instructionPointer = this->read(this->param(2));
                    } else {
                        this->instructionPointer += 3;
                    }
                    break;

                case Instruction::JZ:
                    if (!this->read(this->param(1))) {
                        this->instructionPointer = this->read(this->param(2));
                    } else {
                        this->instructionPointer += 3;
                    }
                    break;

                case Instruction::JL:
                    this->write(this->param(3), this->read(this->param(1)) < this->read(this->param(2)) ? 1 : 0);
                    this->instructionPointer += 4;
                    break;

                case Instruction::JE:
                    this->write(this->param(3), this->read(this->param(1)) == this->read(this->param(2)) ? 1 : 0);
                    this->instructionPointer += 4;
                    break;

                case Instruction::BASE:
                    this->relativeBase += this->read(this->param(1));
                    this->instructionPointer += 2;
                    break;

                case Instruction::HALT:
                    this->halted = true;
                    break;

                default:
                    throw logic_error("Unknown operation");
            }
        }
    }

private:
    Instruction instruction() {
        return static_cast<Instruction>(this->read(this->instructionPointer) % 100);
    }

    Value param(long index) {
        switch ((this->read(this->instructionPointer) / (long) pow(10, index + 1)) % 10) {
            case ParameterMode::POSITION:
                return this->read(this->instructionPointer + index);

            case ParameterMode::IMMEDIATE:
                return this->instructionPointer + index;

            case ParameterMode::RELATIVE:
                return this->relativeBase + this->read(this->instructionPointer + index);

            default:
                throw logic_error("Unknown parameter mode");
        }
    }

    Value read(Address address) {
        try {
            return this->memory.at(address);
        } catch (const out_of_range &e) {
            return 0;
        }
    }

    void write(Address address, Value value) {
        try {
            this->memory.at(address) = value;
        } catch (const out_of_range &e) {
            this->memory.emplace(address, value);
        }
    }
};

Memory getInput() {
    Memory memory;

    string input;
    getline(cin, input);
    stringstream ss(input);

    Address address = 0;
    while (getline(ss, input, ',')) {
        memory.emplace(address++, stol(input));
    }

    return memory;
}

int main() {
    Memory memory = getInput();

    Intcode intcode;
    intcode.memory = memory;
    intcode.init();
    intcode.run();

    int y = 0, x = 0;
    vector<vector<char>> grid{};
    for (auto &number: intcode.output) {

        char scaffold = (char) number;
        if (scaffold == '\n') {
            y++;
            continue;
        }

        while (grid.size() <= y) {
            grid.emplace_back(vector<char>{});
        }

        grid.at(y).emplace_back(scaffold);
    }

    int sum = 0;
    for (y = 1; y < grid.size() - 1; y++) {
        for (x = 1; x < grid.at(y).size() - 1; x++) {
            if (grid.at(y).at(x) == '#'
                && grid.at(y + 1).at(x) == '#'
                && grid.at(y - 1).at(x) == '#'
                && grid.at(y).at(x + 1) == '#'
                && grid.at(y).at(x - 1) == '#'
                ) {
                sum += x * y;
            }
        }
    }

    cout << sum << endl;

    intcode.memory = memory;
    intcode.memory.at(0) = 0x02;
    intcode.output = IO{};
    intcode.input = IO{
        65, 44, 66, 44, 65, 44, 67, 44, 65, 44, 66, 44, 67, 44, 66, 44, 67, 44, 66, 0x0A,
        76, 44, 49, 48, 44, 82, 44, 56, 44, 76, 44, 54, 44, 82, 44, 54, 0x0A,
        76, 44, 56, 44, 76, 44, 56, 44, 82, 44, 56, 0x0A,
        82, 44, 56, 44, 76, 44, 54, 44, 76, 44, 49, 48, 44, 76, 44, 49, 48, 0x0A,
        'n', 0x0A, 0x0A, 0x0A
    };

    intcode.init();
    intcode.run();

    cout << intcode.output.back() << endl;

    return 0;
}
