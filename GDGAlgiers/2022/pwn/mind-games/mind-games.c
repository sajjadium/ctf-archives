#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define BUF_SIZE 32

void flag(void);

void disable_buffering(void);

void flag(void) {
    FILE* file;
    int c = 0;

    file = fopen("flag.txt", "r");

    if (NULL == file) {
        fprintf(stderr, "Cannot open flag.txt");
        exit(EXIT_FAILURE);
    } else {
        while (1) {
            c = fgetc(file);
            if (c == EOF)
                break;
            putchar(c);
        }
        fclose(file);
    }

    return;
}

int main(int argc, char *argv[])
{
    char input[BUF_SIZE] = { '\0' };
    int randnum, guess;

    disable_buffering();

    srand(time(NULL));

    printf("You think you can read my mind? ");
    scanf("%s", input);
    guess = atoi(input);
    randnum = rand();

    if (guess == randnum) {
        flag();
    } else {
        puts("That's what I thought.");
        exit(EXIT_FAILURE);
    }

    return EXIT_SUCCESS;
}

void disable_buffering(void)
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}
