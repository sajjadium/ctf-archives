//! # aes_core
//! `aes_core` is the core part of AES crypto, including key scheduling, block encryption and
//! decryption.
//!
//! This module provides **low-level API**.
//!
//! In this library, AES is implemented by looking-up-tables.
//! ## Attention!
//! This low-level API does NOT provide error handling.
//!
//! Please be careful with the lengths of the slices when passing it as the parameters of a
//! function. Otherwise, it will panic at `index out of bounds` or `assertion failed`.
//! ## Block cipher
//! The AES algorithm only supports 128-bit (16 bytes) block.
//!
//! It supports 128-bit (16 bytes), 192-bit (24 bytes) and 265-bit (32 bytes) keys.
//!
//! AES block crypto uses sub-keys (aka working keys), which are derived from a key. This
//! derivation process is called *key schedule* or *key expansion*.
//!
//! key size in bits | key size in bytes | sub-keys size in 32-bit words
//! - | - | -
//! 128 | 16 | 44
//! 192 | 24 | 52
//! 256 | 32 | 60

include!(concat!(env!("OUT_DIR"), "/tables.rs"));

/// AES block size in bytes, which is 16.
pub const BLOCKSIZE_IN_BYTES: usize = 16;
/// 128bit key size in bytes, which is 16.
pub const KEY_BYTES_128BIT: usize = 16;
/// 192bit key size in bytes, which is 24.
pub const KEY_BYTES_192BIT: usize = 24;
/// 256bit key size in bytes, which is 32.
pub const KEY_BYTES_256BIT: usize = 32;
/// Sub-keys size in words (u32) from 128bit key, which is 44.
pub const N_SUBKEYS_128BIT: usize = 44;
/// Sub-keys size in words (u32) from 192bit key, which is 52.
pub const N_SUBKEYS_192BIT: usize = 52;
/// Sub-keys size in words (u32) from 256bit key, which is 60.
pub const N_SUBKEYS_256BIT: usize = 60;

// Operator precedence in Rust:
// https://doc.rust-lang.org/reference/expressions.html#expression-precedence

// Put four u8 numbers in little-endian order to get an u32 number.
// The first u8 will become the least significant bits (LSB), and the last one
// will be the most significant bits (MSB).
// To a certain extent, these are similar to `u32::from_le_bytes`.
// # Examples
// ```
// let output: u32 = four_u8_to_u32!(0x11u8, 0x22u8, 0x33u8, 0x44u8);
// assert_eq!(output, 0x44332211u32);
// ```
macro_rules! four_u8_to_u32 {
    ($b0:expr, $b1:expr, $b2:expr, $b3:expr) => {
        ($b3 as u32) << 24 | ($b2 as u32) << 16 | ($b1 as u32) << 8 | $b0 as u32
    };
}
macro_rules! u8_b3_of_u32 {
    ($w:expr) => {
        ($w >> 24) as u8
    };
}
macro_rules! u8_b2_of_u32 {
    ($w:expr) => {
        ($w >> 16) as u8
    };
}
macro_rules! u8_b1_of_u32 {
    ($w:expr) => {
        ($w >> 8) as u8
    };
}
macro_rules! u8_b0_of_u32 {
    ($w:expr) => {
        $w as u8
    };
}
macro_rules! usize_b3_of_u32 {
    ($w:expr) => {
        ($w >> 24) as usize
    };
}
macro_rules! usize_b2_of_u32 {
    ($w:expr) => {
        u8_b2_of_u32!($w) as usize
    };
}
macro_rules! usize_b1_of_u32 {
    ($w:expr) => {
        u8_b1_of_u32!($w) as usize
    };
}
macro_rules! usize_b0_of_u32 {
    ($w:expr) => {
        u8_b0_of_u32!($w) as usize
    };
}

/// The g function used in key schedule rounds.
/// aka `SubWord(RotWord(temp)) xor Rcon[i/Nk]` in NIST.FIPS.197
macro_rules! round_g_function {
    ($word:expr, $round:expr) => {
        four_u8_to_u32!(
            SBOX[usize_b1_of_u32!($word)] ^ RC[$round],
            SBOX[usize_b2_of_u32!($word)],
            SBOX[usize_b3_of_u32!($word)],
            SBOX[usize_b0_of_u32!($word)]
        )
    };
}

/// The h function used in 256bit key schedule rounds.
/// aka `SubWord(temp)` in NIST.FIPS.197
macro_rules! round_h_function {
    ($word:expr) => {
        four_u8_to_u32!(
            SBOX[usize_b0_of_u32!($word)],
            SBOX[usize_b1_of_u32!($word)],
            SBOX[usize_b2_of_u32!($word)],
            SBOX[usize_b3_of_u32!($word)]
        )
    };
}

/// 128bit key schedule
macro_rules! key_schedule_128_function {
    ($origin:ident, $subkeys:ident) => {{
        ::std::assert_eq!($subkeys.len(), N_SUBKEYS_128BIT);
        for i in 0..4 {
            $subkeys[i] = four_u8_to_u32!(
                $origin[4 * i],
                $origin[4 * i + 1],
                $origin[4 * i + 2],
                $origin[4 * i + 3]
            );
        }
        for i in 0..10 {
            $subkeys[4 * i + 4] = $subkeys[4 * i] ^ round_g_function!($subkeys[4 * i + 3], i);
            $subkeys[4 * i + 5] = $subkeys[4 * i + 1] ^ $subkeys[4 * i + 4];
            $subkeys[4 * i + 6] = $subkeys[4 * i + 2] ^ $subkeys[4 * i + 5];
            $subkeys[4 * i + 7] = $subkeys[4 * i + 3] ^ $subkeys[4 * i + 6];
        }
    }};
}

/// 192bit key schedule
macro_rules! key_schedule_192_function {
    ($origin:ident, $subkeys:ident) => {{
        ::std::assert_eq!($subkeys.len(), N_SUBKEYS_192BIT);
        for i in 0..6 {
            $subkeys[i] = four_u8_to_u32!(
                $origin[4 * i],
                $origin[4 * i + 1],
                $origin[4 * i + 2],
                $origin[4 * i + 3]
            );
        }
        for i in 0..7 {
            $subkeys[6 * i + 6] = $subkeys[6 * i] ^ round_g_function!($subkeys[6 * i + 5], i);
            $subkeys[6 * i + 7] = $subkeys[6 * i + 1] ^ $subkeys[6 * i + 6];
            $subkeys[6 * i + 8] = $subkeys[6 * i + 2] ^ $subkeys[6 * i + 7];
            $subkeys[6 * i + 9] = $subkeys[6 * i + 3] ^ $subkeys[6 * i + 8];
            $subkeys[6 * i + 10] = $subkeys[6 * i + 4] ^ $subkeys[6 * i + 9];
            $subkeys[6 * i + 11] = $subkeys[6 * i + 5] ^ $subkeys[6 * i + 10];
        }
        $subkeys[48] = $subkeys[42] ^ round_g_function!($subkeys[47], 7);
        $subkeys[49] = $subkeys[43] ^ $subkeys[48];
        $subkeys[50] = $subkeys[44] ^ $subkeys[49];
        $subkeys[51] = $subkeys[45] ^ $subkeys[50];
    }};
}

