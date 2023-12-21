#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

vector <string> explode(const string &input, const char &delimiter) {
    vector <string> result;
    istringstream iss(input);

    for (string token; getline(iss, token, delimiter);) {
        result.push_back(move(token));
    }

    return result;
}

int main() {
    long surface = 0, ribbon = 0;
    int x, y, z;

    string input;
    while (cin >> input) {
        vector <string> exp = explode(input, 'x');

        x = stoi(exp[0]);
        y = stoi(exp[1]);
        z = stoi(exp[2]);

        surface += 2 * (x * y + x * z + y * z)
                   + min(x * y, min(x * z, y * z));
        ribbon += (x * y * z) + 2 * (x + y + z - max(x, max(y, z)));
    }

    cout << surface << endl;
    cout << ribbon << endl;

    return 0;
}