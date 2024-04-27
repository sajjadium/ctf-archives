#include <stdio.h>
#include <stdlib.h>

#define MAX_ORNITHOPTERS 10

struct ornithopter {
    char *pilot;
    unsigned long id;
};

enum choice {
    CHANGE_PILOT = 1,
    CHANGE_ID = 2,
    FLY = 3,
    SHUTDOWN = 4
};

struct ornithopter ornithopters[300];

unsigned int read_uint(char *prompt) {
    char buf[20];
    printf("%s", prompt);
    fgets(buf, sizeof(buf), stdin);
    return atoi(buf);
}

unsigned long read_ulong(char *prompt) {
    char buf[20];
    printf("%s", prompt);
    fgets(buf, sizeof(buf), stdin);
    return atol(buf);
}

enum choice prompt(void) {
    printf("1) Change pilot\n");
    printf("2) Change id\n");
    printf("3) Fly\n");
    printf("4) Shutdown\n");

    return read_uint("> ");
}

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    printf("booting up ornithopter management mentat...\n");
    while (1) {
        unsigned int idx, len;
        unsigned long id;
        struct ornithopter *curr;

        switch (prompt()) {
        case CHANGE_PILOT:
            idx = read_uint("idx: ");
            curr = &ornithopters[idx];
            free(curr->pilot);

            len = read_uint("pilot name len: ");
            curr->pilot = malloc(len);

            printf("pilot name: ");
            fgets(curr->pilot, len, stdin);

            break;
        case CHANGE_ID:
            idx = read_uint("idx: ");
            id = read_ulong("id: ");
            ornithopters[idx].id = id;

            break;
        case FLY:
            idx = read_uint("idx: ");

            printf("ornithopter %lu has been registered for liftoff.\n", ornithopters[idx].id);
            printf("please embark after receiving appropriate authorization\n");

            break;
        default:
            goto done;
        }
    }
done:
    printf("shutting down ornithopter management mentat...\n");

    return 0;
}
