#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void koeri_crypt_init(int* data);
char* koeri_encrypt_flag();


char flag[] = "GPNCTF{fake_flag}";
char enc_flag[] = "GPNCTF{fake_flag}";
char otp[] = "GPNCTF{fake_flag}";

void koeri_crypt_init(int* data) {
    FILE* f = fopen("/dev/urandom", "r");
    fread(otp, 1, strlen(flag), f);
    fclose(f);
    for (int i = 0; i < 7; i++) {
        data[i] = otp[i];
    }
}

void koeri_crypt_scrub_flag() {
    for (int i = 0; i < strlen(flag); i++) {
        flag[i] = 'A';
    }
}

char* koeri_encrypt_flag() {
    for (int i = 0; i < strlen(flag); i++) {
        enc_flag[i] = flag[i] ^ otp[i];
    }
    enc_flag[strlen(flag)] = 0;
    return enc_flag;
}
