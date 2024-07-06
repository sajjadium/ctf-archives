#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/random.h>

typedef struct {
    long uid;
    char username[8];
    char password[8];
} user_t;

typedef struct user_entry user_entry_t;
struct user_entry {
    user_t* user;
    user_entry_t* prev;
    user_entry_t* next;
};

user_entry_t user_list;
long UID = 1;

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}

int menu() {
    int choice;
    puts("1. Sign up");
    puts("2. Sign in");
    puts("3. Remove account");
    puts("4. Get shell");
    printf("> ");
    scanf("%d", &choice);
    return choice;
}

void sign_up() {
    user_t* user = malloc(sizeof(user_t));
    user_entry_t* entry = malloc(sizeof(user_entry_t));
    user->uid = UID++;
    printf("username: ");
    read(0, user->username, 8);
    printf("password: ");
    read(0, user->password, 8);
    entry->user = user;

    user_entry_t* curr = &user_list;
    while(curr->next) {
        curr = curr->next;
    }
    entry->prev = curr;
    curr->next = entry;
}

void remove_account(int uid) {
    user_entry_t* curr = &user_list;
    do {
        if(curr->user->uid == uid) {
            if(curr->prev) {
                curr->prev->next = curr->next;
            }
            if(curr->next) {
                curr->next->prev = curr->prev;
            }
            free(curr->user);
            free(curr);
            break;
        }
        curr = curr->next;
    } while(curr);
}

long sign_in() {
    char username[9] = {0};
    char password[9] = {0};
    printf("username: ");
    read(0, username, 8);
    printf("password: ");
    read(0, password, 8);
    user_entry_t* curr = &user_list;
    do {
        if(memcmp(curr->user->username, username, 8) == 0 && memcmp(curr->user->password, password, 8) == 0) {
            printf("Logging in as %s\n", username);
            return curr->user->uid;
        }
        curr = curr->next;
    } while(curr);
    return -1;
}

int main() {
    init();

    long uid = -1;
    user_t root = {
        .uid = 0,
        .username = "root",
    };
    if(getrandom(root.password, 8, 0) != 8) {
        exit(1);
    }

    user_list.next = NULL;
    user_list.prev = NULL;
    user_list.user = &root;

    while(1) {
        int choice = menu();
        if(choice == 1) {
            sign_up();
        } else if(choice == 2) {
            uid = sign_in();
            if(uid == -1) {
                puts("Invalid username or password!");
            }
        } else if(choice == 3) {
            if(uid == -1) {
                puts("Please sign in first!");
            } else {
                remove_account(uid);
                uid = -1;
            }
        } else if(choice == 4) {
            if(uid == 0) {
                system("/bin/sh");
            } else {
                puts("Please sign in as root first!");
            }
        } else {
            exit(1);
        }
    }
}
