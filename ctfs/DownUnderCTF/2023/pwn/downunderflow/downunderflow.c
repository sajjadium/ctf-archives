#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define USERNAME_LEN 6
#define NUM_USERS 8
char logins[NUM_USERS][USERNAME_LEN] = { "user0", "user1", "user2", "user3", "user4", "user5", "user6", "admin" };

void init() {
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);
}

int read_int_lower_than(int bound) {
    int x;
    scanf("%d", &x);
    if(x >= bound) {
        puts("Invalid input!");
        exit(1);
    }
    return x;
}

int main() {
    init();

    printf("Select user to log in as: ");
    unsigned short idx = read_int_lower_than(NUM_USERS - 1);
    printf("Logging in as %s\n", logins[idx]);
    if(strncmp(logins[idx], "admin", 5) == 0) {
        puts("Welcome admin.");
        system("/bin/sh");
    } else {
        system("/bin/date");
    }
}
