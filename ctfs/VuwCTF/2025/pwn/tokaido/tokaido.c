#include <stdio.h>

int attempts = 0;

void win() {
    puts("you win");
    if (attempts++ > 0){
        FILE *f = fopen("flag.txt", "r");
        if (f) {
            char read;
            while ((read = fgetc(f)) != EOF) {
                putchar(read);
            }
            fclose(f);
        } else {
            puts("flag file not found");
        }
    } else {
        puts("not attempted");
    }
}

int main() {
    // disable i/o buffering
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("funny number: %p\n", main);
    char buffer[16];
    gets(buffer);
    printf("You said: %s\n", buffer);
    return 0;
}