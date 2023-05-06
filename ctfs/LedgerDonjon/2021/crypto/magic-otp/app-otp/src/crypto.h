#pragma once

#include <stdbool.h>
#include <stdint.h>

#include "cx.h"

#define OFFSET_INS  1
#define OFFSET_LC   4
#define OFFSET_DATA 5

enum CMD {
    CMD_GET_PUBKEY,
    CMD_REGISTER_DEVICE,
    CMD_GET_REGISTERED_DEVICE_PUBKEY,
    CMD_ENCRYPT_OTP,
    CMD_DECRYPT_OTP,
};

struct apdu_register_device_s {
    uint8_t public_key[65];
    uint8_t signature[73];
    size_t signature_size;
} __attribute__((__packed__));

struct apdu_get_registered_device_pubkey_s {
    uint32_t n;
} __attribute__((__packed__));

struct apdu_encrypt_otp_s {
    uint32_t n;
    uint8_t epoch[8];
} __attribute__((__packed__));

struct apdu_decrypt_otp_s {
    uint8_t public_key[65];
    uint8_t data[32];
} __attribute__((__packed__));


void get_own_privkey(cx_ecfp_private_key_t *privkey);
int get_own_pubkey(cx_ecfp_public_key_t *pubkey);
int get_pubkey(uint8_t out[65]);
int encrypt_otp_helper(cx_ecfp_public_key_t *pubkey, uint8_t otp[32], uint8_t out[32], bool decrypt);

void init_server(void);
int handle_apdu(uint8_t *buffer, size_t size);
