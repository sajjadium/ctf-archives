#include <stdio.h>
#include <stdlib.h>

char buffer[4096];

int main() {
    FILE *f = fopen("/flag", "r");
    size_t len = fread(buffer, 1, sizeof(buffer), f);
    buffer[len] = '\0';
    puts(buffer);
    fflush(stdout);
    return 0;
}
