#include <iostream>
#include <string>
#include <stdlib.h>

using std::cout, std::endl, std::cin;

struct challenges {
    virtual void solve() {
        cout << "You solved a challenge!" << endl;

    }
};

struct forensics : challenges {
    void solve() override {
        cout << "You solved a forensics challenge by using strings and grepping for the flag!" << endl;
    }
};

struct reversing : challenges {
    void solve() override {
        cout << "You solved a reversing challenge by throwing angr at it!" << endl;
        
    }
};

struct pwn : challenges {
    void solve() override {
        cout << "You solved a pwn challenge by keysmashing and being lucky!" << endl;
        
    }
};

struct web : challenges {
    void solve() override {
        cout << "You solved a web challenge by copy and pasting payloadallthethings!" << endl;
        
    }
};

struct crypto : challenges {
    void solve() override {
        cout << "You solved a crypto challenge with rsactftool!" << endl;
        
    }
};

void win() {
    system("/bin/sh");
}

void* win_addr = (void*) &win;

challenges* downloaded [4];

void downloadChallenge() {
    int choice;
    int index;

    while (true) {
        cout << "DOWNLOAD A CHALLENGE" << endl;
        cout << "Choose a category" << endl;
        cout << "1. Forensics" << endl;
        cout << "2. Reversing" << endl;
        cout << "3. Pwn" << endl;
        cout << "4. Web" << endl;
        cout << "5. Crypto" << endl;
        cout << "> ";
        cin >> choice;

        cout << "Choose an index to save your challenge to (0-3)" << endl;
        cout << "> ";
        cin >> index;
        
        if ((choice >= 1 && choice <=5) && (index >= 0 && index <= 3)) {
            break;
        }
        else {
            cout << "Invalid category or index" << endl;
        }
    }

    if (choice == 1) {
        downloaded[index] = new forensics;
    }
    else if (choice == 2) {
        downloaded[index] = new reversing;
    }
    else if (choice == 3) {
        downloaded[index] = new pwn;
    }
    else if (choice == 4) {
        downloaded[index] = new web;
    }
    else {
        downloaded[index] = new crypto;
    }

}

void solveChallenge() {
    int index;
    while (true) {
        cout << "SOLVE A CHALLENGE" << endl;
        cout << "Choose one of your downloaded challenges (0-3)" << endl;
        cout << "> ";
        cin >> index;

        if (index >= 0 && index <= 3) {
            break;
        }
    }

    downloaded[index] -> solve();
    delete downloaded[index];

}

void submitWriteup() {
    int length;
    cout << "SUBMIT A WRITEUP" << endl;
    cout << "How long is your writeup?" << endl;
    cout << "> ";
    cin >> length;
    cout << "Enter your writeup" << endl;
    cout << "> ";
    cin.get();
    char* writeup;
    writeup = (char*) malloc(length);

    fgets(writeup, length, stdin);   

}


int main() {
    int choice;
    while (true) {
        cout << "CTF SIM" << endl;
        cout << "1. Download a Challenge" << endl;
        cout << "2. Solve a Challenge" << endl;
        cout << "3. Submit a writeup" << endl;
        cout << "4. Quit" << endl;
        cout << "> ";
        cin >> choice;

        if (choice >=1 && choice <= 4) {
            if (choice == 1) {
                downloadChallenge();
            }
            else if (choice == 2) {
                solveChallenge();
            }
            else if (choice == 3) {
                submitWriteup();
            }
            else {
                exit(0);
            }

            
        }
    }



}