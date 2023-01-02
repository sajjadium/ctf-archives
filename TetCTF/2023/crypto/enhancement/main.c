#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "sys/random.h"
#include <secp256k1.h>


const uint8_t BASE64_ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
uint8_t BASE64_INV_ALPHABET[256];

__attribute__((constructor))
static void base64_init() {
    memset(BASE64_INV_ALPHABET, 0, sizeof BASE64_INV_ALPHABET);
    for (int i = 0; i < 64; i++) {
        BASE64_INV_ALPHABET[BASE64_ALPHABET[i]] = i;
    }
}

// base64-decoding inplace replacements.
// {'A', 'A'}           -> {'0', 'A'}
// {'A', 'A', 'A'}      -> {'0', '0', 'A'}
// {'A', 'A', 'A', 'A'} -> {'0', '0', '0', 'A'}
#define BASE64_01_TO_0(s) ((s)[0] = BASE64_INV_ALPHABET[(s)[0]] << 2 | BASE64_INV_ALPHABET[(s)[1]] >> 4)
#define BASE64_012_TO_01(s) BASE64_01_TO_0(s), (s)[1] = (BASE64_INV_ALPHABET[(s)[1]] << 4 | BASE64_INV_ALPHABET[(s)[2]] >> 2)
#define BASE64_0123_TO_012(s) BASE64_012_TO_01(s), (s)[2] = (BASE64_INV_ALPHABET[(s)[2]] << 6 | BASE64_INV_ALPHABET[(s)[3]])

// `base64_read` reads `n` bytes from stdin in base-64 format and writes to `buf`.
void base64_read(uint8_t *buf, int n) {
    while (n > 0) {
        switch (n) {
            case 1:
                // need 2
                fread(buf, 1, 2, stdin);
                BASE64_01_TO_0(buf);
                return;
            case 2:
                // need 3
                fread(buf, 1, 3, stdin);
                BASE64_012_TO_01(buf);
                return;
            default:
                // need 4
                fread(buf, 1, 4, stdin);
                BASE64_0123_TO_012(buf);
                buf += 3;
                n -= 3;
        }
    }
}

// `base64_print` print `n` bytes to stdout in base64 format
void base64_print(const uint8_t *buf, int n) {
    while (n > 0) {
        switch (n) {
            case 1:
                // print 2
                fputc(BASE64_ALPHABET[buf[0] >> 2], stdout);
                fputc(BASE64_ALPHABET[(buf[0] << 4) & 0x3f], stdout);
                return;
            case 2:
                // print 3
                fputc(BASE64_ALPHABET[buf[0] >> 2], stdout);
                fputc(BASE64_ALPHABET[(buf[0] << 4 | buf[1] >> 4) & 0x3f], stdout);
                fputc(BASE64_ALPHABET[buf[1] << 2 & 0x3f], stdout);
                return;
            default:
                // print 4
                fputc(BASE64_ALPHABET[buf[0] >> 2], stdout);
                fputc(BASE64_ALPHABET[(buf[0] << 4 | buf[1] >> 4) & 0x3f], stdout);
                fputc(BASE64_ALPHABET[(buf[1] << 2 | buf[2] >> 6) & 0x3f], stdout);
                fputc(BASE64_ALPHABET[buf[2] & 0x3f], stdout);
                buf += 3;
                n -= 3;
        }
    }
}

// `generate_nonce` tries to combine randomness from different sources to
// mitigate possible failures caused by poorly-generated, single-source
// nonce. This is currently done by XOR'ing the two input bytearrays passed
// via `data`.
int generate_nonce(
        unsigned char *nonce32,
        const unsigned char *msg32,
        const unsigned char *key32,
        const unsigned char *algo16,
        void *data,
        unsigned int attempt
) {
    uint8_t **entropy = (uint8_t **) data;
    uint8_t *user_entropy = entropy[0];
    uint8_t *system_entropy = entropy[1];
    for (int i = 0; i < 32; ++i) {
        nonce32[i] = user_entropy[i] ^ system_entropy[i];
    }
    return 1;
}


int main(void) {
    uint8_t message_hash[32];
    uint8_t private_key[32];
    uint8_t user_entropy[32];
    uint8_t system_entropy[32];
    uint8_t flag[64];
    secp256k1_ecdsa_signature signature;
    uint8_t serialized_signature[64];

    FILE *f_key = fopen("key", "r");
    fread(private_key, 1, 32, f_key);
    fclose(f_key);

    getrandom(message_hash, 32, 0);
    getrandom(system_entropy, 32, 0);
    base64_read(user_entropy, 32);
    if (memcmp(private_key, user_entropy, 32) == 0) { // private key leaked!
        FILE *f_flag = fopen("flag", "r");
        flag[fread(flag, 1, sizeof flag - 1, f_flag)] = 0;
        printf("No way... %s", flag);
        fclose(f_flag);
        return 0;
    }

    uint8_t *entropy[2] = {user_entropy, system_entropy};
    secp256k1_context *ctx = secp256k1_context_create(SECP256K1_CONTEXT_SIGN);
    secp256k1_ecdsa_sign(ctx, &signature, message_hash, private_key, generate_nonce, entropy);
    secp256k1_ecdsa_signature_serialize_compact(ctx, serialized_signature, &signature);
    secp256k1_context_destroy(ctx);

    printf("m: ");
    base64_print(message_hash, 32);
    printf("\nr: ");
    base64_print(serialized_signature, 32);
    printf("\ns: ");
    base64_print(&serialized_signature[32], 32);
    printf("\n");

    return 0;
}