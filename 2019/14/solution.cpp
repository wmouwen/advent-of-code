#include <iostream>
#include <vector>
#include <regex>
#include <set>
#include <string>
#include <map>

using namespace std;
using Chemical = pair<string, long>;
using ReactionMap = map<string, pair<long, set<Chemical>>>;

Chemical parseChemical(const string &input) {
    smatch matches;
    regex_match(input, matches, regex(R"(\s*(\d+)\s+(\w+)\s*)"));
    return Chemical{matches[2], stoi(matches[1])};
}

ReactionMap getInput() {
    ReactionMap reactions{};

    string line;
    while (getline(cin, line)) {
        smatch lineMatch;
        if (!regex_match(line, lineMatch, regex("(.*?)\\s+=>\\s+(.*?)"))) {
            break;
        }

        Chemical target = parseChemical(lineMatch[2]);
        if (reactions.count(target.first) == 0) {
            reactions.emplace(target.first, pair<long, set<Chemical>>{target.second, set<Chemical>{}});
        }

        stringstream ss(lineMatch[1]);
        while (getline(ss, line, ',')) {
            Chemical chemical = parseChemical(line);
            reactions.find(target.first)->second.second.insert(chemical);
        }
    }

    return reactions;
}

long oreRequired(ReactionMap reactions, long fuel) {
    deque<pair<string, long>> todo{pair<string, long>{"FUEL", fuel}};
    map<string, long> remainders{};
    long ore = 0;

    while (!todo.empty()) {
        pair<string, long> current = todo.front();
        todo.pop_front();

        if (remainders.count(current.first) == 0) {
            remainders.emplace(current.first, 0);
        }

        long needed = current.second - remainders.at(current.first);

        if (needed <= 0) {
            // Enough in store.
            remainders.at(current.first) -= current.second;

        } else {
            // We need more.
            pair<long, set<Chemical>> list = reactions.find(current.first)->second;

            // Find first multiple of list.first which equals or exceeds needed.
            long times = needed / list.first;
            while (times * list.first < needed) {
                times++;
            }

            remainders.at(current.first) = (times * list.first) - needed;

            for (const pair<basic_string<char>, long> &req: list.second) {
                if (req.first == "ORE") {
                    ore += req.second * times;
                } else {
                    todo.emplace_back(
                            req.first,
                            req.second * times
                    );
                }
            }
        }
    }

    return ore;
}

int main() {
    ReactionMap reactions = getInput();

    long t = 4*631981 - 260438;
    cout << oreRequired(reactions, 1) << endl;
    cout << t << endl;

    return 0;
}