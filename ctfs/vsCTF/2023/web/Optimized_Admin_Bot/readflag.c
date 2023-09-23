#include <stdio.h>

int main() {
    FILE *file;
    int c;

    file = fopen("flag.txt", "r");
    while ((c = fgetc(file)) != EOF) {
        putchar(c);
    }
    fclose(file);

    return 0;
}
