#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {

    char secret[] = "brck{not_the_flag}";
    char *key = NULL;
    size_t read_length, buffer_length = 0;
    
    // Read One Time Key
    FILE *random_bytes = fopen("/dev/urandom", "r");
    read_length = getline(&key, &buffer_length, random_bytes);
    fclose(random_bytes);

    // Encrypt
    for (int i = 0; i < strlen(secret); i++)
        secret[i] = secret[i] ^ key[i%read_length];

    // Return encrypted secret
    printf("%s", secret);

    free(key);
    return 0;
}