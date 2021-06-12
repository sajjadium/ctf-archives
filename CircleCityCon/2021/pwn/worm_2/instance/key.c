#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifndef ID
#define ID 0
#endif

typedef struct {
    char name[32];
    char password[32];
} User;

void auth() {
    printf("Authenticating ...\n");
    assert(setuid(ID) == 0);
    assert(setgid(ID) == 0);
    system("/bin/bash");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    User user;

    printf("Name: ");
    gets(user.name);

    if (strncmp(user.password, "p4ssw0rd", 8) == 0) {
        auth();
    } else {
        printf("Unauthorized :(\n");
    }

    return 0;
}
