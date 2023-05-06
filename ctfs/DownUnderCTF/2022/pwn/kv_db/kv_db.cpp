#include <iostream>
#include <unordered_map>
#include <fcntl.h>
#include <unistd.h>
#include <string>

#define MAX_DB_SIZE 5
#define MAX_KEY_SIZE 8
#define MAX_VAL_SIZE 32

char dump[MAX_DB_SIZE * (MAX_KEY_SIZE + MAX_VAL_SIZE + 2)];
std::unordered_map<std::string, std::string> kv_db;

std::string read_n(int n) {
    std::string r;
    char c;
    for(int i = 0; i < n+1; i++) {
        if(read(0, &c, 1)) {
            if(c == '\n') break;
            r.push_back(c);
        } else {
            break;
        }
    }
    return r;
}

void init() {
    setvbuf(stdout, 0, 2, 0);

    char flag_buf[0x100];
    int fd = open("flag.txt", O_RDONLY);
    read(fd, flag_buf, 0x100);
    kv_db["flag"] = flag_buf;
}

void dump_db() {
    int l = MAX_DB_SIZE * (MAX_KEY_SIZE + MAX_VAL_SIZE + 2);
    for(int k = 0; k < l; k++) {
        dump[k] = ' ';
    }

    int i = 0;
    for(auto it = kv_db.begin(); it != kv_db.end(); it++) {
        if(it->first.find("flag") != std::string::npos) {
            continue;
        }

        it->first.copy(dump + i, it->first.size());
        i += it->first.size();

        dump[i++] = '\t';

        it->second.copy(dump + i, it->second.size());
        i += it->second.size();

        dump[i++] = '\n';
    }
}

bool set(std::string key, std::string val) {
    if(kv_db.size() == MAX_DB_SIZE) {
        return false;    
    }

    if(key.size() > MAX_KEY_SIZE || val.size() > MAX_VAL_SIZE) {
        return false;
    }

    kv_db[key] = val;
    return true;
}

std::string get(std::string key) {
    if(key.find("flag") == std::string::npos) {
        std::string val = kv_db[key];
        return val;
    } else {
        return "nope";
    }
}

void menu() {
    std::cout << "1. Get" << std::endl;
    std::cout << "2. Set" << std::endl;
    std::cout << "3. Dump" << std::endl;
    std::cout << "> ";
}

int main() {
    init();

    int choice;
    while(true) {
        menu();
        std::cin >> choice;

        if(choice == 1) {
            std::cout << "key: ";
            std::string key = read_n(MAX_KEY_SIZE);

            std::string val = get(key);

            std::cout << key << "\t" << val << std::endl;
        } else if(choice == 2) {
            std::cout << "key: ";
            std::string key = read_n(MAX_KEY_SIZE);

            std::cout << "val: ";
            std::string val = read_n(MAX_VAL_SIZE);

            bool res = set(key, val);

            std::cout << (res ? "Set successful" : "Set failed") << std::endl;
        } else if(choice == 3) {
            dump_db();

            std::cout << dump << std::endl;
        } else {
            exit(1);
        }

        std::cout << std::endl;
    }
}
