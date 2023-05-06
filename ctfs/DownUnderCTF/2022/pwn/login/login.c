#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>


#define NUM_USERS 0x8
#define USERNAME_LEN 0x18
#define ADMIN_UID 0x1337

typedef struct {
    int uid;
    char username[USERNAME_LEN];
} *user_t;

int curr_user_id = ADMIN_UID;
user_t users[NUM_USERS];


void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

void read_n_delimited(char* buf, size_t n, char delimiter) {
    char c;
    size_t i = 0;
    while(i <= n - 1) {
        if(read(0, &c, 1) != 1) {
            break;
        }

        if(c == delimiter) {
            break;
        }

        buf[i++] = c;
    }
    buf[i] = '\0';
}

int read_int() {
    char buf[8];
    read_n_delimited(buf, 8, '\n');
    return atoi(buf);
}


void menu() {
    puts("1. Add user");
    puts("2. Login");
    printf("> ");
}

void add_user() {
    user_t user = (user_t) malloc(sizeof(user_t));
    users[curr_user_id++ - ADMIN_UID] = user;

    printf("Username length: ");
    size_t len = read_int();
    if(len > USERNAME_LEN) {
        puts("Length too large!");
        exit(1);
    }

    if(!user->uid) {
        user->uid = curr_user_id;
    }
    printf("Username: ");
    read_n_delimited(user->username, len, '\n');
}

void login() {
    int found = 0;

    char username[USERNAME_LEN];
    printf("Username: ");
    read_n_delimited(username, USERNAME_LEN, '\n');
    for(int i = 0; i < NUM_USERS; i++) {
        if(users[i] != NULL) {
            if(strncmp(users[i]->username, username, USERNAME_LEN) == 0) {
                found = 1;

                if(users[i]->uid == 0x1337) {
                    system("/bin/sh");
                } else {
                    printf("Successfully logged in! uid: 0x%x\n", users[i]->uid);
                }
            }
        }
    }

    if(!found) {
        puts("User not found");
    }
}


int main() {
    init();

    while(1) {
        menu();
        int choice = read_int();
        if(choice == 1) {
            add_user();
        } else if(choice == 2) {
            login();
        } else {
            exit(1);
        }
    }
}
