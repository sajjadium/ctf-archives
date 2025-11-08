#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    INVALID,
    FIBONACCI,
    ART,
    FLAG,
    RANDOM
} viewee_t;

void handle_viewee(viewee_t viewee) {
    int a, b, c;
    int i;
    FILE *file;
    char flag_char;
    switch (viewee) {
    case INVALID:
        printf("Error: Unauthorized or invalid input\n");
        break;
    case FIBONACCI:
        a = 0;
        b = 1;
        for (i = 0; i < 10; i++) {
            c = a + b;
            a = b;
            b = c;
            printf("%i: %i\n", i, a);
        }
        break;
    case ART:
        printf("  ||/\\\n"
               "  ||  \\\n"
               "  |    \\\n"
               " /______\\\n"
               "/|      |\\\n"
               " |  ||  |\n"
               " |__||__|\n");
        break;
    case FLAG:
        file = fopen("flag.txt", "r");
        while (fread(&flag_char, sizeof(flag_char), 1, file)
               == sizeof(flag_char)) {
            putchar(flag_char);
        }
        putchar('\n');
        fclose(file);
        break;
    case RANDOM:
        printf("Rand: %i\n", rand());
        break;
    }
}

int main() {
    viewee_t viewee = INVALID;
    char input[10];
    bool is_admin = false;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("What would you like to view?\n> ");
    gets(input);

    if (strcmp(input, "fibonacci") == 0) {
        viewee = FIBONACCI;
    } else if (strcmp(input, "art") == 0) {
        viewee = ART;
    } else if (strcmp(input, "flag") == 0 && is_admin) {
        viewee = FLAG;
    } else if (strcmp(input, "random") == 0) {
        viewee = RANDOM;
    }

    handle_viewee(viewee);

    return 0;
}
