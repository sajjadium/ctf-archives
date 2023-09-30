#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char flag[256] = { 0 };

    FILE *file = fopen("/flag.txt", "r");
    if (!file) {
        return 1;
    }
    if (fread(flag, 1, 256, file) < 0) {
        return 1;
    }
    printf("%s\n", flag);
    fclose(file);
    return 0;

}