/// 256bit key schedule
macro_rules! key_schedule_256_function {
    ($origin:ident, $subkeys:ident) => {{
        ::std::assert_eq!($subkeys.len(), N_SUBKEYS_256BIT);
        for i in 0..8 {
            $subkeys[i] = four_u8_to_u32!(
                $origin[4 * i],
                $origin[4 * i + 1],
                $origin[4 * i + 2],
                $origin[4 * i + 3]
            );
        }
        for i in 0..6 {
            $subkeys[8 * i + 8] = $subkeys[8 * i] ^ round_g_function!($subkeys[8 * i + 7], i);
            $subkeys[8 * i + 9] = $subkeys[8 * i + 1] ^ $subkeys[8 * i + 8];
            $subkeys[8 * i + 10] = $subkeys[8 * i + 2] ^ $subkeys[8 * i + 9];
            $subkeys[8 * i + 11] = $subkeys[8 * i + 3] ^ $subkeys[8 * i + 10];
            $subkeys[8 * i + 12] = $subkeys[8 * i + 4] ^ round_h_function!($subkeys[8 * i + 11]);
            $subkeys[8 * i + 13] = $subkeys[8 * i + 5] ^ $subkeys[8 * i + 12];
            $subkeys[8 * i + 14] = $subkeys[8 * i + 6] ^ $subkeys[8 * i + 13];
            $subkeys[8 * i + 15] = $subkeys[8 * i + 7] ^ $subkeys[8 * i + 14];
        }
        $subkeys[56] = $subkeys[48] ^ round_g_function!($subkeys[55], 6);
        $subkeys[57] = $subkeys[49] ^ $subkeys[56];
        $subkeys[58] = $subkeys[50] ^ $subkeys[57];
        $subkeys[59] = $subkeys[51] ^ $subkeys[58];
    }};
}

/// The keys for decryption need extra transform -- the inverse MixColumn.
macro_rules! dkey_mixcolumn {
    ($subkeys:ident, $length:expr) => {{
        // The first and the last round don't need the inverse MixColumn transform
        for i in 4..($length - 4) {
            $subkeys[i] = TD0[SBOX[usize_b0_of_u32!($subkeys[i])] as usize]
                ^ TD1[SBOX[usize_b1_of_u32!($subkeys[i])] as usize]
                ^ TD2[SBOX[usize_b2_of_u32!($subkeys[i])] as usize]
                ^ TD3[SBOX[usize_b3_of_u32!($subkeys[i])] as usize];
        }
    }};
}

/// Encrypt a block.
macro_rules! encryption_function {
    ($input:ident, $output:ident, $subkeys:ident, $inner_rounds:expr, $subkeys_length:expr) => {
        // These `assert` improved performance.
        ::std::assert_eq!($output.len(), 128 / 8);
        ::std::assert_eq!($input.len(), 128 / 8);
        ::std::assert_eq!($subkeys.len(), $subkeys_length);
        let mut wa0 = four_u8_to_u32!($input[0], $input[1], $input[2], $input[3]) ^ $subkeys[0];
        let mut wa1 = four_u8_to_u32!($input[4], $input[5], $input[6], $input[7]) ^ $subkeys[1];
        let mut wa2 = four_u8_to_u32!($input[8], $input[9], $input[10], $input[11]) ^ $subkeys[2];
        let mut wa3 = four_u8_to_u32!($input[12], $input[13], $input[14], $input[15]) ^ $subkeys[3];
        // round 1
        let mut wb0 = TE0[usize_b0_of_u32!(wa0)]
            ^ TE1[usize_b1_of_u32!(wa1)]
            ^ TE2[usize_b2_of_u32!(wa2)]
            ^ TE3[usize_b3_of_u32!(wa3)]
            ^ $subkeys[4];
        let mut wb1 = TE0[usize_b0_of_u32!(wa1)]
            ^ TE1[usize_b1_of_u32!(wa2)]
            ^ TE2[usize_b2_of_u32!(wa3)]
            ^ TE3[usize_b3_of_u32!(wa0)]
            ^ $subkeys[5];
        let mut wb2 = TE0[usize_b0_of_u32!(wa2)]
            ^ TE1[usize_b1_of_u32!(wa3)]
            ^ TE2[usize_b2_of_u32!(wa0)]
            ^ TE3[usize_b3_of_u32!(wa1)]
            ^ $subkeys[6];
        let mut wb3 = TE0[usize_b0_of_u32!(wa3)]
            ^ TE1[usize_b1_of_u32!(wa0)]
            ^ TE2[usize_b2_of_u32!(wa1)]
            ^ TE3[usize_b3_of_u32!(wa2)]
            ^ $subkeys[7];
        // round 2 to round 9 (or 11, 13)
        // NOTE NOTE NOTE: I changed this
        for i in 1..$inner_rounds {
            // even-number rounds
            wa0 = TE0[usize_b0_of_u32!(wb0)]
                ^ TE1[usize_b1_of_u32!(wb1)]
                ^ TE2[usize_b2_of_u32!(wb2)]
                ^ TE3[usize_b3_of_u32!(wb3)]
                ^ $subkeys[8 * i];
            wa1 = TE0[usize_b0_of_u32!(wb1)]
                ^ TE1[usize_b1_of_u32!(wb2)]
                ^ TE2[usize_b2_of_u32!(wb3)]
                ^ TE3[usize_b3_of_u32!(wb0)]
                ^ $subkeys[8 * i + 1];
            wa2 = TE0[usize_b0_of_u32!(wb2)]
                ^ TE1[usize_b1_of_u32!(wb3)]
                ^ TE2[usize_b2_of_u32!(wb0)]
                ^ TE3[usize_b3_of_u32!(wb1)]
                ^ $subkeys[8 * i + 2];
            wa3 = TE0[usize_b0_of_u32!(wb3)]
                ^ TE1[usize_b1_of_u32!(wb0)]
                ^ TE2[usize_b2_of_u32!(wb1)]
                ^ TE3[usize_b3_of_u32!(wb2)]
                ^ $subkeys[8 * i + 3];
            // odd-number rounds
            wb0 = TE0[usize_b0_of_u32!(wa0)]
                ^ TE1[usize_b1_of_u32!(wa1)]
                ^ TE2[usize_b2_of_u32!(wa2)]
                ^ TE3[usize_b3_of_u32!(wa3)]
                ^ $subkeys[8 * i + 4];
            wb1 = TE0[usize_b0_of_u32!(wa1)]
                ^ TE1[usize_b1_of_u32!(wa2)]
                ^ TE2[usize_b2_of_u32!(wa3)]
                ^ TE3[usize_b3_of_u32!(wa0)]
                ^ $subkeys[8 * i + 5];
            wb2 = TE0[usize_b0_of_u32!(wa2)]
                ^ TE1[usize_b1_of_u32!(wa3)]
                ^ TE2[usize_b2_of_u32!(wa0)]
                ^ TE3[usize_b3_of_u32!(wa1)]
                ^ $subkeys[8 * i + 6];
            wb3 = TE0[usize_b0_of_u32!(wa3)]
                ^ TE1[usize_b1_of_u32!(wa0)]
                ^ TE2[usize_b2_of_u32!(wa1)]
                ^ TE3[usize_b3_of_u32!(wa2)]
                ^ $subkeys[8 * i + 7];
        }

        wa0 = TE0[usize_b0_of_u32!(wb0)]
            ^ TE1[usize_b1_of_u32!(wb1)]
            ^ TE2[usize_b2_of_u32!(wb2)]
            ^ TE3[usize_b3_of_u32!(wb3)]
            ^ $subkeys[$subkeys_length - 4];

        wa1 = TE0[usize_b0_of_u32!(wb1)]
            ^ TE1[usize_b1_of_u32!(wb2)]
            ^ TE2[usize_b2_of_u32!(wb3)]
            ^ TE3[usize_b3_of_u32!(wb0)]
            ^ $subkeys[$subkeys_length - 3];

        wa2 = TE0[usize_b0_of_u32!(wb2)]
            ^ TE1[usize_b1_of_u32!(wb3)]
            ^ TE2[usize_b2_of_u32!(wb0)]
            ^ TE3[usize_b3_of_u32!(wb1)]
            ^ $subkeys[$subkeys_length - 2];

        wa3 = TE0[usize_b0_of_u32!(wb3)]
            ^ TE1[usize_b1_of_u32!(wb0)]
            ^ TE2[usize_b2_of_u32!(wb1)]
            ^ TE3[usize_b3_of_u32!(wb2)]
            ^ $subkeys[$subkeys_length - 1];

        $output[0x0] = u8_b0_of_u32!(wa0);
        $output[0x1] = u8_b1_of_u32!(wa0);
        $output[0x2] = u8_b2_of_u32!(wa0);
        $output[0x3] = u8_b3_of_u32!(wa0);

        $output[0x4] = u8_b0_of_u32!(wa1);
        $output[0x5] = u8_b1_of_u32!(wa1);
        $output[0x6] = u8_b2_of_u32!(wa1);
        $output[0x7] = u8_b3_of_u32!(wa1);

        $output[0x8] = u8_b0_of_u32!(wa2);
        $output[0x9] = u8_b1_of_u32!(wa2);
        $output[0xa] = u8_b2_of_u32!(wa2);
        $output[0xb] = u8_b3_of_u32!(wa2);

        $output[0xc] = u8_b0_of_u32!(wa3);
        $output[0xd] = u8_b1_of_u32!(wa3);
        $output[0xe] = u8_b2_of_u32!(wa3);
        $output[0xf] = u8_b3_of_u32!(wa3);
    };
}

