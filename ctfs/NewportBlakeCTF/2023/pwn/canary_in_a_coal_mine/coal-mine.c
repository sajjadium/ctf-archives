#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

void menu() {
    puts("1. mine");
    puts("2. extract");
    puts("3. collapse");
    puts("4. abandon your friends");
    printf("> ");
}

int number() {
    int n;
    scanf("%d", &n); getchar();
    return n;
}

int main() {
    uint32_t minecarts[8];
    int choice;
    int index;
    uint32_t coal;
    uint32_t *addr;
    int depth;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    while (true) {
        menu();
        choice = number();
        switch (choice) {
            case 1:
                printf("mining position\n> ");
                addr = (uint32_t *)number();
                printf("mining depth\n> ");
                depth = number();
                coal = (uint32_t)addr;
                for (int i = 0; i < depth; i++) {
                    coal = *(uint32_t *)coal;
                }
                break;
            case 2:
                printf("minecart number\n> ");
                index = number();
                if (index >= 0) {
                    minecarts[index] = coal;
                } else {
                    printf("minecart does not exist!\n");
                }
                break;
            case 3:
                printf("collapsing mineshaft\n> ");
                gets((char *)minecarts);
                break;
            case 4:
                printf("goodbye!");
                goto done;
            default:
                printf("invalid choice...");
                break;
        }
    }

done:
    return 0;
}

void win() {
    system("/bin/sh");
}