#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void readn(char *buf, unsigned size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned x = read(0, buf + i, 1);
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n') buf[cnt - 1] = '\x00';
}

void init() {
    alarm(60);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

char *ptr = NULL;
void create() {
    unsigned size;
    printf("size: ");
    scanf("%u", &size);
    ptr = malloc(size);
    printf("data: ");
    readn(ptr, 0x100);
}

void show() {
    printf("%s\n", ptr);
}

void delete() {
    free(ptr);
}

int main(void) {
    init();
    int select = 0;
    while (1) {
        puts("1. create");
        puts("2. show");
        puts("3. remove");
        printf("Choice: ");
        scanf("%d", &select);
        if (select == 1) {
            create();
        } else if (select == 2) {
            show();
        } else if (select == 3) {
            delete();
        } else {
            exit(-1);
        }

    }
    return 0;
}
