#include <math.h>
#include <stdio.h>

// gcc -fno-stack-protector -lm

int main(int argc, char* argv) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char yours[8];

    printf("Check out my pecs: %p\n", fabs);
    printf("How about yours? ");
    gets(yours);
    printf("Let's see how they stack up.");

    return 0;
}
