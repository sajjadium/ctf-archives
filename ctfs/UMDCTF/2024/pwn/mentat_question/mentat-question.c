#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

void secret() {
    system("/bin/sh");
}

uint32_t calculate(uint32_t num1, uint32_t num2) {
    printf("%i\n", num1);
    printf("%i\n", num2);

    char buf[16];

    if (num2 < 1) {
        puts("Oh, I was not aware we were using negative numbers!");
        puts("Would you like to try again?");
        gets(buf);
        if (strncmp(buf, "Yes", 3) == 0) {
            fputs("Was that a ", stdout);
            printf(buf);
            fputs(" I heard?\n", stdout);
            return 0;
        } else {
            puts("I understand. Apologies, young master.");
            exit(0);
        }
    }

    return num1 / num2;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    uint32_t num1;
    uint32_t num2;
    uint32_t res = 0;

    char buf[11];
    puts("Hello young master. What would you like today?");
    fgets(buf, sizeof(buf), stdin);

    if (strncmp(buf, "Division", 8) == 0) {
        puts("Of course");
        while (res == 0) {
            puts("Which numbers would you like divided?");
            fgets(buf, sizeof(buf), stdin);
            num1 = atoi(buf);

            fgets(buf, sizeof(buf), stdin);
            getc(stdin);
            if (strncmp(buf, "0", 1) == 0) {
                puts("I'm afraid I cannot divide by zero, young master.");
                return 1;
            } else {
                num2 = atoi(buf);
            }

            res = calculate(num1, num2);
        }
    }

    return 0;
}
