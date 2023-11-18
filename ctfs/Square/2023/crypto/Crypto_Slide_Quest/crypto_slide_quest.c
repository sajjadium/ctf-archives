#include "flag.h"

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    _Static_assert(sizeof(key) == 7, "Invalid key size!");

    char* output = malloc(sizeof(flag));
    strncpy(output, flag, sizeof(flag));

    int flag_len = strlen(flag);
    int key_len = strlen(key);

    for(int i = 0; i < flag_len - key_len + 1; i++) {
        for(int j = 0; j < key_len; j++) {
            output[i + j] ^= key[j];
        }
    }


    printf("%s", output);
    free(output);
    return 0;
}

