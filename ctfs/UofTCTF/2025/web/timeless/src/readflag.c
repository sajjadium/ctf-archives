#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    if (setuid(0) != 0) {
        perror("Error setting UID");
        return EXIT_FAILURE;
    }

    FILE *file = fopen("/flag.txt", "r");
    if (file == NULL) {
        perror("Error opening /flag.txt");
        return EXIT_FAILURE;
    }

    char flag[256];
    if (fgets(flag, sizeof(flag), file) != NULL) {
        printf("Flag: %s\n", flag);
    } else {
        perror("Error reading /flag.txt");
    }

    fclose(file);
    return EXIT_SUCCESS;
}