/// Decrypt a block.
macro_rules! decryption_function {
    ($input:ident, $output:ident, $subkeys:ident, $inner_rounds:expr, $subkeys_length:expr) => {{
        // These `assert` improved performance.
        ::std::assert_eq!($output.len(), 128 / 8);
        ::std::assert_eq!($input.len(), 128 / 8);
        ::std::assert_eq!($subkeys.len(), $subkeys_length);
        let mut wa0 = four_u8_to_u32!($input[0], $input[1], $input[2], $input[3])
            ^ $subkeys[$subkeys_length - 4];
        let mut wa1 = four_u8_to_u32!($input[4], $input[5], $input[6], $input[7])
            ^ $subkeys[$subkeys_length - 3];
        let mut wa2 = four_u8_to_u32!($input[8], $input[9], $input[10], $input[11])
            ^ $subkeys[$subkeys_length - 2];
        let mut wa3 = four_u8_to_u32!($input[12], $input[13], $input[14], $input[15])
            ^ $subkeys[$subkeys_length - 1];
        // round 1
        let mut wb0 = TD0[usize_b0_of_u32!(wa0)]
            ^ TD1[usize_b1_of_u32!(wa3)]
            ^ TD2[usize_b2_of_u32!(wa2)]
            ^ TD3[usize_b3_of_u32!(wa1)]
            ^ $subkeys[$subkeys_length - 8];
        let mut wb1 = TD0[usize_b0_of_u32!(wa1)]
            ^ TD1[usize_b1_of_u32!(wa0)]
            ^ TD2[usize_b2_of_u32!(wa3)]
            ^ TD3[usize_b3_of_u32!(wa2)]
            ^ $subkeys[$subkeys_length - 7];
        let mut wb2 = TD0[usize_b0_of_u32!(wa2)]
            ^ TD1[usize_b1_of_u32!(wa1)]
            ^ TD2[usize_b2_of_u32!(wa0)]
            ^ TD3[usize_b3_of_u32!(wa3)]
            ^ $subkeys[$subkeys_length - 6];
        let mut wb3 = TD0[usize_b0_of_u32!(wa3)]
            ^ TD1[usize_b1_of_u32!(wa2)]
            ^ TD2[usize_b2_of_u32!(wa1)]
            ^ TD3[usize_b3_of_u32!(wa0)]
            ^ $subkeys[$subkeys_length - 5];
        // round 2 to round 9 (or 11, 13)
        // NOTE NOTE NOTE: I changed this
        for i in 1..$inner_rounds {
            // even-number rounds
            wa0 = TD0[usize_b0_of_u32!(wb0)]
                ^ TD1[usize_b1_of_u32!(wb3)]
                ^ TD2[usize_b2_of_u32!(wb2)]
                ^ TD3[usize_b3_of_u32!(wb1)]
                ^ $subkeys[$subkeys_length - 4 - (8 * i)];
            wa1 = TD0[usize_b0_of_u32!(wb1)]
                ^ TD1[usize_b1_of_u32!(wb0)]
                ^ TD2[usize_b2_of_u32!(wb3)]
                ^ TD3[usize_b3_of_u32!(wb2)]
                ^ $subkeys[$subkeys_length - 3 - (8 * i)];
            wa2 = TD0[usize_b0_of_u32!(wb2)]
                ^ TD1[usize_b1_of_u32!(wb1)]
                ^ TD2[usize_b2_of_u32!(wb0)]
                ^ TD3[usize_b3_of_u32!(wb3)]
                ^ $subkeys[$subkeys_length - 2 - (8 * i)];
            wa3 = TD0[usize_b0_of_u32!(wb3)]
                ^ TD1[usize_b1_of_u32!(wb2)]
                ^ TD2[usize_b2_of_u32!(wb1)]
                ^ TD3[usize_b3_of_u32!(wb0)]
                ^ $subkeys[$subkeys_length - 1 - (8 * i)];
            // odd-number rounds
            wb0 = TD0[usize_b0_of_u32!(wa0)]
                ^ TD1[usize_b1_of_u32!(wa3)]
                ^ TD2[usize_b2_of_u32!(wa2)]
                ^ TD3[usize_b3_of_u32!(wa1)]
                ^ $subkeys[$subkeys_length - 8 - (8 * i)];
            wb1 = TD0[usize_b0_of_u32!(wa1)]
                ^ TD1[usize_b1_of_u32!(wa0)]
                ^ TD2[usize_b2_of_u32!(wa3)]
                ^ TD3[usize_b3_of_u32!(wa2)]
                ^ $subkeys[$subkeys_length - 7 - (8 * i)];
            wb2 = TD0[usize_b0_of_u32!(wa2)]
                ^ TD1[usize_b1_of_u32!(wa1)]
                ^ TD2[usize_b2_of_u32!(wa0)]
                ^ TD3[usize_b3_of_u32!(wa3)]
                ^ $subkeys[$subkeys_length - 6 - (8 * i)];
            wb3 = TD0[usize_b0_of_u32!(wa3)]
                ^ TD1[usize_b1_of_u32!(wa2)]
                ^ TD2[usize_b2_of_u32!(wa1)]
                ^ TD3[usize_b3_of_u32!(wa0)]
                ^ $subkeys[$subkeys_length - 5 - (8 * i)];
        }

        wa0 = TE0[usize_b0_of_u32!(wb0)]
            ^ TE1[usize_b1_of_u32!(wb1)]
            ^ TE2[usize_b2_of_u32!(wb2)]
            ^ TE3[usize_b3_of_u32!(wb3)]
            ^ $subkeys[$subkeys_length - 4];

        wa1 = TE0[usize_b0_of_u32!(wb1)]
            ^ TE1[usize_b1_of_u32!(wb2)]
            ^ TE2[usize_b2_of_u32!(wb3)]
            ^ TE3[usize_b3_of_u32!(wb0)]
            ^ $subkeys[$subkeys_length - 3];

        wa2 = TE0[usize_b0_of_u32!(wb2)]
            ^ TE1[usize_b1_of_u32!(wb3)]
            ^ TE2[usize_b2_of_u32!(wb0)]
            ^ TE3[usize_b3_of_u32!(wb1)]
            ^ $subkeys[$subkeys_length - 2];

        wa3 = TE0[usize_b0_of_u32!(wb3)]
            ^ TE1[usize_b1_of_u32!(wb0)]
            ^ TE2[usize_b2_of_u32!(wb1)]
            ^ TE3[usize_b3_of_u32!(wb2)]
            ^ $subkeys[$subkeys_length - 1];

        $output[0x0] = u8_b0_of_u32!(wa0);
        $output[0x1] = u8_b1_of_u32!(wa0);
        $output[0x2] = u8_b2_of_u32!(wa0);
        $output[0x3] = u8_b3_of_u32!(wa0);

        $output[0x4] = u8_b0_of_u32!(wa1);
        $output[0x5] = u8_b1_of_u32!(wa1);
        $output[0x6] = u8_b2_of_u32!(wa1);
        $output[0x7] = u8_b3_of_u32!(wa1);

        $output[0x8] = u8_b0_of_u32!(wa2);
        $output[0x9] = u8_b1_of_u32!(wa2);
        $output[0xa] = u8_b2_of_u32!(wa2);
        $output[0xb] = u8_b3_of_u32!(wa2);

        $output[0xc] = u8_b0_of_u32!(wa3);
        $output[0xd] = u8_b1_of_u32!(wa3);
        $output[0xe] = u8_b2_of_u32!(wa3);
        $output[0xf] = u8_b3_of_u32!(wa3);
    }};
}

