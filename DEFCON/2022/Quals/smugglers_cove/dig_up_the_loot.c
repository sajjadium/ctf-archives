#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* args[] = { "x", "marks", "the", "spot" };

int main(int argc, char** argv) {
    const size_t num_args = sizeof(args)/sizeof(char*);
    if (argc != num_args + 1) {
        printf("Avast ye missing arguments: ./dig_up_the_loot");
        for (size_t i=0; i<num_args; i++)
            printf(" %s", args[i]);
        puts("");
        exit(0);
    }
    for (size_t i=0; i<num_args; i++) {
        if (strcmp(argv[i+1], args[i])) {
            puts("Blimey! Are missing your map?");
            exit(0);
        }
    }
    puts("Shiver me timbers! Thar be your flag: FLAG PLACEHOLDER");
}
