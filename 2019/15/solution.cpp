#include <set>
#include <utility>
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
        HALT = 0x99
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

using Location = pair<int, int>;
using Walls = set<Location>;
using Distances = map<Location, int>;

enum Direction {
    NORTH = 1,
    SOUTH = 2,
    WEST = 3,
    EAST = 4
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

Direction left(Direction direction) {
    switch (direction) {
        case Direction::NORTH:
            return Direction::WEST;
        case Direction::WEST:
            return Direction::SOUTH;
        case Direction::SOUTH:
            return Direction::EAST;
        case Direction::EAST:
            return Direction::NORTH;
        default:
            throw logic_error("Invalid direction");
    }
}

Direction right(Direction direction) {
    switch (direction) {
        case Direction::NORTH:
            return Direction::EAST;
        case Direction::EAST:
            return Direction::SOUTH;
        case Direction::SOUTH:
            return Direction::WEST;
        case Direction::WEST:
            return Direction::NORTH;
        default:
            throw logic_error("Invalid direction");
    }
}

Location move(Location location, Direction direction) {
    switch (direction) {
        case Direction::NORTH:
            location.first--;
            break;
        case Direction::SOUTH:
            location.first++;
            break;
        case Direction::EAST:
            location.second++;
            break;
        case Direction::WEST:
            location.second--;
            break;
        default:
            throw logic_error("Invalid direction");
    }

    return location;
}

Walls createMap(const Memory &memory, Location source, Location &sink) {
    Intcode intcode = Intcode();
    intcode.memory = memory;
    intcode.init();

    Walls walls;
    Location droid{source.first, source.second};
    Direction direction = Direction::EAST;

    while (droid.first != source.first || droid.second != source.second || walls.empty()) {
        Direction attemptedDirection = left(direction);
        bool droidMoved = false;

        do {
            intcode.input.push_back(attemptedDirection);
            intcode.run();

            int output = intcode.output.front();
            intcode.output.pop_front();

            if (output == 0) {
                // Wall
                walls.insert(move(droid, attemptedDirection));
                attemptedDirection = right(attemptedDirection);

            } else {
                // Open space
                if (output == 2) {
                    sink = move(droid, attemptedDirection);
                }

                droid = move(droid, attemptedDirection);
                direction = attemptedDirection;
                droidMoved = true;

            }

        } while (!droidMoved);
    }

    return walls;
}

Distances distances(const Walls &walls, Location source) {
    static const Location movements[]{
        {1,  0},
        {-1, 0},
        {0,  1},
        {0,  -1}
    };

    Distances distances{{source, 0}};
    deque<Location> queue{source};

    while (!queue.empty()) {
        Location current = queue.front();
        queue.pop_front();

        for (auto &movement: movements) {
            Location attempt{
                current.first + movement.first,
                current.second + movement.second
            };

            if (!walls.count(attempt) && !distances.count(attempt)) {
                distances.emplace(attempt, distances.at(current) + 1);
                queue.push_back(attempt);
            }
        }
    }

    return distances;
}

int max(const Distances &distances) {
    int farthest = 0;

    for (auto &distance: distances) {
        farthest = max(farthest, distance.second);
    }

    return farthest;
}

int main() {
    Location source{0, 0}, sink;
    Walls walls = createMap(getInput(), source, sink);

    Distances dists = distances(walls, sink);
    cout << dists.find(source)->second << endl;
    cout << max(dists) << endl;

    return 0;
}