/// Schedule a key to sub-keys for **encryption** with **auto-selected** key-size.
/// * *parameter* `origin`: the slice that contains original key.
/// * *parameter* `buffer`: the buffer to store the sub-keys.
///
/// The parameters must possess elements of the following amounts:
///
/// key-size | `origin` | `buffer`
/// - | - | -
/// 128bit | 16 | 44
/// 192bit | 24 | 52
/// 256bit | 32 | 60
///
/// This function is an alternative to [`key_schedule_encrypt128`], [`key_schedule_encrypt192`] and
/// [`key_schedule_encrypt256`] functions. Which one to use is up to you.
/// # Examples
/// Please refer to [`key_schedule_encrypt128`], [`key_schedule_encrypt192`] and
/// [`key_schedule_encrypt256`] functions, they are very similar.
///
/// [`key_schedule_encrypt128`]: ../aes_core/fn.key_schedule_encrypt128.html
/// [`key_schedule_encrypt192`]: ../aes_core/fn.key_schedule_encrypt192.html
/// [`key_schedule_encrypt256`]: ../aes_core/fn.key_schedule_encrypt256.html
pub fn key_schedule_encrypt_auto(origin: &[u8], buffer: &mut [u32]) {
    match origin.len() {
        KEY_BYTES_128BIT => key_schedule_128_function!(origin, buffer),
        KEY_BYTES_192BIT => key_schedule_192_function!(origin, buffer),
        KEY_BYTES_256BIT => key_schedule_256_function!(origin, buffer),
        _ => panic!("Invalid key length."),
    }
}

/// Schedule a **128bit key** to sub-keys for **encryption**.
///
/// * *parameter* `origin`: the slice (length = 16) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 44) to store the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::key_schedule_encrypt128;
/// use aes_frast::misc::hex;
/// use aes_frast::{KEY_BYTES_128BIT, N_SUBKEYS_128BIT};
///
/// // This example key came from NIST.FIPS.197 Appendix A.1
/// let origin_key: [u8; KEY_BYTES_128BIT] = [
///     0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
///     0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
///
/// key_schedule_encrypt128(&origin_key, &mut subkeys);
///
/// let expected: [u32; N_SUBKEYS_128BIT] = [
///     hex("2B7E1516"), hex("28AED2A6"), hex("ABF71588"), hex("09CF4F3C"),
///     hex("A0FAFE17"), hex("88542CB1"), hex("23A33939"), hex("2A6C7605"),
///     hex("F2C295F2"), hex("7A96B943"), hex("5935807A"), hex("7359F67F"),
///     hex("3D80477D"), hex("4716FE3E"), hex("1E237E44"), hex("6D7A883B"),
///     hex("EF44A541"), hex("A8525B7F"), hex("B671253B"), hex("DB0BAD00"),
///     hex("D4D1C6F8"), hex("7C839D87"), hex("CAF2B8BC"), hex("11F915BC"),
///     hex("6D88A37A"), hex("110B3EFD"), hex("DBF98641"), hex("CA0093FD"),
///     hex("4E54F70E"), hex("5F5FC9F3"), hex("84A64FB2"), hex("4EA6DC4F"),
///     hex("EAD27321"), hex("B58DBAD2"), hex("312BF560"), hex("7F8D292F"),
///     hex("AC7766F3"), hex("19FADC21"), hex("28D12941"), hex("575C006E"),
///     hex("D014F9A8"), hex("C9EE2589"), hex("E13F0CC8"), hex("B6630CA6"),
/// ];
/// for i in 0..N_SUBKEYS_128BIT {
///     assert_eq!(subkeys[i], expected[i]);
/// }
/// ```
pub fn key_schedule_encrypt128(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), 128 / 8);
    key_schedule_128_function!(origin, buffer);
}

/// Schedule a **192bit key** to sub-keys for **encryption**.
///
/// * *parameter* `origin`: the slice (length = 24) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 52) to store the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::key_schedule_encrypt192;
/// use aes_frast::misc::hex;
/// use aes_frast::{KEY_BYTES_192BIT, N_SUBKEYS_192BIT};
///
/// // This example key came from NIST.FIPS.197 Appendix A.2
/// let origin_key: [u8; KEY_BYTES_192BIT] = [
///     0x8E, 0x73, 0xB0, 0xF7, 0xDA, 0x0E, 0x64, 0x52,
///     0xC8, 0x10, 0xF3, 0x2B, 0x80, 0x90, 0x79, 0xE5,
///     0x62, 0xF8, 0xEA, 0xD2, 0x52, 0x2C, 0x6B, 0x7B,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
///
/// key_schedule_encrypt192(&origin_key, &mut subkeys);
///
/// let expected: [u32; N_SUBKEYS_192BIT] = [
///     hex("8E73B0F7"), hex("DA0E6452"), hex("C810F32B"), hex("809079E5"),
///     hex("62F8EAD2"), hex("522C6B7B"), hex("FE0C91F7"), hex("2402F5A5"),
///     hex("EC12068E"), hex("6C827F6B"), hex("0E7A95B9"), hex("5C56FEC2"),
///     hex("4DB7B4BD"), hex("69B54118"), hex("85A74796"), hex("E92538FD"),
///     hex("E75FAD44"), hex("BB095386"), hex("485AF057"), hex("21EFB14F"),
///     hex("A448F6D9"), hex("4D6DCE24"), hex("AA326360"), hex("113B30E6"),
///     hex("A25E7ED5"), hex("83B1CF9A"), hex("27F93943"), hex("6A94F767"),
///     hex("C0A69407"), hex("D19DA4E1"), hex("EC1786EB"), hex("6FA64971"),
///     hex("485F7032"), hex("22CB8755"), hex("E26D1352"), hex("33F0B7B3"),
///     hex("40BEEB28"), hex("2F18A259"), hex("6747D26B"), hex("458C553E"),
///     hex("A7E1466C"), hex("9411F1DF"), hex("821F750A"), hex("AD07D753"),
///     hex("CA400538"), hex("8FCC5006"), hex("282D166A"), hex("BC3CE7B5"),
///     hex("E98BA06F"), hex("448C773C"), hex("8ECC7204"), hex("01002202"),
/// ];
/// for i in 0..N_SUBKEYS_192BIT {
///     assert_eq!(subkeys[i], expected[i]);
/// }
/// ```
pub fn key_schedule_encrypt192(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), 192 / 8);
    key_schedule_192_function!(origin, buffer);
}

