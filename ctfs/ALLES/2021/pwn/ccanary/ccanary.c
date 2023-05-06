// clang -o ccanary ccanary.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ignore_me_init_buffering() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void canary(void) { puts("canary: *chirp* *chirp*"); }

struct data {
    char yourinput[32];
    void (*call_canary)();
    int give_flag;
};

// FIXME: this partial-overwrite mitigation sucks :/
void quotegets(char* inp) {
    *inp = '"';
    // read input
    for (; *inp != '\n';)
        *++inp = fgetc(stdin);
    // append postfix
    for (char* postfix = "\"\n- you, 2021"; *postfix; postfix++)
        *inp++ = *postfix;
    // NUL-terminate
    *inp = 0;
}

int main(void) {
    ignore_me_init_buffering();
    struct data data = {
        .yourinput = { 0 },
        .call_canary = canary,
        .give_flag = 0,
    };

    printf("quote> ");
    quotegets((char*) &data.yourinput);

    data.call_canary();
    puts("good birb!");

    puts("");
    puts((char*) &data.yourinput);

    if (data.give_flag) {
        puts("Here's the flag:");
        system("cat flag");
    }
    return 0;
}

