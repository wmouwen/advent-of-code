#include <iostream>
#include <regex>

using namespace std;

pair<int, int> getRange() {
    string input;
    pair<int, int> range;

    getline(cin, input, '-');
    range.first = stoi(input);

    getline(cin, input);
    range.second = stoi(input);

    return range;
}

int main() {
    pair<int, int> range = getRange();

    int partOne = 0;
    int partTwo = 0;

    regex regexNonDecreasing("^0*1*2*3*4*5*6*7*8*9*$");
    regex regexDigitGroups("(\\d)\\1+");

    for (int i = range.first; i <= range.second; i++) {
        string number = to_string(i);
        if (!regex_match(number, regexNonDecreasing)) {
            continue;
        }

        smatch match;
        bool partOneMatch = false;
        bool partTwoMatch = false;

        while (regex_search(number, match, regexDigitGroups)) {
            partOneMatch = true;
            partTwoMatch = partTwoMatch || (match.length() == 2);
            number = match.suffix();
        }

        partOne += partOneMatch ? 1 : 0;
        partTwo += partTwoMatch ? 1 : 0;
    }

    cout << partOne << endl;
    cout << partTwo << endl;

    return 0;
}