/// Schedule a **256bit key** to sub-keys for **encryption**.
///
/// * *parameter* `origin`: the slice (length = 32) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 60) to store the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::key_schedule_encrypt256;
/// use aes_frast::misc::hex;
/// use aes_frast::{KEY_BYTES_256BIT, N_SUBKEYS_256BIT};
///
/// // This example key came from NIST.FIPS.197 Appendix A.3
/// let origin_key: [u8; KEY_BYTES_256BIT] = [
///     0x60, 0x3D, 0xEB, 0x10, 0x15, 0xCA, 0x71, 0xBE,
///     0x2B, 0x73, 0xAE, 0xF0, 0x85, 0x7D, 0x77, 0x81,
///     0x1F, 0x35, 0x2C, 0x07, 0x3B, 0x61, 0x08, 0xD7,
///     0x2D, 0x98, 0x10, 0xA3, 0x09, 0x14, 0xDF, 0xF4,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
///
/// key_schedule_encrypt256(&origin_key, &mut subkeys);
///
/// let expected: [u32; N_SUBKEYS_256BIT] = [
///     hex("603DEB10"), hex("15CA71BE"), hex("2B73AEF0"), hex("857D7781"),
///     hex("1F352C07"), hex("3B6108D7"), hex("2D9810A3"), hex("0914DFF4"),
///     hex("9BA35411"), hex("8E6925AF"), hex("A51A8B5F"), hex("2067FCDE"),
///     hex("A8B09C1A"), hex("93D194CD"), hex("BE49846E"), hex("B75D5B9A"),
///     hex("D59AECB8"), hex("5BF3C917"), hex("FEE94248"), hex("DE8EBE96"),
///     hex("B5A9328A"), hex("2678A647"), hex("98312229"), hex("2F6C79B3"),
///     hex("812C81AD"), hex("DADF48BA"), hex("24360AF2"), hex("FAB8B464"),
///     hex("98C5BFC9"), hex("BEBD198E"), hex("268C3BA7"), hex("09E04214"),
///     hex("68007BAC"), hex("B2DF3316"), hex("96E939E4"), hex("6C518D80"),
///     hex("C814E204"), hex("76A9FB8A"), hex("5025C02D"), hex("59C58239"),
///     hex("DE136967"), hex("6CCC5A71"), hex("FA256395"), hex("9674EE15"),
///     hex("5886CA5D"), hex("2E2F31D7"), hex("7E0AF1FA"), hex("27CF73C3"),
///     hex("749C47AB"), hex("18501DDA"), hex("E2757E4F"), hex("7401905A"),
///     hex("CAFAAAE3"), hex("E4D59B34"), hex("9ADF6ACE"), hex("BD10190D"),
///     hex("FE4890D1"), hex("E6188D0B"), hex("046DF344"), hex("706C631E"),
/// ];
/// for i in 0..N_SUBKEYS_256BIT {
///     assert_eq!(subkeys[i], expected[i]);
/// }
/// ```
pub fn key_schedule_encrypt256(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), 256 / 8);
    key_schedule_256_function!(origin, buffer);
}

/// Schedule a key to sub-keys for **decryption** with **auto-selected** key-size.
/// * *parameter* `origin`: the slice that contains original key.
/// * *parameter* `buffer`: the buffer to store the sub-keys.
///
/// The parameters must possess elements of the following amounts:
///
/// key-size | `origin` | `buffer`
/// - | - | -
/// 128bit | 16 | 44
/// 192bit | 24 | 52
/// 256bit | 32 | 60
///
/// This function is an alternative to [`key_schedule_decrypt128`], [`key_schedule_decrypt192`] and
/// [`key_schedule_decrypt256`] functions. Which one to use is up to you.
/// # Examples
/// Please refer to [`key_schedule_decrypt128`], [`key_schedule_decrypt192`] and
/// [`key_schedule_decrypt256`] functions, they are very similar.
///
/// [`key_schedule_decrypt128`]: ../aes_core/fn.key_schedule_decrypt128.html
/// [`key_schedule_decrypt192`]: ../aes_core/fn.key_schedule_decrypt192.html
/// [`key_schedule_decrypt256`]: ../aes_core/fn.key_schedule_decrypt256.html
pub fn key_schedule_decrypt_auto(origin: &[u8], buffer: &mut [u32]) {
    match origin.len() {
        KEY_BYTES_128BIT => {
            key_schedule_128_function!(origin, buffer);
            dkey_mixcolumn!(buffer, N_SUBKEYS_128BIT);
        }
        KEY_BYTES_192BIT => {
            key_schedule_192_function!(origin, buffer);
            dkey_mixcolumn!(buffer, N_SUBKEYS_192BIT);
        }
        KEY_BYTES_256BIT => {
            key_schedule_256_function!(origin, buffer);
            dkey_mixcolumn!(buffer, N_SUBKEYS_256BIT);
        }
        _ => panic!("Invalid key length."),
    }
}

/// Schedule a **128bit key** to sub-keys for **decryption**.
///
/// * *parameter* `origin`: the slice (length = 16) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 44) to store the sub-keys.
/// # Examples
/// Please refer to [`key_schedule_encrypt128`] function, they are very similar.
///
/// [`key_schedule_encrypt128`]: ../aes_core/fn.key_schedule_encrypt128.html
pub fn key_schedule_decrypt128(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), KEY_BYTES_128BIT);
    key_schedule_128_function!(origin, buffer);
    dkey_mixcolumn!(buffer, N_SUBKEYS_128BIT);
}

/// Schedule a **192bit key** to sub-keys for **decryption**.
///
/// * *parameter* `origin`: the slice (length = 24) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 52) to store the sub-keys.
/// # Examples
/// Please refer to [`key_schedule_encrypt192`] function, they are very similar
///
/// [`key_schedule_encrypt192`]: ../aes_core/fn.key_schedule_encrypt192.html
pub fn key_schedule_decrypt192(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), KEY_BYTES_192BIT);
    key_schedule_192_function!(origin, buffer);
    dkey_mixcolumn!(buffer, N_SUBKEYS_192BIT);
}

