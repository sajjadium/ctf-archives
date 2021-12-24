#ifdef MODE_SERVER

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cx.h"
#include "ox.h"
#include "os_seed.h"

#include "crypto.h"

#define MAX_PUBLIC_KEYS 8
#define OTP_SECRET      "this isn't the production OTP_SECRET"


static cx_ecfp_public_key_t public_keys[MAX_PUBLIC_KEYS];
static unsigned int n_public_keys;


void init_server(void)
{
    memset(public_keys, 0, sizeof(public_keys));
    n_public_keys = 0;
}


static void generate_otp(uint8_t epoch[8], char otp[32])
{
    uint32_t truncated_hash;
    uint8_t hmac_hash[32];
    unsigned int offset;

    cx_hmac_sha256((uint8_t *)OTP_SECRET, sizeof(OTP_SECRET)-1, epoch, 8, hmac_hash, 32);
    offset = hmac_hash[31] & 0x0f;

    truncated_hash = 0;
    truncated_hash |= (hmac_hash[offset+0] & 0x7f) << 24;
    truncated_hash |= hmac_hash[offset+1] << 16;
    truncated_hash |= hmac_hash[offset+2] << 8;
    truncated_hash |= hmac_hash[offset+3] << 0;

    explicit_bzero(hmac_hash, sizeof(hmac_hash));

    memset(otp, 0, 32);
    snprintf(otp, 32, "%010d", truncated_hash);
}


static int register_device(struct apdu_register_device_s *apdu)
{
    if (n_public_keys >= MAX_PUBLIC_KEYS) {
        return -1;
    }

    if (apdu->signature_size > sizeof(apdu->signature)) {
        return -2;
    }

    // 1. derive the OTP server pubkey
    cx_ecfp_public_key_t server_pubkey;
    if (get_own_pubkey(&server_pubkey) != 0) {
        return -3;
    }

    // 2. verify the OTP client pubkey signature
    cx_sha256_t sha256;
    uint8_t hash[32];

    cx_sha256_init(&sha256);
    cx_hash((cx_hash_t *)&sha256, CX_LAST, apdu->public_key, 65, hash, sizeof(hash));

    if (!cx_ecdsa_verify_no_throw(&server_pubkey, hash, sizeof(hash),
                                  apdu->signature, apdu->signature_size)) {
        return -4;
    }

    // 3. register the OTP client pubkey
    if (cx_ecfp_init_public_key_no_throw(CX_CURVE_256K1, apdu->public_key, 65,
                                         &public_keys[n_public_keys]) != CX_OK) {
        return -5;
    }

    n_public_keys++;

    return 0;
}


static int get_registered_device_pubkey(struct apdu_get_registered_device_pubkey_s *apdu, uint8_t out[65])
{
    if (apdu->n >= n_public_keys) {
        return -1;
    }

    size_t size = public_keys[apdu->n].W_len;
    if (size > 65) {
        size = 65;
    }

    memcpy(out, public_keys[apdu->n].W, size);

    return (int)size;
}


static int encrypt_otp(struct apdu_encrypt_otp_s *apdu, uint8_t out[32])
{
    uint8_t otp[32];

    if (apdu->n >= n_public_keys) {
        return -1;
    }

    generate_otp(apdu->epoch, (char *)otp);

    return encrypt_otp_helper(&public_keys[apdu->n], otp, out, false);
}


int handle_apdu(uint8_t *buffer, size_t size)
{
    if (size < 5) {
        return -1;
    }

    uint8_t cmd = buffer[OFFSET_INS];
    uint8_t lc = buffer[OFFSET_LC];
    uint8_t *data = &buffer[OFFSET_DATA];
    int ret = -0xff;

    switch (cmd) {
    case CMD_GET_PUBKEY:
        ret = get_pubkey(buffer);
        break;

    case CMD_REGISTER_DEVICE:
        if (lc == sizeof(struct apdu_register_device_s)) {
            ret = register_device((struct apdu_register_device_s *)data);
        }
        break;

    case CMD_GET_REGISTERED_DEVICE_PUBKEY:
        if (lc == sizeof(struct apdu_get_registered_device_pubkey_s)) {
            ret = get_registered_device_pubkey((struct apdu_get_registered_device_pubkey_s *)data, buffer);
        }
        break;

    case CMD_ENCRYPT_OTP:
        if (lc == sizeof(struct apdu_encrypt_otp_s)) {
            ret = encrypt_otp((struct apdu_encrypt_otp_s *)data, buffer);
        }
        break;

    default:
        break;
    }

    if (ret >= 0) {
        buffer[ret] = 0x9000 >> 8;
        buffer[ret + 1] = 0x9000 & 0xff;
        ret += 2;
    } else {
        buffer[0] = 0x6800 >> 8;
        buffer[1] = (-ret) & 0xff;
        ret = 2;
    }

    return ret;
}

#endif
