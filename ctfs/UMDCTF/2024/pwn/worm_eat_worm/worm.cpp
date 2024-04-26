#include <iostream>
#include <iomanip>
#include <cstring>
#include <vector>



class Worm {
    char* cstring; 
 
public:
    Worm(): cstring(new char[100]) {
        std::cout << "Enter your worm name: ";
        std::cin >> std::setw(99) >> cstring;
    }
    Worm(const char* s): cstring(new char[100]) {
        std::memcpy(cstring, s, 100); 
    }
 
 
    ~Worm() {
        delete[] cstring; 
    }
 
    Worm(const Worm& other) 
        : Worm(other.cstring) {}
 
    Worm& operator=(const Worm& other) {
        delete[] cstring;
        cstring = other.cstring;
 
        return *this;
    }

    char* get() {
        return cstring;
    }

    void set() {
        std::cout << "Enter your string: ";
        std::cin >> std::setw(99) >> cstring;
    }
};


void prompt() {
    std::cout << "1) New" << std::endl;
    std::cout << "2) Eat" << std::endl;
    std::cout << "3) Rename" << std::endl;
    std::cout << "4) Get" << std::endl;
    std::cout << "5) Exit" << std::endl;
}

int main() {

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int choice;
    int a, b;
    int get_count = 0;

    std::vector<Worm> worms;
    worms.reserve(20);


    std::cout << "Free libc leak: " << stdin << std::endl;
    while (true) {
        prompt();
        std::cin >> choice;
        switch (choice) {
        case 1:
            worms.emplace_back(Worm{});
            break;
        case 2:
            std::cout << "Which worm do you want to be the eater? " << std::endl;
            std::cin >> a;
            std::cout << "Which worm do you want to eat? " << std::endl;
            std::cin >> b;
            if (a < 0 || b < 0 || a >= worms.size() || b >= worms.size()) {
                std::cout << "Invalid indices." << std::endl;
                break;
            }
            worms[b] = worms[a];
            break;

        case 3:
            std::cout << "Which worm do you want to rename? ";
            std::cin >> a;
            if (a >= 0 && a < worms.size()) {
                worms[a].set();
            } else {
                std::cout << "Invalid indices." << std::endl;
            }
            break;

        case 4:
            if (get_count++ > 0) {
                std::cout << "Why don't you remember your worms' names?" << std::endl;
                break;
            }
            std::cout << "Which do you want to get? ";
            std::cin >> a;
            if (a >= 0 && a < worms.size()) {
                std::cout << worms[a].get() << std::endl;
            } else {
                std::cout << "Invalid indices" << std::endl;
            }
            break;
        case 5:
            return 0;
        default:
            break;
        }
    }
}
