#include <algorithm>
#include <iostream>
#include <string>

const int IMGWIDTH = 25;
const int IMGHEIGHT = 6;

using namespace std;

int main() {
    string input;
    getline(cin, input);

    long fewestZeroes = INT32_MAX;
    long amountOneTimesTwo = 0;

    char message[IMGWIDTH * IMGHEIGHT] = {};

    for (int i = 0; i * IMGWIDTH * IMGHEIGHT < input.length(); i++) {
        string substr = input.substr(i * IMGWIDTH * IMGHEIGHT, IMGWIDTH * IMGHEIGHT);

        int zeroes = count(substr.begin(), substr.end(), '0');
        if (zeroes < fewestZeroes) {
            fewestZeroes = zeroes;
            amountOneTimesTwo = count(substr.begin(), substr.end(), '1') * count(substr.begin(), substr.end(), '2');
        }

        for (int j = 0; j < substr.length(); j++) {
            if (message[j] != '1' && message[j] != '0') {
                message[j] = substr[j];
            }
        }
    }

    cout << amountOneTimesTwo << endl;

    for (int y = 0; y < IMGHEIGHT; y++) {
        for (int x = 0; x < IMGWIDTH; x++) {
            switch (message[y * IMGWIDTH + x]) {
                case '0':
                    cout << ' ';
                    break;
                case '1':
                    cout << '#';
                    break;
                default:
                    break;
            }
        }
        cout << endl;
    }

    return 0;
}
