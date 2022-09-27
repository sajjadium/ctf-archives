#include <linux/random.h>

unsigned int KEY1;

unsigned char SBOX[16] = { 8, 11, 14, 13, 4, 7, 2, 1, 3, 0, 5, 6, 15, 12, 9, 10 };
unsigned char PBOX[8] = { 0, 5, 7, 6, 3, 2, 1, 4 };
unsigned int RC[8] = { 0x91bb3fc1, 0x139b37ca, 0x9bccd3de, 0x37d8eae1, 0x19f8ba7c, 0x338a8b1c, 0xbad8143e, 0xd8e8bab1 };

void init_pac_encryptor(void) {
    unsigned char r_buf[8];
    get_random_bytes(r_buf, 8);
    KEY1 = *((unsigned int*)r_buf);
}

unsigned long encrypt_ptr(unsigned long ptr) {
    int i, j;
    unsigned int pt, pt_;
    unsigned long ptr_enc;
    unsigned int keys[64];

    pt = ptr & 0xffffffff;
    for(j = 0; j < 8; j++) {
        for(i = 0; i < 8; i++) {
            keys[8*j+i] = KEY1 ^ (j * RC[i] * pt);
        }
    }

    pt ^= keys[0];
    for(j = 1; j < 64; j++) {
        for(i = 0; i < 8; i++) {
            pt = (pt & (0xffffffff - (0xf << (4 * i)))) ^ (SBOX[(pt >> (4 * i)) & 0xf] << (4 * i));
        }
        pt_ = 0;
        for(i = 0; i < 8; i++) {
            pt_ ^= ((pt >> (4 * i)) & 0xf) << (4 * PBOX[i]);
        }
        pt = pt_;
        pt ^= keys[j];
    }

    ptr_enc = (((unsigned long)pt) << 32) | (ptr & 0xffffffff);

    return ptr_enc;
}

int verify_ptr(unsigned long enc_ptr) {
    unsigned long enc_ptr_;

    if(!KEY1) {
        pr_alert("pac not initialised %u\n", KEY1);
        return 0;
    }

    enc_ptr_ = encrypt_ptr(enc_ptr);

    return enc_ptr == enc_ptr_;
}
