#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

FILE *flag_file;
char flag[100];

int main(void) {
    unsigned int pp;
    unsigned long my_pp;
    char buf[16];

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    printf("How much pp did you get? ");
    fgets(buf, 100, stdin);
    pp = atoi(buf);

    my_pp = pp + 1;

    printf("Any last words?\n");
    fgets(buf, 100, stdin);

    if (pp <= my_pp) {
        printf("Ha! I got %d\n", my_pp);
        printf("Maybe you'll beat me next time\n");
    } else {
        printf("What??? how did you beat me??\n");
        printf("Hmm... I'll consider giving you the flag\n");

        if (pp == 727) {
            printf("Wait, you got %d pp?\n", pp);
            printf("You can't possibly be an NPC! Here, have the flag: ");

            flag_file = fopen("flag.txt", "r");
            fgets(flag, sizeof(flag), flag_file);
            printf("%s\n", flag);
        } else {
            printf("Just kidding!\n");
        }
    }

    return 0;
}
