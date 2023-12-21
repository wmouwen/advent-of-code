#include <iostream>
#include <string>

using namespace std;

int main() {
    int floor = 0;
    int basement = 0;

    string input;
    cin >> input;

    for (int i = 0; i < input.length(); i++) {
        floor += input[i] == '(' ? 1 : -1;
        if (floor == -1 && basement == 0) {
            basement = i + 1;
        }
    }

    cout << floor << endl;
    cout << basement << endl;

    return 0;
}