#include <stdio.h>
#include <stdlib.h>

void welcome() {
    char buf[16];
    printf("Enter your name: ");
    fgets(buf, sizeof(buf), stdin);
    printf("\nWelcome, %s\nIf you're super lucky, you might get a flag! ", buf);
}

int seed() {
    char msg[] = "GLHF :D";
    printf("%s\n", msg);
    int lol;
    return lol;
}

void win() {
    char flag[64] = {0};
    FILE* f = fopen("flag.txt", "r");
    fread(flag, 1, sizeof(flag), f);
    printf("Nice work! Here's the flag: %s\n", flag);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    welcome();
    srand(seed());

    int key0 = rand() == 306291429;
    int key1 = rand() == 442612432;
    int key2 = rand() == 110107425;

    if (key0 && key1 && key2) {
        win();
    } else {
        printf("Looks like you weren't lucky enough. Better luck next time!\n");
    }
}
