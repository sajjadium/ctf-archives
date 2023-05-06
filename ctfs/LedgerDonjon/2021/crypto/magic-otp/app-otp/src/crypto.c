#include <stdlib.h>
#include <string.h>

#include "cx.h"
#include "ox.h"
#include "os_seed.h"

#include "crypto.h"


void get_own_privkey(cx_ecfp_private_key_t *privkey)
{
    uint8_t privkey_data[32];
    uint32_t path[5] = { 0x8000000d, 0x80000025, 0x80000000, 0, 0 };

    os_perso_derive_node_bip32(CX_CURVE_256K1, path, 5, privkey_data, NULL);
    cx_ecfp_init_private_key(CX_CURVE_256K1, privkey_data, sizeof(privkey_data), privkey);
    explicit_bzero(&privkey_data, sizeof(privkey_data));
}


int get_own_pubkey(cx_ecfp_public_key_t *pubkey)
{
    cx_ecfp_private_key_t privkey;
    get_own_privkey(&privkey);

    cx_err_t err = cx_ecfp_generate_pair_no_throw(CX_CURVE_256K1, pubkey, &privkey, 1);
    explicit_bzero(&privkey, sizeof(privkey));
    if (err != CX_OK) {
        return -1;
    }

    return 0;
}


int get_pubkey(uint8_t out[65])
{
    cx_ecfp_public_key_t server_pubkey;

    if (get_own_pubkey(&server_pubkey) != 0) {
        return -1;
    }

    size_t size = server_pubkey.W_len;
    if (size > 65) {
        size = 65;
    }

    memcpy(out, server_pubkey.W, size);

    return (int)size;
}


static int get_shared_secret(cx_ecfp_public_key_t *pubkey, uint8_t secret[32])
{
    cx_ecfp_private_key_t privkey;
    uint8_t out[32];
    cx_err_t ret;

    get_own_privkey(&privkey);
    ret = cx_ecdh_no_throw(&privkey, CX_ECDH_X, pubkey->W, pubkey->W_len,
                           out, sizeof(out));

    explicit_bzero(&privkey, sizeof(privkey));
    if (ret != CX_OK) {
        return -1;
    }

    memcpy(secret, out, sizeof(secret));

    return 0;
}


int encrypt_otp_helper(cx_ecfp_public_key_t *pubkey, uint8_t otp[32], uint8_t out[32], bool decrypt)
{
    uint8_t secret[32] = { 0 };
    if (get_shared_secret(pubkey, secret) != 0) {
        return -10;
    }

    cx_aes_key_t key;
    cx_err_t err = cx_aes_init_key_no_throw(secret, sizeof(secret), &key);

    explicit_bzero(secret, sizeof(secret));
    if (err != CX_OK) {
        return -11;
    }

    size_t out_len = 32;
    int flag = CX_CHAIN_CBC | CX_LAST | ((decrypt) ? CX_DECRYPT : CX_ENCRYPT);
    err = cx_aes_iv_no_throw(&key, flag, NULL, 0,
                             otp, 32, out, &out_len);

    explicit_bzero(&key, sizeof(key));
    if (err != CX_OK) {
        return -12;
    }

    return out_len;
}
