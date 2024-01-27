// To compile:
// git clone https://github.com/kokke/tiny-AES-c
// gcc encrypt.c tiny-AES-c/aes.c
#include "tiny-AES-c/aes.h"
#include <unistd.h>

uint8_t plaintext[16] = {0x20, 0x24};
uint8_t key[16] = {0x20, 0x24};

int main() {
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);
    AES_ECB_encrypt(&ctx, plaintext);
    write(STDOUT_FILENO, plaintext, 16);
    return 0;
}
