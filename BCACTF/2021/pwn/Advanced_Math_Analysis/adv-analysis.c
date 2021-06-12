#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void cheat() {
    FILE *fp = fopen("flag.txt", "r");
    char flag[100];

    if (fp == NULL) {
        puts("My bad, I can't find the answers.");
        puts("Oh wait, that's a foodable offense!");
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

    puts("Welcome to the more advanced math class!");
    puts("Unlike the folks in regular analysis, you'll have to put in more effort.");
    puts("That's because this class has a strict anti-cheating defense.");
    puts("Ha, take that!");
    puts("We have to maintain the BCA reputation somehow, y'know.");
    printf("> ");
    gets(response);

    if (strcmp(response, "i pledge to not cheat")) {
        puts("I'm sorry, but you did not type out the honor pledge.");
        puts("This obviously means that you are a cheater.");
        puts("And we certainly cannot have that.");
        puts("Goodbye.");
        exit(1);
    }

    puts("Hey, I'm glad you decided to be honest and not cheat!");
    puts("Makes my life a whole lot easier when I can let my guard down.");
    puts("You still have to do tests and whatnot, but that's a you problem.");
}
