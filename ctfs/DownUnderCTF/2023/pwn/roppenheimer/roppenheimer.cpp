// g++ roppenheimer.cpp -o roppenheimer -fno-stack-protector -no-pie

#include <cstdint>
#include <iostream>
#include <unordered_map>

#define MAX_ATOMS   32
#define MAX_COLLIDE 20
#define NAME_LEN    128

char username[NAME_LEN + 1];
std::unordered_map<unsigned int, uint64_t> atoms;

void useful() {
    __asm__(
        "pop %rax;"
        "pop %rsp;"
        "pop %rdi;"
    );
}

void panic(const std::string& message) {
    std::cerr << std::endl << "error: " << message << std::endl;
    exit(1);
}

void add_atom() {
    if (atoms.size() >= MAX_ATOMS) {
        panic("atom capacity reached");
    }

    unsigned int atom;
    std::cout << "atom> ";
    std::cin >> atom;

    if (atoms.find(atom) != atoms.end()) {
        panic("atom already exists");
    }

    uint64_t data;
    std::cout << "data> ";
    std::cin >> data;

    atoms[atom] = data;
}

void fire_neutron() {
    unsigned int atom;
    std::cout << "atom> ";
    std::cin >> atom;

    if (atoms.find(atom) == atoms.end()) {
        panic("atom does not exist");
    }

    size_t bucket = atoms.bucket(atom);
    size_t bucket_size = atoms.bucket_size(bucket);

    std::pair<unsigned int, uint64_t> elems[MAX_COLLIDE - 1];
    copy(atoms.begin(bucket), atoms.end(bucket), elems);

    std::cout << "[atoms hit]" << std::endl;
    for (size_t i = 0; i < bucket_size; i++) {
        std::cout << elems->first << std::endl;
    }
}

void quit() {
    std::cout << std::endl << "goodbye!" << std::endl;
    exit(0);
}

int get_choice() {
    std::cout << std::endl
              << "[1] add atom" << std::endl
              << "[2] fire neutron" << std::endl
              << "[3] quit" << std::endl;

    int choice;
    std::cout << "choice> ";
    std::cin >> choice;

    if (choice < 1 || choice > 3) {
        panic("invalid choice");
    }

    return choice;
}

int main() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
    atoms.clear();

    puts("atomic research lab v0.0.1");

    std::cout << std::endl << "name> ";
    fgets(username, NAME_LEN, stdin);

    while (true) {
        int choice = get_choice();

        if (choice == 1) {
            add_atom();
        }
        if (choice == 2) {
            fire_neutron();
            quit();
        }
        if (choice == 3) {
            quit();
        }
    }

    return 0;
}