/// Schedule a **256bit key** to sub-keys for **decryption**.
///
/// * *parameter* `origin`: the slice (length = 32) that contains original key.
/// * *parameter* `buffer`: the buffer (length = 60) to store the sub-keys.
/// # Examples
/// Please refer to [`key_schedule_encrypt256`] function, they are very similar
///
/// [`key_schedule_encrypt256`]: ../aes_core/fn.key_schedule_encrypt256.html
pub fn key_schedule_decrypt256(origin: &[u8], buffer: &mut [u32]) {
    assert_eq!(origin.len(), KEY_BYTES_256BIT);
    key_schedule_256_function!(origin, buffer);
    dkey_mixcolumn!(buffer, N_SUBKEYS_256BIT);
}

/// **Encrypt** a block with scheduled keys (from **128bit key**) in place.
///
/// Encrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 44) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt128, block_encrypt128_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_128BIT, N_SUBKEYS_128BIT};
///
/// // This example came from NIST.FIPS.197 Appendix B
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
///     0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34,
/// ];
/// let origin_key: [u8; KEY_BYTES_128BIT] = [
///     0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
///     0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
///
/// key_schedule_encrypt128(&origin_key, &mut subkeys);
/// block_encrypt128_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x39, 0x25, 0x84, 0x1D, 0x02, 0xDC, 0x09, 0xFB,
///     0xDC, 0x11, 0x85, 0x97, 0x19, 0x6A, 0x0B, 0x32,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt128_inplace(block: &mut [u8], subkeys: &[u32]) {
    encryption_function!(block, block, subkeys, 5, N_SUBKEYS_128BIT);
}

/// **Encrypt** a block with scheduled keys (from **192bit key**) in place.
///
/// Encrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 52) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt192, block_encrypt192_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_192BIT, N_SUBKEYS_192BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.2
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// let origin_key: [u8; KEY_BYTES_192BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
///
/// key_schedule_encrypt192(&origin_key, &mut subkeys);
/// block_encrypt192_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0xDD, 0xA9, 0x7C, 0xA4, 0x86, 0x4C, 0xDF, 0xE0,
///     0x6E, 0xAF, 0x70, 0xA0, 0xEC, 0x0D, 0x71, 0x91,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt192_inplace(block: &mut [u8], subkeys: &[u32]) {
    encryption_function!(block, block, subkeys, 6, N_SUBKEYS_192BIT);
}

/// **Encrypt** a block with scheduled keys (from **256bit key**) in place.
///
/// Encrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 60) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt256, block_encrypt256_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_256BIT, N_SUBKEYS_256BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.3
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// let origin_key: [u8; KEY_BYTES_256BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
///     0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
///
/// key_schedule_encrypt256(&origin_key, &mut subkeys);
/// block_encrypt256_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x8E, 0xA2, 0xB7, 0xCA, 0x51, 0x67, 0x45, 0xBF,
///     0xEA, 0xFC, 0x49, 0x90, 0x4B, 0x49, 0x60, 0x89,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt256_inplace(block: &mut [u8], subkeys: &[u32]) {
    encryption_function!(block, block, subkeys, 7, N_SUBKEYS_256BIT);
}

/// **Decrypt** a block with scheduled keys (from **128bit key**) in place.
///
/// Decrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 44) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt128, block_decrypt128_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_128BIT, N_SUBKEYS_128BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.1
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x69, 0xC4, 0xE0, 0xD8, 0x6A, 0x7B, 0x04, 0x30,
///     0xD8, 0xCD, 0xB7, 0x80, 0x70, 0xB4, 0xC5, 0x5A,
/// ];
/// let origin_key: [u8; KEY_BYTES_128BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
///
/// key_schedule_decrypt128(&origin_key, &mut subkeys);
/// block_decrypt128_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt128_inplace(block: &mut [u8], subkeys: &[u32]) {
    decryption_function!(block, block, subkeys, 5, N_SUBKEYS_128BIT);
}

/// **Decrypt** a block with scheduled keys (from **192bit key**) in place.
///
/// Decrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 52) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt192, block_decrypt192_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_192BIT, N_SUBKEYS_192BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.2
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0xDD, 0xA9, 0x7C, 0xA4, 0x86, 0x4C, 0xDF, 0xE0,
///     0x6E, 0xAF, 0x70, 0xA0, 0xEC, 0x0D, 0x71, 0x91,
/// ];
/// let origin_key: [u8; KEY_BYTES_192BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
///
/// key_schedule_decrypt192(&origin_key, &mut subkeys);
/// block_decrypt192_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt192_inplace(block: &mut [u8], subkeys: &[u32]) {
    decryption_function!(block, block, subkeys, 6, N_SUBKEYS_192BIT);
}

/// **Decrypt** a block with scheduled keys (from **256bit key**) in place.
///
/// Decrypt the data in `block` and write it back there, using the `subkeys`.
///
/// * *parameter* `block`: the slice (length = 16) that stores a block of data.
/// * *parameter* `subkeys`: the slice (length = 60) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt256, block_decrypt256_inplace};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_256BIT, N_SUBKEYS_256BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.3
/// let mut data_buffer: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x8E, 0xA2, 0xB7, 0xCA, 0x51, 0x67, 0x45, 0xBF,
///     0xEA, 0xFC, 0x49, 0x90, 0x4B, 0x49, 0x60, 0x89,
/// ];
/// let origin_key: [u8; KEY_BYTES_256BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
///     0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
///
/// key_schedule_decrypt256(&origin_key, &mut subkeys);
/// block_decrypt256_inplace(&mut data_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(data_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt256_inplace(block: &mut [u8], subkeys: &[u32]) {
    decryption_function!(block, block, subkeys, 7, N_SUBKEYS_256BIT);
}

/// **Encrypt** a block with scheduled keys (from **128bit key**).
///
/// Encrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 44) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt128, block_encrypt128};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_128BIT, N_SUBKEYS_128BIT};
///
/// // This example came from NIST.FIPS.197 Appendix B
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D,
///     0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_128BIT] = [
///     0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6,
///     0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
///
/// key_schedule_encrypt128(&origin_key, &mut subkeys);
/// block_encrypt128(&input_data,&mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x39, 0x25, 0x84, 0x1D, 0x02, 0xDC, 0x09, 0xFB,
///     0xDC, 0x11, 0x85, 0x97, 0x19, 0x6A, 0x0B, 0x32,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt128(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    encryption_function!(input, output, subkeys, 5, N_SUBKEYS_128BIT);
}

/// **Encrypt** a block with scheduled keys (from **192bit key**).
///
/// Encrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 52) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt192, block_encrypt192};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_192BIT, N_SUBKEYS_192BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.2
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_192BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
///
/// key_schedule_encrypt192(&origin_key, &mut subkeys);
/// block_encrypt192(&input_data, &mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0xDD, 0xA9, 0x7C, 0xA4, 0x86, 0x4C, 0xDF, 0xE0,
///     0x6E, 0xAF, 0x70, 0xA0, 0xEC, 0x0D, 0x71, 0x91,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt192(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    encryption_function!(input, output, subkeys, 6, N_SUBKEYS_192BIT);
}

/// **Encrypt** a block with scheduled keys (from **256bit key**).
///
/// Encrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 60) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_encrypt256, block_encrypt256};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_256BIT, N_SUBKEYS_256BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.3
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_256BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
///     0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
///
/// key_schedule_encrypt256(&origin_key, &mut subkeys);
/// block_encrypt256(&input_data, &mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x8E, 0xA2, 0xB7, 0xCA, 0x51, 0x67, 0x45, 0xBF,
///     0xEA, 0xFC, 0x49, 0x90, 0x4B, 0x49, 0x60, 0x89,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_encrypt256(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    encryption_function!(input, output, subkeys, 7, N_SUBKEYS_256BIT);
}

