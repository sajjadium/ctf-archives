#include <stdio.h>
#include<stdlib.h>
#include <stdint.h>

#ifdef ENABLE_SNAPSHOT
#define SNAPSHOT() asm volatile("int3")
#else
#define SNAPSHOT() ((void)0)
#endif

#define SLOTS 7

struct gambler {
    int win;
    int numbers[SLOTS];
};

void win() {
    FILE *flag = fopen("/flag", "r");
    if (flag == NULL) {
        perror("fopen");
        return;
    }

    char line[256];

    if (fgets(line, sizeof(line), flag) == NULL) {
        puts("failed to read flag");
        fclose(flag);
        return;
    }

    fclose(flag);
    printf("%s", line);
}

void challenge(void) {
    struct gambler noob;
    noob.win = 0x67;

    int i = 0;
    int accum = 0;
    while (i != SLOTS) {
        printf("number> ");
        scanf("%d", &noob.numbers[i]);
        accum += noob.numbers[i];

        if (accum == 67) {
            puts("thats a naughty naughty number, one less chance to win");
            i++;
        }

        SNAPSHOT();
        i++;
    }

    puts("spinning the lotto of fate, lets see if you win...");
    if (noob.win == 0x67) {
        puts("rip the odds were not in your favour");
        return;
    }

    puts("wtf you win???");
    win();
    return;
}

int main(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    puts("welcome to gamble");
    puts("may the odds ever be in your favour");

    challenge();

    return 0;
}
