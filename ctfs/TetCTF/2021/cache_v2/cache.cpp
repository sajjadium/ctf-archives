#include <iostream>
#include <fstream>
#include <memory>
#include <unordered_map>
#include <cstring>
#include <unistd.h>
#include <signal.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>

struct cache {
    uint8_t refCount;
    std::unique_ptr<char[]> base;
    size_t size;

    cache(size_t size) : refCount(1), size(size) {
        base = std::make_unique<char[]>(size);
        memset(base.get(), 0, size);
    }

    cache(char *data, size_t size) : refCount(1), size(size) {
        base = std::make_unique<char[]>(size);
        memcpy(base.get(), data, size);
    }

    void reference() {
        if (refCount++ > UINT8_MAX) {
            std::cout << "Too many references!\n";
            exit(1);
        }
    }

    void release() {
        if (--refCount == 0) {
            delete this;
        }
    }
};

std::unordered_map<std::string, std::pair<cache *, bool>> caches;

uint64_t readUint64() {
    std::string tmp;
    std::getline(std::cin, tmp);
    return strtoull(tmp.c_str(), nullptr, 10);
}

void handleCreate() {
    std::cout << "Cache name: ";
    std::string name;
    std::getline(std::cin, name);
    if (caches.count(name) > 0) {
        std::cout << "Cache already exists!\n";
        return;
    }
    std::cout << "Size: ";
    size_t size = readUint64();
    if (size == 0 || size > 0x1000000) {
        std::cout << "Invalid size!\n";
        return;
    }
    caches[name] = {new cache(size), false};
    std::cout << "Done!\n";
}

void handleRead() {
    std::cout << "Cache name: ";
    std::string name;
    std::getline(std::cin, name);
    if (caches.count(name) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    cache *c = caches[name].first;
    std::cout << "Offset: ";
    size_t off = readUint64();
    if (off >= c->size) {
        std::cout << "Invalid offset!\n";
        return;
    }
    std::cout << "Count: ";
    size_t n = readUint64();
    if (off + n > c->size) {
        std::cout << "Invalid offset + count!\n";
        return;
    }
    std::cout.write(c->base.get() + off, n);
    std::cout << '\n';
}

void handleWrite() {
    std::cout << "Cache name: ";
    std::string name;
    std::getline(std::cin, name);
    if (caches.count(name) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    cache *c = caches[name].first;
    std::cout << "Offset: ";
    size_t off = readUint64();
    if (off >= c->size) {
        std::cout << "Invalid offset!\n";
        return;
    }
    std::cout << "Count: ";
    size_t n = readUint64();
    if (off + n > c->size) {
        std::cout << "Invalid offset + count!\n";
        return;
    }
    std::cout << "Data: ";
    if (caches[name].second == true) {
        cache *newCache = new cache(c->base.get(), c->size);
        caches[name] = {newCache, false};
        c->release();
        c = newCache;
    }
    std::cin.read(c->base.get() + off, n);
    std::cout << "Done!\n";
}

void handleErase() {
    std::cout << "Cache name: ";
    std::string name;
    std::getline(std::cin, name);
    if (caches.count(name) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    caches[name].first->release();
    caches.erase(name);
    std::cout << "Done!\n";
}

void handleDuplicate() {
    std::cout << "Source cache name: ";
    std::string sourceName;
    std::getline(std::cin, sourceName);
    if (caches.count(sourceName) == 0) {
        std::cout << "Cache does not exist!\n";
        return;
    }
    std::cout << "New cache name: ";
    std::string destName;
    std::getline(std::cin, destName);
    if (caches.count(destName) > 0) {
        std::cout << "Cache already exists!\n";
        return;
    }
    cache *c = caches[sourceName].first;
    c->reference();
    caches[destName] = {c, true};
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
    std::cout << "5. Duplicate cache\n";
    std::cout << "6. Exit\n";
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
    alarm(300);
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
            handleDuplicate();
            break;
        case 6:
            exit(0);
            break;
        default:
            std::cout << "Invalid choice!\n";
            break;
        }
    }
}
