
#include <params.h>


const uint64_t pbits = 1020;

const struct uint p = {{
    0xdbe34c5460e36453, 0xa1d81eebbc3d344d, 0x514ba72cb8d89fd3, 0xc2cab6a0e287f1bd,
    0x642aca4d5a313709, 0x6b317c5431541f40, 0xb97c56d1de81ede5, 0x0978dbeed90a2b58,
    0x7611ad4f90441c80, 0xf811d9c419ec8329, 0x4d6c594a8ad82d2d, 0xf06de2471cf9386e,
    0x0683cf25db31ad5b, 0x216c22bc86f21a08, 0xd89dec879007ebd7, 0x0ece55ed427012a9,
}};

/* (p+1)/prod(primes) */
const struct uint p_cofactor = {{4}};

const struct fp fp_0 = {{0}};

/* 2^1024 mod p */
const struct fp fp_1 = {{
    0x65e7ee6590e6567d, 0x40a5f2587fef86d4, 0x99f9e607b99d62f2, 0x1089df50f4f8f26d,
    0x592890dd02bb585a, 0xe1b6be68b969ecb9, 0xaebe3c10395f33c3, 0x5ef9652396531f1b,
    0x28d37db76b7a1b7f, 0x86d089fa474b4a3f, 0xdbce120cc7a4fff2, 0x08b3f947137340ac,
    0x913f3e7c71b37ce5, 0xc7d1b17b09ec4577, 0x9d834aff6f7956b6, 0x044c4b3e968ec2b8,
}};

/* (2^1024)^2 mod p */
const struct fp r_squared_mod_p = {{
    0xd6b8f146ec5055af, 0x68ac5d7707ccb03a, 0x1322c9b9837dca17, 0x4f2940830c1d2b35,
    0x8c1a56e5bf96471a, 0x6cdde00636c4f801, 0x9365ec4fa327c9ac, 0xa0056a67c1de0e82,
    0x8aa6fa7e6811faa8, 0x9aad9631bb760403, 0x156b34c683839b9d, 0xa5ae047480992b2c,
    0xc124d930289048b5, 0x4f8a8344bbe56288, 0xe1a2eb1d838b8237, 0x057162f911ca93a3,
}};

/* -p^-1 mod 2^64 */
const uint64_t inv_min_p_mod_r = 0xd2c2c24160038025;

/* p - 2 */
const struct uint p_minus_2 = {{
    0xdbe34c5460e36451, 0xa1d81eebbc3d344d, 0x514ba72cb8d89fd3, 0xc2cab6a0e287f1bd,
    0x642aca4d5a313709, 0x6b317c5431541f40, 0xb97c56d1de81ede5, 0x0978dbeed90a2b58,
    0x7611ad4f90441c80, 0xf811d9c419ec8329, 0x4d6c594a8ad82d2d, 0xf06de2471cf9386e,
    0x0683cf25db31ad5b, 0x216c22bc86f21a08, 0xd89dec879007ebd7, 0x0ece55ed427012a9,
}};

/* (p - 1) / 2 */
const struct uint p_minus_1_halves = {{
    0xedf1a62a3071b229, 0xd0ec0f75de1e9a26, 0xa8a5d3965c6c4fe9, 0xe1655b507143f8de,
    0x32156526ad189b84, 0xb598be2a18aa0fa0, 0x5cbe2b68ef40f6f2, 0x04bc6df76c8515ac,
    0xbb08d6a7c8220e40, 0xfc08ece20cf64194, 0x26b62ca5456c1696, 0xf836f1238e7c9c37,
    0x0341e792ed98d6ad, 0x90b6115e43790d04, 0xec4ef643c803f5eb, 0x07672af6a1380954,
}};

/* floor(4 sqrt(p)) */
const struct uint four_sqrt_p = {{
    0xeba75c5815bb0d57, 0xfec8564a9ae457c6, 0xe362e1c2334bd738, 0x56f74a246ef0a30e,
    0x4a598c9571aeb858, 0xc5617b211ccad355, 0x4fb69e4928ccc442, 0xf643475c7915859c,
}};


/* x = 13 has full order on E0; this is 1/(13^2-1). */
const fp first_elligator_rand = {{
    0x76772bd7462e098e, 0x033927842a4ef8ca, 0x8dd67171f93933cb, 0x43504227b40cf273,
    0xa804134451bb8b56, 0xb4e02438c7bede67, 0xb0243907cc0c5fcc, 0xdc54a73b519f71d7,
    0x91570450b86802b6, 0x3c327643702ee7eb, 0x075fa6fae8a6dfbb, 0x849cc03788dac86c,
    0x3161e2f76a357e39, 0xde9c95980cda1adc, 0xd7ad843dac31842c, 0x02ef145fbd2f3eba,
}};


const unsigned cost_ratio_inv_mul = 1536; /* approximately */

