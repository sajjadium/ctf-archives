
#include <params.h>


const uint64_t pbits = 511;

const struct uint p = {{
    0x1b81b90533c6c87b, 0xc2721bf457aca835, 0x516730cc1f0b4f25, 0xa7aac6c567f35507,
    0x5afbfcc69322c9cd, 0xb42d083aedc88c42, 0xfc8ab0d15e3e4c4a, 0x65b48e8f740f89bf,
}};

/* (p+1)/prod(primes) */
const struct uint p_cofactor = {{4}};

const struct fp fp_0 = {{0}};

/* 2^512 mod p */
const struct fp fp_1 = {{
    0xc8fc8df598726f0a, 0x7b1bc81750a6af95, 0x5d319e67c1e961b4, 0xb0aa7275301955f1,
    0x4a080672d9ba6c64, 0x97a5ef8a246ee77b, 0x06ea9e5d4383676a, 0x3496e2e117e0ec80,
}};

/* (2^512)^2 mod p */
const struct fp r_squared_mod_p = {{
    0x36905b572ffc1724, 0x67086f4525f1f27d, 0x4faf3fbfd22370ca, 0x192ea214bcc584b1,
    0x5dae03ee2f5de3d0, 0x1e9248731776b371, 0xad5f166e20e4f52d, 0x4ed759aea6f3917e,
}};

/* -p^-1 mod 2^64 */
const uint64_t inv_min_p_mod_r = 0x66c1301f632e294d;

/* p - 2 */
const struct uint p_minus_2 = {{
    0x1b81b90533c6c879, 0xc2721bf457aca835, 0x516730cc1f0b4f25, 0xa7aac6c567f35507,
    0x5afbfcc69322c9cd, 0xb42d083aedc88c42, 0xfc8ab0d15e3e4c4a, 0x65b48e8f740f89bf,
}};

/* (p - 1) / 2 */
const struct uint p_minus_1_halves = {{
    0x8dc0dc8299e3643d, 0xe1390dfa2bd6541a, 0xa8b398660f85a792, 0xd3d56362b3f9aa83,
    0x2d7dfe63499164e6, 0x5a16841d76e44621, 0xfe455868af1f2625, 0x32da4747ba07c4df,
}};

/* floor(4 sqrt(p)) */
const struct uint four_sqrt_p = {{
    0x17895e71e1a20b3f, 0x38d0cd95f8636a56, 0x142b9541e59682cd, 0x856f1399d91d6592,
    0x02,
}};


/* x = 7 has full order on E0; this is 1/(7^2-1). */
const fp first_elligator_rand = {{
    0x092b3dac66979829, 0x40d0b3fc1d398d67, 0x1b2265995fae6fb7, 0x37e3979722a671ad,
    0xc8fea9978660edef, 0x91645813a4982ec0, 0x542e3af074bf6ec3, 0x273c2f8526afd895,
}};


const unsigned cost_ratio_inv_mul = 128; /* TODO figure out exactly */

