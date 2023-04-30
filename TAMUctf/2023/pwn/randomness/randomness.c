#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void upkeep() {
    // Not related to the challenge, just some stuff so the remote works correctly
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    char* argv[] = {"/bin/cat", "flag.txt", NULL};
    execve(argv[0], argv, NULL);
}

void foo() {
    unsigned long seed;
    puts("Enter a seed:");
    scanf("%lu", &seed);
    srand(seed);
}

void bar() {
    unsigned long a;

    puts("Enter your guess:");
    scanf("%lu", a);

    if (rand() == a) {
        puts("correct!");
    } else {
        puts("incorrect!");
    }
}


int main() {
    upkeep();
    puts("hello!");
    foo();
    bar();
    puts("goodbye!");
}
