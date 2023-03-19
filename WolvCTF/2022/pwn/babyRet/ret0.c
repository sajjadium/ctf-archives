#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void setup(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


void print_flag(void)
{
    char flag[] = "wsc{This_is_not_the_real_flag}";

    printf("%s\n", flag);
    exit(0);
}

int main(void)
{
    setup();
    char buffer0[16] = { 0 };

    printf("What is your favorite food?\n");
    scanf("%s", buffer0);
    printf("Cool.\n");

    return 1;
}