/// **Decrypt** a block with scheduled keys (from **128bit key**).
///
/// Decrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 44) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt128, block_decrypt128};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_128BIT, N_SUBKEYS_128BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.1
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x69, 0xC4, 0xE0, 0xD8, 0x6A, 0x7B, 0x04, 0x30,
///     0xD8, 0xCD, 0xB7, 0x80, 0x70, 0xB4, 0xC5, 0x5A,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_128BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
///
/// key_schedule_decrypt128(&origin_key, &mut subkeys);
/// block_decrypt128(&input_data, &mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt128(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    decryption_function!(input, output, subkeys, 5, N_SUBKEYS_128BIT);
}

/// **Decrypt** a block with scheduled keys (from **192bit key**).
///
/// Decrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 52) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt192, block_decrypt192};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_192BIT, N_SUBKEYS_192BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.2
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0xDD, 0xA9, 0x7C, 0xA4, 0x86, 0x4C, 0xDF, 0xE0,
///     0x6E, 0xAF, 0x70, 0xA0, 0xEC, 0x0D, 0x71, 0x91,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_192BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
///
/// key_schedule_decrypt192(&origin_key, &mut subkeys);
/// block_decrypt192(&input_data, &mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt192(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    decryption_function!(input, output, subkeys, 6, N_SUBKEYS_192BIT);
}

