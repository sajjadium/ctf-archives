#include <iostream>
#include <fstream>
#include <string>

using namespace std;

ifstream flag("flag.txt");

struct character {
	int health;
	int skill;
	long tokens;
	string name;
};

void play() {
	string action;
	character player;
	cout << "Enter your name: " << flush;
	getline(cin, player.name);
	cout << "Welcome, " << player.name << ". Skill level: " << player.skill << endl;
	while (true) {
		cout << "\n1. Power up" << endl;
		cout << "2. Fight for the flag" << endl;
		cout << "3. Exit game\n" << endl;
		cout << "What would you like to do? " << flush;
		cin >> action;
		cin.ignore();
		if (action == "1") {
			cout << "Power up requires shadow tokens, available via in app purchase." << endl;
		} else if (action == "2") {
			if (player.skill < 1337) {
				cout << "You flail your arms wildly, but it is no match for the flag guardian. Raid failed." << endl;
			} else if (player.skill > 1337) {
				cout << "The flag guardian quickly succumbs to your overwhelming power. But the flag was destroyed in the frenzy!" << endl;
			} else {
				cout << "It's a tough battle, but you emerge victorious. The flag has been recovered successfully: " << flag.rdbuf() << endl;
			}
		} else if (action == "3") {
			return;
		}
	}
}

void terms_and_conditions() {
	string agreement;
	string signature;
	cout << "\nRAIId Shadow Legends is owned and operated by Working Group 21, Inc. ";
	cout << "As a subsidiary of the International Organization for Standardization, ";
	cout << "we reserve the right to standardize and/or destandardize any gameplay ";
	cout << "elements that are deemed fraudulent, unnecessary, beneficial to the ";
	cout << "player, or otherwise undesirable in our authoritarian society where ";
	cout << "social capital has been eradicated and money is the only source of ";
	cout << "power, legal or otherwise.\n" << endl;
	cout << "Do you agree to the terms and conditions? " << flush;
	cin >> agreement;
	cin.ignore();
	while (agreement != "yes") {
		cout << "Do you agree to the terms and conditions? " << flush;
		cin >> agreement;
		cin.ignore();
	}
	cout << "Sign here: " << flush;
	getline(cin, signature);
}

int main() {
	cout << "Welcome to RAIId Shadow Legends!" << endl;
	while (true) {
		cout << "\n1. Start game" << endl;
		cout << "2. Purchase shadow tokens\n" << endl;
		cout << "What would you like to do? " << flush;
		string action;
		cin >> action;
		cin.ignore();
		if (action == "1") {
			terms_and_conditions();
			play();
		} else if (action == "2") {
			cout << "Please mail a check to RAIId Shadow Legends Headquarters, 1337 Leet Street, 31337." << endl;
		}
	}
}
