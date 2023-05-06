#ifdef MODE_CLIENT

#include "crypto.h"


static int decrypt_otp(struct apdu_decrypt_otp_s *apdu, uint8_t out[32])
{
    cx_ecfp_public_key_t pubkey;

    if (cx_ecfp_init_public_key_no_throw(CX_CURVE_256K1, apdu->public_key, 65, &pubkey) != CX_OK) {
        return -1;
    }

    return encrypt_otp_helper(&pubkey, apdu->data, out, true);
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

    case CMD_DECRYPT_OTP:
        if (lc == sizeof(struct apdu_decrypt_otp_s)) {
            ret = decrypt_otp((struct apdu_decrypt_otp_s *)data, buffer);
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
