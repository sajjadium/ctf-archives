#include <exception>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void print_flag() {
    ifstream f{"./flag.txt"};
    if (!f.is_open()) {
        cout << "Failed to open flag file. Contact CTF organizers if you see this error." << endl;
    } else {
        string flag;
        f >> flag;
        cout << flag << endl;
    }
}


void direct_hit() {
    try {
        throw exception{};
    } catch (exception e) {
        cout << "Direct hit!" << endl;
        print_flag();
    }
}

class Cannon {
public:
    int bufIndex;
    char buf[32];

    Cannon(): bufIndex(0) {}

    void fire() {
        char c ;
        for (;;) {
            cin.get(c);
            if (c == '\n') {
                break;
            } else {
                buf[bufIndex++] = c;
            }
        }
        if (bufIndex >= 32) {
            throw out_of_range{""};
        }
    }
};

void fire_weapon() {
    Cannon w;
    w.fire();
}

int main() {
    int target_assist;
    cout << "Quick! While the spice harvester's shields are down! Fire the laser cannon!" << endl;
    cout << &target_assist << endl;

    try {
        fire_weapon();
        cout << "Looks like you missed your opportunity to fire." << endl;
    }
    catch (exception e) {
        cout << "Seems like you missed." << endl;
    }
}
