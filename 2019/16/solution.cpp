#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

vector<int> getInput() {
    vector<int> input{};
    char character;

    while (cin >> character) {
        int digit = character - '0';
        if (0 <= digit && digit <= 9) {
            input.push_back(digit);
        }
    }

    return input;
}

int seq(int newPosition, int oldPosition) {
    switch ((int) floor((oldPosition + 1) / (newPosition + 1)) % 4) {
        case 0:
            return 0;

        case 1:
            return 1;

        case 2:
            return 0;

        case 3:
            return -1;
    }

    throw logic_error("Mathematical error");
}

vector<int> nextperm(vector<int> &signal) {
    vector<int> newSignal{};

    for (int newPosition = 0; newPosition < signal.size(); newPosition++) {
        long sum = 0;

        for (int oldPosition = 0; oldPosition < signal.size(); oldPosition++) {
            sum += signal.at(oldPosition) * seq(newPosition, oldPosition);
        }

        newSignal.emplace_back(abs(sum) % 10);
    }

    return newSignal;
}


vector<int> nextperm_b(vector<int> &signal) {
    long sum = 0;
    for (int position = signal.size() - 1; position >= 0; position--) {
        sum = (sum + signal.at(position)) % 10;
        signal.at(position) = sum;
    }

    return signal;
}

void output(vector<int> signal) {
    for (int position = 0; position < 8; position++) {
        cout << signal.at(position);
    }

    cout << endl;
}

int main() {
    vector<int> input = getInput();
    vector<int> signal;

    // Part 1
    signal = input;
    for (int phase = 0; phase < 100; phase++) {
        signal = nextperm(signal);
    }
    output(signal);

    // Part 2
    signal = vector<int>{};
    int offset = 0;
    for (int i = 0; i < 7; i++) {
        offset += input.at(i) * (int) pow(10, 7 - i - 1);
    }
    for (int i = offset; i < 10000 * input.size(); i++) {
        signal.emplace_back(input.at(i % input.size()));
    }
    for (int phase = 0; phase < 100; phase++) {
        signal = nextperm_b(signal);
    }
    output(signal);

    return 0;
}
