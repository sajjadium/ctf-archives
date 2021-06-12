#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void cheat() {
    FILE *fp = fopen("flag.txt", "r");
    char flag[100];

    if (fp == NULL) {
        puts("Hmmm... I can't find my answers.");
        puts("That's not good, but at least it means you can't cheat!");
        puts("[If you are seeing this on the remote server, please contact admin].");
        exit(1);
    }

    fgets(flag, sizeof(flag), fp);
    puts(flag);
}

int main() {
    char response[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("It's math time, baby!");
    puts("WOOO I love my numbers and functions and stuff!!");
    printf("For example, here's a number: %d.\n", cheat);
    puts("What do you think about that wonderful number?");
    printf("> ");
    gets(response);

    srand(time(NULL));
    switch (rand() % 5) {
        case 0:
            puts("Hmm, that's an interesting way to look at that.");
            break;
        case 1:
            puts("Oh, but you forgot about [insert obscure math fact].");
            break;
        case 2:
            puts("Yeah, isn't that pretty cool?");
            break;
        case 3:
            puts("Well, you better like it because that's what we're learning about.");
            break;
        case 4:
            puts("Numbeerrrrrs!");
            break;
    }

    puts("Anyways, we have a test coming up.");
    puts("Be sure to study!");
}
