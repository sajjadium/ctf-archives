#include <iostream>
#include <fstream>
#include <unordered_set>
#include <unordered_map>
#include <memory>
#include <cstring>
#include <unistd.h>
#include <signal.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>

struct cache {
    char *base;
    size_t size;
    cache() : base(nullptr), size(0) {}
    virtual ~cache() {
        if (base != nullptr) {
            delete[] base;
            base = nullptr;
        }
    }
};

std::unordered_set<std::string> usedNames;
std::unordered_map<size_t, cache> caches;

size_t readUint64() {
    std::string tmp;
    std::getline(std::cin, tmp);
    return strtoull(tmp.data(), nullptr, 10);
}

void handleCreate() {
    std::cout << "Name: ";
    std::string name;
    std::getline(std::cin, name);
    if (usedNames.count(name) > 0) {
        std::cout << "Cache already exists!\n";
        return;
    }
    std::cout << "Size: ";
    size_t size = readUint64();
    if (size == 0 || size > 0x1000000) {
        std::cout << "Invalid size!\n";
    }
    usedNames.insert(name);
    caches[std::hash<std::string>{}(name)].size = size;
    std::cout << "Done!\n";
}

void handleRead() {
    std::cout << "Name: ";
    std::string name;
    std::getline(std::cin, name);
    if (usedNames.count(name) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    size_t hash = std::hash<std::string>{}(name);
    if (caches[hash].base == nullptr) {
        std::cout << "No data!\n";
        return;
    }
    std::cout << "Offset: ";
    size_t off = readUint64();
    if (off >= caches[hash].size) {
        std::cout << "Invalid offset!\n";
        return;
    }
    std::cout << "Count: ";
    size_t n = readUint64();
    if (off + n > caches[hash].size) {
        std::cout << "Invalid offset + count!\n";
        return;
    }
    std::cout.write(caches[hash].base + off, n);
    std::cout << '\n';
}

void handleWrite() {
    std::cout << "Name: ";
    std::string name;
    std::getline(std::cin, name);
    if (usedNames.count(name) == 0) {
        std::cout << "Invalid cache name!\n";
        return;
    }
    size_t hash = std::hash<std::string>{}(name);
    std::cout << "Offset: ";
    size_t off = readUint64();
    if (off >= caches[hash].size) {
        std::cout << "Invalid offset!\n";
        return;
    }
    std::cout << "Count: ";
    size_t n = readUint64();
    if (off + n > caches[hash].size) {
        std::cout << "Invalid offset + count!\n";
        return;
    }
    if (caches[hash].base == nullptr) {
        caches[hash].base = new char[caches[hash].size];
        memset(caches[hash].base, 0, caches[hash].size);
    }
    std::cout << "Data: ";
    std::cin.read(caches[hash].base + off, n);
    std::cout << "Done!\n";
}

void handleErase() {
    std::cout << "Name: ";
    std::string name;
    std::getline(std::cin, name);
    if (usedNames.count(name) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    usedNames.erase(name);
    caches.erase(std::hash<std::string>{}(name));
    std::cout << "Done!\n";
}

void menu() {
    std::cout << "*******************************\n";
    std::cout << "* Cache system by nyancat0131 *\n";
    std::cout << "*******************************\n";
    std::cout << "1. Create cache\n";
    std::cout << "2. Read from cache\n";
    std::cout << "3. Write to cache\n";
    std::cout << "4. Erase cache\n";
    std::cout << "5. Exit\n";
    std::cout << "> ";
}

void alarmHandler(int sig) {
    std::cout << "Timeout!\n";
    exit(1);
}

void init_seccomp() {
    static unsigned char filter[] = {32,0,0,0,4,0,0,0,21,0,0,9,62,0,0,192,32,0,0,0,0,0,0,0,53,0,7,0,0,0,0,64,21,0,7,0,2,0,0,0,21,0,6,0,0,0,0,0,21,0,5,0,1,0,0,0,21,0,4,0,3,0,0,0,21,0,3,0,12,0,0,0,21,0,2,0,9,0,0,0,21,0,1,0,231,0,0,0,6,0,0,0,0,0,0,0,6,0,0,0,0,0,255,127};
    struct prog {
        unsigned short len;
        unsigned char *filter;
    } rule = {
        .len = sizeof(filter) >> 3,
        .filter = filter
    };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        exit(2);
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) {
        perror("prctl(PR_SET_SECCOMP)");
        exit(2);
    }
}

void setup() {
    signal(SIGALRM, alarmHandler);
    alarm(60);
    setvbuf(stdin, nullptr, _IONBF, 0);
    setvbuf(stdout, nullptr, _IONBF, 0);
    setvbuf(stderr, nullptr, _IONBF, 0);
    init_seccomp();
}

int main() {
    setup();
    for (;;) {
        menu();
        switch (readUint64()) {
        case 1:
            handleCreate();
            break;
        case 2:
            handleRead();
            break;
        case 3:
            handleWrite();
            break;
        case 4:
            handleErase();
            break;
        case 5:
            exit(0);
            break;
        default:
            std::cout << "Invalid choice!\n";
            break;
        }
    }
}
