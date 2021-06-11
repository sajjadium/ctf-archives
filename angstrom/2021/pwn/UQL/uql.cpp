#include <vector>
#include <map>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include <unistd.h>

using namespace std;

vector<string> db;

struct modification {
	string target;
	int index;
	char value;

	modification(string target, int index, char value)
		: target(target), index(index), value(value) {}
};

struct operation {
	vector<string> insertions;
	vector<string> removals;
	vector<modification> modifications;
	bool display;

	operation() : display(false) {}
};

void check_token (string&& expected, string& received) {
	if (expected != received)
		throw runtime_error("Expected token \""+expected+"\" (got \""+received+"\")");
}

vector<operation> parse(string& query) {
	vector<operation> operations;
	stringstream querystream(query);

	std::string line;
	std::string token;

	while (getline(querystream, line, ';')) {
		while (line.at(0) == ' ') line.erase(line.begin());

		stringstream linestream(line);
		string argument;
		operation op;

		while (linestream >> token) {
			if (token == "insert") {
				linestream >> argument;
				op.insertions.push_back(argument);
			} else if (token == "remove") {
				linestream >> argument;
				op.removals.push_back(argument);
			} else if (token == "modify") {
				linestream >> argument;
				linestream >> token;
				check_token("to", token);
				linestream >> token;
				check_token("be", token);
				string value;
				linestream >> value;
				if (value.length() != 1)
					throw runtime_error("Modification expected single character");
				linestream >> token;
				check_token("at", token);
				int index;
				linestream >> index;
				if (index >= argument.length())
					throw runtime_error("Modification index out of bounds");
				op.modifications.emplace_back(argument, index, value.at(0));
			} else if (token == "display") {
				linestream >> token;
				check_token("everything", token);
				op.display = true;
			}
		}
		operations.push_back(op);
	}
	return operations;
}

void execute(vector<operation>& operations) {
	for (vector<operation>::iterator op_it = operations.begin(); op_it != operations.end(); op_it++) {
		operation& op = *op_it;
		for (vector<string>::iterator it = op.insertions.begin(); it != op.insertions.end(); it++) {
			db.push_back(*it);
		}
		for (vector<string>::iterator it = db.begin(); it != db.end(); it++) {
			string data = *it;
			vector<modification>::iterator it2 = op.modifications.begin();
			while (it2 != op.modifications.end()) {
				it2 = find_if(it2, op.modifications.end(), [&](modification& m){ return m.target == data; });
				if (it2 != op.modifications.end()) {
					modification m = *(it2++);
					(*it)[m.index] = m.value;
				}
			}
			if (find(op.removals.begin(), op.removals.end(), data) != op.removals.end()) db.erase(it);
			else if (op.display) {
				if (*it != data) cout << data << " -> " << *it << endl;
				else cout << data << endl;
			}
		}
	}
}

int main() {
	setresgid(getegid(), getegid(), getegid());
	string query;
	cout << "Welcome to UQL, the unstructed query language! You can kind of do whatever and it usually works." << endl;
	cout << "Enter your queries below:" << endl;
	while (true) {
		try {
			cout << "> " << flush;
			getline(cin, query);
			vector<operation> ops = parse(query);
			execute(ops);
		}
		catch (exception& e) {
			cout << "Invalid query: " << e.what() << endl;
		}
	}
}
