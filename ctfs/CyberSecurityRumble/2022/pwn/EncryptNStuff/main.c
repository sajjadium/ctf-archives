//
// Created by rg on 9/22/22.
//
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/random.h>

#define PLAINTEXT_LEN 32
#define CIPHERTEXT_STORE_LEN 10

int stream_ref_xor_ic(unsigned char *c, const unsigned char *m,
                  unsigned long long mlen, const unsigned char *n, uint64_t ic,
                  const unsigned char *k);

void print_hex(const uint8_t *x, size_t xlen) {
    size_t i;
    for (i = 0; i < xlen; i++) {
        printf("%02x", x[i]);
    }
    printf("\n");
}

void read_hex(char *dst, int num_bytes) {
    for (size_t count = 0; count < num_bytes; count++) {
        scanf("%2hhx", &dst[count]);
    }
}

void memzero(char *dst, size_t len) {
    explicit_bzero(dst, len);
}
#define KEYLEN 32
#define NONCE_LEN 8
#define KEYMAT_LEN 4096
void encrypt_stuff(char ct[PLAINTEXT_LEN], char pt[PLAINTEXT_LEN], int print_key) {
    unsigned char keymat[KEYMAT_LEN] = {0};
    unsigned char key[KEYLEN] = {0};
    unsigned char nonce[NONCE_LEN] = {0};
    
    getrandom(keymat, KEYMAT_LEN, GRND_RANDOM);
    memcpy(key, keymat + (rand() % (KEYMAT_LEN - KEYLEN)), KEYLEN);
    memcpy(nonce, keymat + (rand() % (KEYMAT_LEN - NONCE_LEN)), NONCE_LEN);
    
    int res = stream_ref_xor_ic(ct, pt, PLAINTEXT_LEN, nonce, 0, key);

    if (print_key) {
        printf("Key: ");
        print_hex(key, KEYLEN);
        printf("Nonce: ");
        print_hex(nonce, NONCE_LEN);
        printf("Ciphertext: ");
        print_hex(ct, PLAINTEXT_LEN);
    }

     // explicitly overwrite plaintext, key and nonce
     getrandom(key, KEYLEN, GRND_RANDOM);
     getrandom(nonce, NONCE_LEN, GRND_RANDOM);
     getrandom(keymat, KEYMAT_LEN, GRND_RANDOM);
     getrandom(pt, PLAINTEXT_LEN, GRND_RANDOM);
}

int read_flag(char *flag) {
    FILE* f = fopen("flag.txt", "r");
 
    if (NULL == f) {
        printf("flag not found!\n");
        return -1;
    } 

    if(fgets(flag, PLAINTEXT_LEN, f) == NULL){
        printf("Flag could not be read.");
        return -2;
    }
 
    fclose(f);
}

int main(void) {
    char pt[PLAINTEXT_LEN] = {0};
    unsigned char ciphertext[PLAINTEXT_LEN];
    int ciphertext_store_pos = 0, choice = 1;

    char ciphertext_store[CIPHERTEXT_STORE_LEN][PLAINTEXT_LEN]; 

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    if (read_flag(pt) < 0) {
        return EXIT_FAILURE;
    }

    encrypt_stuff(ciphertext_store[0], pt, 0);

    while (ciphertext_store_pos < CIPHERTEXT_STORE_LEN)
    {
        puts("What would you like to do?");
        puts("1: Print a ciphertext.");
        puts("2: Encrypt a plaintext.");
        scanf("%d", &choice);
        if (choice == 1) {
            puts("Which ciphertext would you like to read [0-9]?");
            scanf("%d", &choice);
            printf("Ciphertext: ");
            print_hex(ciphertext_store[choice], PLAINTEXT_LEN);
        } else if (choice == 2)
        {
            puts("Plaintext(32 bytes) pls: ");
            read(STDIN_FILENO, pt, PLAINTEXT_LEN);
            printf("Ciphertext will be stored at index %d\n", ++ciphertext_store_pos);
            encrypt_stuff(ciphertext_store[ciphertext_store_pos], pt, 1);
        } else {
            puts("Learn to type you 'tard.");
        }
        
    }
    
    printf("Plaintext(hex) pls: ");
    read_hex(pt, PLAINTEXT_LEN);

    encrypt_stuff(ciphertext, pt, 1);
    printf("Ciphertext: ");
    print_hex(ciphertext, PLAINTEXT_LEN);
}
