#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef ENABLE_SNAPSHOT
#define SNAPSHOT() asm volatile("int3")
#else
#define SNAPSHOT() ((void)0)
#endif

void flush() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
    };
}

void win() {
    FILE *file = fopen("/flag", "r");
    char flag[256];
    fgets(flag, 256, file);
    puts(flag);
    fclose(file);
}

void game(int *balance) {
    int wager;

    puts("> welcome to ONLINE ROULETTE");
    puts(">  - gamble as much as you want!");
    puts(">  - you have a 1-in-36 chance to double your wager! (tiny house edge so we can maintain infra costs)");
    puts(">  - enter `0` to quit the game");
    puts("");

    // something to help you
    puts("[!] minibolt has breached the system");
    SNAPSHOT();

    unsigned long addr;
    unsigned int value;

    printf("[addr]> ");
    scanf("%lx", &addr);
    if (addr > (uintptr_t)&wager) {
        puts("intruder neutralised");
    } else {
        printf("[value]> ");
        scanf("%u", &value);
        flush();

        *(unsigned char *)addr = (unsigned char)value;

        SNAPSHOT();
        puts("[!] we now return you to your regularly scheduled gambling\n");
    }

    // gambling time
    printf("wager> ");
    scanf("%d", &wager);

    while (wager != 0) {
        if (wager < 0) {
            puts("invalid wager");
            exit(0);
        }

        *balance -= wager;

        SNAPSHOT();

        int lotto = (rand() % 36) + 1;

        if (lotto == 1) {
            puts("> congrats! you won!!!\n");
            *balance += 2 * wager;
        } else {
            puts("> better luck next time!\n");
        }

        if (*balance < 0) {
            puts("damn no more money");
            return;
        }

        printf("wager> ");
        scanf("%d", &wager);
    }

    puts("> thx for the money\n");
}

int main(void) {
    srand(time(NULL));
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int balance = 10;
    char name[20];
    uint8_t name_length;

    puts("how long would you like your name to be?");
    scanf("%hhu", &name_length);
    flush();
    puts("");

    if (name_length > 20) {
        puts("bad number, get out");
        exit(0);
    }

    // play the game hrm
    game(&balance);
    flush();

    puts("please leave your name as you leave");
    printf("> ");
    fgets(name, name_length, stdin);

    // check sentinel value
    if (balance > 999999999) {
        puts("whaaaaaa u r the goat");
        win();
    }

    return 0;
}