/// **Decrypt** a block with scheduled keys (from **256bit key**).
///
/// Decrypt the data in `input` and write it to `output`, using the `subkeys`.
///
/// * *parameter* `input`: the slice (length = 16) that stores a block of input data.
/// * *parameter* `output`: the buffer (length = 16) to store the output data.
/// * *parameter* `subkeys`: the slice (length = 60) that contains the sub-keys.
/// # Examples
/// ```
/// use aes_frast::aes_core::{key_schedule_decrypt256, block_decrypt256};
/// use aes_frast::{BLOCKSIZE_IN_BYTES, KEY_BYTES_256BIT, N_SUBKEYS_256BIT};
///
/// // This example came from NIST.FIPS.197 Appendix C.3
/// let input_data: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x8E, 0xA2, 0xB7, 0xCA, 0x51, 0x67, 0x45, 0xBF,
///     0xEA, 0xFC, 0x49, 0x90, 0x4B, 0x49, 0x60, 0x89,
/// ];
/// let mut output_buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
///
/// let origin_key: [u8; KEY_BYTES_256BIT] = [
///     0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
///     0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
///     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
///     0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F,
/// ];
/// let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
///
/// key_schedule_decrypt256(&origin_key, &mut subkeys);
/// block_decrypt256(&input_data, &mut output_buffer, &subkeys);
///
/// let expected: [u8; BLOCKSIZE_IN_BYTES] = [
///     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
///     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF,
/// ];
/// for i in 0..BLOCKSIZE_IN_BYTES {
///     assert_eq!(output_buffer[i], expected[i]);
/// }
/// ```
pub fn block_decrypt256(input: &[u8], output: &mut [u8], subkeys: &[u32]) {
    decryption_function!(input, output, subkeys, 7, N_SUBKEYS_256BIT);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::misc::hex;

    #[test]
    fn key_schedule_decrypt128_works() {
        let origin_key: [u8; KEY_BYTES_128BIT] = [
            0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF,
            0x4F, 0x3C,
        ];
        let mut subkeys: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
        key_schedule_decrypt128(&origin_key, &mut subkeys);
        let expected: [u32; N_SUBKEYS_128BIT] = [
            hex("2B7E1516"),
            hex("28AED2A6"),
            hex("ABF71588"),
            hex("09CF4F3C"),
            hex("2B3708A7"),
            hex("F262D405"),
            hex("BC3EBDBF"),
            hex("4B617D62"),
            hex("CC7505EB"),
            hex("3E17D1EE"),
            hex("82296C51"),
            hex("C9481133"),
            hex("7C1F13F7"),
            hex("4208C219"),
            hex("C021AE48"),
            hex("0969BF7B"),
            hex("90884413"),
            hex("D280860A"),
            hex("12A12842"),
            hex("1BC89739"),
            hex("6EA30AFC"),
            hex("BC238CF6"),
            hex("AE82A4B4"),
            hex("B54A338D"),
            hex("6EFCD876"),
            hex("D2DF5480"),
            hex("7C5DF034"),
            hex("C917C3B9"),
            hex("12C07647"),
            hex("C01F22C7"),
            hex("BC42D2F3"),
            hex("7555114A"),
            hex("DF7D925A"),
            hex("1F62B09D"),
            hex("A320626E"),
            hex("D6757324"),
            hex("0C7B5A63"),
            hex("1319EAFE"),
            hex("B0398890"),
            hex("664CFBB4"),
            hex("D014F9A8"),
            hex("C9EE2589"),
            hex("E13F0CC8"),
            hex("B6630CA6"),
        ];
        for i in 0..N_SUBKEYS_128BIT {
            assert_eq!(subkeys[i], expected[i]);
        }
    }

    #[test]
    fn key_schedule_decrypt192_works() {
        let origin_key: [u8; KEY_BYTES_192BIT] = [
            0x8E, 0x73, 0xB0, 0xF7, 0xDA, 0x0E, 0x64, 0x52, 0xC8, 0x10, 0xF3, 0x2B, 0x80, 0x90,
            0x79, 0xE5, 0x62, 0xF8, 0xEA, 0xD2, 0x52, 0x2C, 0x6B, 0x7B,
        ];
        let mut subkeys: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
        key_schedule_decrypt192(&origin_key, &mut subkeys);
        let expected: [u32; N_SUBKEYS_192BIT] = [
            hex("8E73B0F7"),
            hex("DA0E6452"),
            hex("C810F32B"),
            hex("809079E5"),
            hex("9EB149C4"),
            hex("79D69C5D"),
            hex("FEB4A27C"),
            hex("EAB6D7FD"),
            hex("659763E7"),
            hex("8C817087"),
            hex("12303943"),
            hex("6BE6A51E"),
            hex("41B34544"),
            hex("AB0592B9"),
            hex("CE92F15E"),
            hex("421381D9"),
            hex("5023B89A"),
            hex("3BC51D84"),
            hex("D04B1937"),
            hex("7B4E8B8E"),
            hex("B5DC7AD0"),
            hex("F7CFFB09"),
            hex("A7EC4393"),
            hex("9C295E17"),
            hex("C5DDB7F8"),
            hex("BE933C76"),
            hex("0B4F46A6"),
            hex("FC80BDAF"),
            hex("5B6CFE3C"),
            hex("C745A02B"),
            hex("F8B9A572"),
            hex("462A9904"),
            hex("4D65DFA2"),
            hex("B1E5620D"),
            hex("EA899C31"),
            hex("2DCC3C1A"),
            hex("F3B42258"),
            hex("B59EBB5C"),
            hex("F8FB64FE"),
            hex("491E06F3"),
            hex("A3979AC2"),
            hex("8E5BA6D8"),
            hex("E12CC9E6"),
            hex("54B272BA"),
            hex("AC491644"),
            hex("E55710B7"),
            hex("46C08A75"),
            hex("C89B2CAD"),
            hex("E98BA06F"),
            hex("448C773C"),
            hex("8ECC7204"),
            hex("01002202"),
        ];
        for i in 0..N_SUBKEYS_192BIT {
            assert_eq!(subkeys[i], expected[i]);
        }
    }

    #[test]
    fn key_schedule_decrypt256_works() {
        let origin_key: [u8; KEY_BYTES_256BIT] = [
            0x60, 0x3D, 0xEB, 0x10, 0x15, 0xCA, 0x71, 0xBE, 0x2B, 0x73, 0xAE, 0xF0, 0x85, 0x7D,
            0x77, 0x81, 0x1F, 0x35, 0x2C, 0x07, 0x3B, 0x61, 0x08, 0xD7, 0x2D, 0x98, 0x10, 0xA3,
            0x09, 0x14, 0xDF, 0xF4,
        ];
        let mut subkeys: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
        key_schedule_decrypt256(&origin_key, &mut subkeys);
        let expected: [u32; N_SUBKEYS_256BIT] = [
            hex("603DEB10"),
            hex("15CA71BE"),
            hex("2B73AEF0"),
            hex("857D7781"),
            hex("8EC6BFF6"),
            hex("829CA03B"),
            hex("9E49AF7E"),
            hex("DBA96125"),
            hex("42107758"),
            hex("E9EC98F0"),
            hex("66329EA1"),
            hex("93F8858B"),
            hex("4A7459F9"),
            hex("C8E8F9C2"),
            hex("56A156BC"),
            hex("8D083799"),
            hex("6C3D6329"),
            hex("85D1FBD9"),
            hex("E3E36578"),
            hex("701BE0F3"),
            hex("54FB808B"),
            hex("9C137949"),
            hex("CAB22FF5"),
            hex("47BA186C"),
            hex("25BA3C22"),
            hex("A06BC7FB"),
            hex("4388A283"),
            hex("33934270"),
            hex("D669A733"),
            hex("4A7ADE7A"),
            hex("80C8F18F"),
            hex("C772E9E3"),
            hex("C440B289"),
            hex("642B7572"),
            hex("27A3D7F1"),
            hex("14309581"),
            hex("32526C36"),
            hex("7828B24C"),
            hex("F8E043C3"),
            hex("3F92AA20"),
            hex("34AD1E44"),
            hex("50866B36"),
            hex("7725BCC7"),
            hex("63152946"),
            hex("B668B621"),
            hex("CE40046D"),
            hex("36A047AE"),
            hex("0932ED8E"),
            hex("57C96CF6"),
            hex("074F07C0"),
            hex("706ABB07"),
            hex("137F9241"),
            hex("ADA23F49"),
            hex("63E23B24"),
            hex("55427C8A"),
            hex("5C709104"),
            hex("FE4890D1"),
            hex("E6188D0B"),
            hex("046DF344"),
            hex("706C631E"),
        ];
        for i in 0..N_SUBKEYS_256BIT {
            assert_eq!(subkeys[i], expected[i]);
        }
    }

    #[test]
    fn key_schedule_encrypt_auto_works() {
        let origin128: [u8; KEY_BYTES_128BIT] = [
            0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF,
            0x4F, 0x3C,
        ];
        let mut scheduled128a: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
        let mut scheduled128b: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
        key_schedule_encrypt_auto(&origin128, &mut scheduled128a);
        key_schedule_encrypt128(&origin128, &mut scheduled128b);
        for i in 0..N_SUBKEYS_128BIT {
            assert_eq!(scheduled128a[i], scheduled128b[i]);
        }
        let origin192: [u8; KEY_BYTES_192BIT] = [
            0x8E, 0x73, 0xB0, 0xF7, 0xDA, 0x0E, 0x64, 0x52, 0xC8, 0x10, 0xF3, 0x2B, 0x80, 0x90,
            0x79, 0xE5, 0x62, 0xF8, 0xEA, 0xD2, 0x52, 0x2C, 0x6B, 0x7B,
        ];
        let mut scheduled192a: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
        let mut scheduled192b: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
        key_schedule_encrypt_auto(&origin192, &mut scheduled192a);
        key_schedule_encrypt192(&origin192, &mut scheduled192b);
        for i in 0..N_SUBKEYS_192BIT {
            assert_eq!(scheduled192a[i], scheduled192b[i]);
        }
        let origin256: [u8; KEY_BYTES_256BIT] = [
            0x60, 0x3D, 0xEB, 0x10, 0x15, 0xCA, 0x71, 0xBE, 0x2B, 0x73, 0xAE, 0xF0, 0x85, 0x7D,
            0x77, 0x81, 0x1F, 0x35, 0x2C, 0x07, 0x3B, 0x61, 0x08, 0xD7, 0x2D, 0x98, 0x10, 0xA3,
            0x09, 0x14, 0xDF, 0xF4,
        ];
        let mut scheduled256a: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
        let mut scheduled256b: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
        key_schedule_encrypt_auto(&origin256, &mut scheduled256a);
        key_schedule_encrypt256(&origin256, &mut scheduled256b);
        for i in 0..N_SUBKEYS_256BIT {
            assert_eq!(scheduled256a[i], scheduled256b[i]);
        }
    }

    #[test]
    fn key_schedule_decrypt_auto_works() {
        let origin128: [u8; KEY_BYTES_128BIT] = [
            0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF,
            0x4F, 0x3C,
        ];
        let mut scheduled128a: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
        let mut scheduled128b: [u32; N_SUBKEYS_128BIT] = [0; N_SUBKEYS_128BIT];
        key_schedule_decrypt_auto(&origin128, &mut scheduled128a);
        key_schedule_decrypt128(&origin128, &mut scheduled128b);
        for i in 0..N_SUBKEYS_128BIT {
            assert_eq!(scheduled128a[i], scheduled128b[i]);
        }
        let origin192: [u8; KEY_BYTES_192BIT] = [
            0x8E, 0x73, 0xB0, 0xF7, 0xDA, 0x0E, 0x64, 0x52, 0xC8, 0x10, 0xF3, 0x2B, 0x80, 0x90,
            0x79, 0xE5, 0x62, 0xF8, 0xEA, 0xD2, 0x52, 0x2C, 0x6B, 0x7B,
        ];
        let mut scheduled192a: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
        let mut scheduled192b: [u32; N_SUBKEYS_192BIT] = [0; N_SUBKEYS_192BIT];
        key_schedule_decrypt_auto(&origin192, &mut scheduled192a);
        key_schedule_decrypt192(&origin192, &mut scheduled192b);
        for i in 0..N_SUBKEYS_192BIT {
            assert_eq!(scheduled192a[i], scheduled192b[i]);
        }
        let origin256: [u8; KEY_BYTES_256BIT] = [
            0x60, 0x3D, 0xEB, 0x10, 0x15, 0xCA, 0x71, 0xBE, 0x2B, 0x73, 0xAE, 0xF0, 0x85, 0x7D,
            0x77, 0x81, 0x1F, 0x35, 0x2C, 0x07, 0x3B, 0x61, 0x08, 0xD7, 0x2D, 0x98, 0x10, 0xA3,
            0x09, 0x14, 0xDF, 0xF4,
        ];
        let mut scheduled256a: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
        let mut scheduled256b: [u32; N_SUBKEYS_256BIT] = [0; N_SUBKEYS_256BIT];
        key_schedule_decrypt_auto(&origin256, &mut scheduled256a);
        key_schedule_decrypt256(&origin256, &mut scheduled256b);
        for i in 0..N_SUBKEYS_256BIT {
            assert_eq!(scheduled256a[i], scheduled256b[i]);
        }
    }
}
