//! # aes_with_operation_mode
//! `aes_with_operation_mode` allows you to use AES with operation modes like CBC, CFB and so on.  
use super::aes_core::{self, BLOCKSIZE_IN_BYTES};
use std::mem;
macro_rules! select_encrypt_function {
    ($key:ident) => {
        match $key.len() {
            aes_core::N_SUBKEYS_128BIT => aes_core::block_encrypt128,
            aes_core::N_SUBKEYS_192BIT => aes_core::block_encrypt192,
            aes_core::N_SUBKEYS_256BIT => aes_core::block_encrypt256,
            _ => panic!("Invalid key length."),
        }
    };
}
macro_rules! select_decrypt_function {
    ($key:ident) => {
        match $key.len() {
            aes_core::N_SUBKEYS_128BIT => aes_core::block_decrypt128,
            aes_core::N_SUBKEYS_192BIT => aes_core::block_decrypt192,
            aes_core::N_SUBKEYS_256BIT => aes_core::block_decrypt256,
            _ => panic!("Invalid key length."),
        }
    };
}
/// ECB (Electronic Codebook) Encryption
///
/// This function encrypts a long plain from the first parameter and put the long cipher
/// into the second parameter, using the scheduled keys in the third parameter.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![ECB encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/ECB_encryption.svg/1280px-ECB_encryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode, padding_128bit};
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let mut plain: Vec<u8> = vec![0x4E, 0xFD, 0x06, 0xB2, 0xCE, 0xEE, 0x59, 0x02,
///                               0xCA, 0xE8, 0x4E, 0x58, 0xFC, 0x50, 0x92, 0x1E,
///                               0xF0, 0x8D, 0xD2, 0x30, 0xB9, 0xC4, 0x1D, 0x1C,
///                               0xD2, 0xEB, 0x88, 0x1D, 0xE7, 0x4A, 0xF7, 0x7B,
///                               0x36, 0x75, 0xA9, 0x68, 0x03, 0xB9, 0x39, 0xDF,
///                               0xFB, 0x9E, 0x80, 0x85, 0x1C, 0x73, 0x54, 0xBF,
///                               0x2A, 0xE4, 0xAD, 0x0E, 0x43, 0x58, 0xDE, 0x88,
///                               0xDF, 0xE9, 0xDF, 0xE1, 0x66, 0x3B, 0x1A, 0x7F];
/// let mut cipher = vec![0u8; length + 16];
/// let mut dec_cipher = vec![0u8; length + 16];
/// let mut o_key: Vec<u8> = vec![0xDE, 0xA6, 0xE1, 0x3A, 0x82, 0xFF, 0x95, 0x11,
///                               0x86, 0x2D, 0xC1, 0x5A, 0x8E, 0xFA, 0xBE, 0xD4,
///                               0x3B, 0x52, 0x28, 0x78, 0xE2, 0x49, 0x1F, 0x86,
///                               0x0A, 0xB6, 0xE0, 0xCD, 0xBD, 0xDD, 0xCC, 0x2E];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
/// padding_128bit::pa_pkcs7(&mut plain);
/// aes_with_operation_mode::ecb_enc(&plain, &mut cipher, &w_keys);
///
/// let expected_encrypted = vec![0x48, 0x52, 0xC9, 0xB1, 0xD0, 0x45, 0xA4, 0xC1,
///                               0x8C, 0xCF, 0x98, 0xEF, 0x57, 0x97, 0x62, 0xAC,
///                               0x1D, 0xD5, 0x1A, 0xBC, 0xF6, 0x4F, 0xED, 0xD6,
///                               0xAD, 0x18, 0x46, 0x4B, 0xED, 0x28, 0xC0, 0xC6,
///                               0x72, 0xBD, 0x54, 0x49, 0x11, 0x93, 0xE3, 0xAE,
///                               0xE8, 0x49, 0x9C, 0x84, 0x7C, 0xD5, 0x99, 0x41,
///                               0x0B, 0x5D, 0x80, 0x07, 0x6A, 0x87, 0x6F, 0xFB,
///                               0x45, 0x75, 0xE6, 0x38, 0x8A, 0x5C, 0x0D, 0x03,
///                               0xFA, 0x60, 0x15, 0x86, 0x83, 0x02, 0x2E, 0xD9,
///                               0x27, 0x56, 0x65, 0x6B, 0xFE, 0x68, 0x5F, 0xF3];
///
/// for i in 0..(length + 16) {
///     assert_eq!(expected_encrypted[i], cipher[i], "ERROR in encrypt {}", i);
/// }
///
/// aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::ecb_dec(&cipher, &mut dec_cipher, &w_keys);
/// padding_128bit::de_ansix923_pkcs7(&mut dec_cipher);
///
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i], "ERROR in decrypt {}", i);
/// }
/// ```
pub fn ecb_enc(plain: &[u8], cipher: &mut [u8], keys: &[u32]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    // `>> 4` is the same as `/ 16` and `<< 4` is the same as `* 4`.
    let block_number = plain.len() >> 4;
    let mut start = 0;
    let mut end = BLOCKSIZE_IN_BYTES;
    for i in 0..block_number {
        start = i << 4;
        end = start + BLOCKSIZE_IN_BYTES;
        encryptor(&plain[start..end], &mut cipher[start..end], keys);
    }
    cipher[start..end].to_owned()
}
/// ECB (Electronic Codebook) Decryption
///
/// This function decrypts a long cipher from the first parameter and put the long plain
/// into the second parameter, using the scheduled keys in the third parameter.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![ECB decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/ECB_decryption.svg/1280px-ECB_decryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// Please refer to the [`ecb_enc`] function, codes are included there.
///
/// [`ecb_enc`]: ../aes_with_operation_mode/fn.ecb_enc.html
pub fn ecb_dec(cipher: &[u8], plain: &mut [u8], keys: &[u32]) -> Vec<u8> {
    let decryptor = select_decrypt_function!(keys);
    let block_number = cipher.len() >> 4;
    let mut start = 0;
    let mut end = BLOCKSIZE_IN_BYTES;
    for i in 0..block_number {
        start = i << 4;
        end = start + BLOCKSIZE_IN_BYTES;
        decryptor(&cipher[start..end], &mut plain[start..end], keys);
    }
    cipher[start..end].to_owned()
}
/// CBC (Cipher Block Chaining) Encryption
///
/// This function encrypts a long plain from the first parameter and put the long cipher
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![CBC encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/1280px-CBC_encryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode, padding_128bit};
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let mut plain: Vec<u8> = vec![0x30, 0xA3, 0xBC, 0xA0, 0xBA, 0x57, 0xFB, 0x27,
///                               0x2F, 0xE2, 0x31, 0xEC, 0xBB, 0x04, 0x5E, 0x93,
///                               0x40, 0xA1, 0x19, 0xB6, 0xE2, 0x60, 0x4F, 0x74,
///                               0x0E, 0xF2, 0xC0, 0x29, 0x1B, 0xF0, 0xF9, 0x9B,
///                               0xFD, 0x90, 0xFD, 0x0D, 0x97, 0xF8, 0x9B, 0x91,
///                               0x78, 0xF4, 0x90, 0x07, 0x66, 0x6C, 0xE8, 0x11,
///                               0x5F, 0xFE, 0x6F, 0xE9, 0x4F, 0x75, 0xB0, 0xCE,
///                               0x53, 0x48, 0x92, 0xC7, 0x96, 0xD2, 0x0B, 0x3E];
/// let mut cipher = vec![0u8; length + 16];
/// let mut dec_cipher = vec![0u8; length + 16];
/// let mut o_key: Vec<u8> = vec![0x0F, 0x57, 0x9F, 0x79, 0x50, 0x99, 0x0A, 0xCE,
///                               0x66, 0x72, 0xA8, 0x17, 0x95, 0x1F, 0xF6, 0x06,
///                               0x24, 0x40, 0xDE, 0xF5, 0x08, 0xF1, 0x64, 0x34,
///                               0xD6, 0xEF, 0xEF, 0xFD, 0x26, 0x23, 0x04, 0x95];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
/// let mut iv: Vec<u8> = vec![0x04, 0x7C, 0xF3, 0xEA, 0xE1, 0x76, 0x45, 0x85,
///                            0x72, 0x52, 0x7B, 0xAA, 0x26, 0x0D, 0x65, 0xBB];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
/// padding_128bit::pa_pkcs7(&mut plain);
/// aes_with_operation_mode::cbc_enc(&plain, &mut cipher, &w_keys, &iv);
///
/// let expected_encrypted = vec![0xBE, 0xF7, 0x24, 0xED, 0xB0, 0x45, 0x0F, 0x20,
///                               0xBC, 0x8B, 0x97, 0xA4, 0x17, 0xF3, 0xC0, 0x6F,
///                               0x08, 0xF8, 0x3D, 0xF4, 0x78, 0x0E, 0xA3, 0x11,
///                               0x5C, 0xE8, 0x59, 0x8F, 0xF7, 0xD6, 0x9C, 0x54,
///                               0x83, 0x37, 0x9C, 0xE7, 0x95, 0x44, 0x78, 0x03,
///                               0xDA, 0x86, 0x6B, 0x67, 0x7D, 0x66, 0xAD, 0x48,
///                               0x7F, 0x8B, 0xF5, 0x57, 0x0C, 0xDC, 0xB0, 0x2C,
///                               0x7C, 0xB7, 0xFA, 0x1A, 0x07, 0x57, 0x94, 0x14,
///                               0x3A, 0xA4, 0xB7, 0x91, 0x76, 0x1C, 0x2F, 0xAD,
///                               0x77, 0x8E, 0x50, 0xE7, 0x03, 0xEA, 0x70, 0x2A];
///
/// for i in 0..(length + 16) {
///     assert_eq!(expected_encrypted[i], cipher[i], "ERROR in encrypt {}", i);
/// }
///
/// aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::cbc_dec(&cipher, &mut dec_cipher, &w_keys, &iv);
/// padding_128bit::de_ansix923_pkcs7(&mut dec_cipher);
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i], "ERROR in decrypt {}", i);
/// }
/// ```
pub fn cbc_enc(plain: &[u8], cipher: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    for j in 0..BLOCKSIZE_IN_BYTES {
        buffer[j] = iv[j] ^ plain[j];
    }
    encryptor(&buffer, &mut cipher[..BLOCKSIZE_IN_BYTES], keys);
    // The other blocks
    let block_number = plain.len() >> 4;
    let mut start = 0;
    for i in 1..block_number {
        start = i << 4;
        for j in 0..BLOCKSIZE_IN_BYTES {
            buffer[j] = cipher[start + j - BLOCKSIZE_IN_BYTES] ^ plain[start + j];
        }
        encryptor(
            &buffer,
            &mut cipher[start..(start + BLOCKSIZE_IN_BYTES)],
            keys,
        );
    }
    cipher[start..(start + BLOCKSIZE_IN_BYTES)].to_owned()
}
/// CBC (Cipher Block Chaining) Decryption
///
/// This function decrypts a long cipher from the first parameter and put the long plain
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![CBC decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/CBC_decryption.svg/1280px-CBC_decryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// Please refer to the [`cbc_enc`] function, codes are included there.
///
/// [`cbc_enc`]: ../aes_with_operation_mode/fn.cbc_enc.html
pub fn cbc_dec(cipher: &[u8], plain: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let decryptor = select_decrypt_function!(keys);
    let mut buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    decryptor(&cipher[..BLOCKSIZE_IN_BYTES], &mut buffer, keys);
    for j in 0..BLOCKSIZE_IN_BYTES {
        plain[j] = iv[j] ^ buffer[j];
    }
    // The other blocks
    let block_number = cipher.len() >> 4;
    let mut start = 0;
    for i in 1..block_number {
        start = i << 4;
        decryptor(
            &cipher[start..(start + BLOCKSIZE_IN_BYTES)],
            &mut buffer,
            keys,
        );
        for j in 0..BLOCKSIZE_IN_BYTES {
            plain[start + j] = cipher[start + j - BLOCKSIZE_IN_BYTES] ^ buffer[j];
        }
    }
    cipher[start..(start + BLOCKSIZE_IN_BYTES)].to_owned()
}
/// CFB (Cipher Feedback) Encryption
///
/// The feedback size is fixed to 128 bits, which is the same as block size.  
/// This mode doesn't require padding.
///
/// This function encrypts a long plain from the first parameter and put the long cipher
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![CFB encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/CFB_encryption.svg/1280px-CFB_encryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode  /* , padding_128bit */  };
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let plain: Vec<u8> = vec![0x34, 0x63, 0xD0, 0x89, 0x1D, 0x71, 0x4A, 0xB0,
///                           0x08, 0x5D, 0x22, 0xE1, 0x8B, 0xFA, 0x77, 0xF0,
///                           0xEB, 0xE4, 0xB8, 0x9E, 0xF0, 0x05, 0x32, 0x7D,
///                           0x4F, 0xBD, 0x87, 0x69, 0x75, 0x76, 0x78, 0xAA,
///                           0x3D, 0x24, 0x06, 0x0C, 0xA4, 0xA5, 0x8C, 0xA0,
///                           0x21, 0x58, 0xB8, 0xA1, 0x86, 0xAD, 0xBB, 0x6D,
///                           0x9E, 0x09, 0x1C, 0x47, 0x06, 0x25, 0x4B, 0x2E,
///                           0x30, 0x53, 0x3A, 0x5F, 0xE9, 0xDF, 0x3A, 0x90];
/// let mut cipher = vec![0u8; length];
/// let mut dec_cipher = vec![0u8; length];
/// let     o_key: Vec<u8> = vec![0x0F, 0x57, 0x9F, 0x79, 0x50, 0x99, 0x0A, 0xCE,
///                               0x66, 0x72, 0xA8, 0x17, 0x95, 0x1F, 0xF6, 0x06,
///                               0x24, 0x40, 0xDE, 0xF5, 0x08, 0xF1, 0x64, 0x34,
///                               0xD6, 0xEF, 0xEF, 0xFD, 0x26, 0x23, 0x04, 0x95];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
/// let     iv: Vec<u8> = vec![0x04, 0x7C, 0xF3, 0xEA, 0xE1, 0x76, 0x45, 0x85,
///                            0x72, 0x52, 0x7B, 0xAA, 0x26, 0x0D, 0x65, 0xBB];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::cfb_enc(&plain, &mut cipher, &w_keys, &iv);
///
/// let expected_encrypted = vec![0x9D, 0xF9, 0x3D, 0x71, 0xC1, 0x9E, 0x50, 0x22,
///                               0x36, 0x35, 0xF1, 0xB6, 0xED, 0xA6, 0x86, 0x74,
///                               0x5F, 0x34, 0xD6, 0x93, 0xA9, 0x0F, 0xFF, 0x50,
///                               0x4C, 0xE6, 0x8E, 0xC0, 0x06, 0x3F, 0x3A, 0x62,
///                               0x78, 0x9F, 0xAB, 0xB1, 0x06, 0x95, 0x64, 0xB6,
///                               0xBB, 0x06, 0x92, 0x02, 0x34, 0x2D, 0x36, 0x35,
///                               0xA4, 0x95, 0x30, 0x2E, 0x20, 0xD3, 0xE8, 0x53,
///                               0x95, 0xA2, 0xDF, 0x83, 0x9B, 0x7B, 0x12, 0x3F];
///
/// for i in 0..length {
///     assert_eq!(expected_encrypted[i], cipher[i], "ERROR in encrypt {}", i);
/// }
///
/// // Notice: CFB only uses block-encryption, no matter we use it as encryption or decryption.
/// // So, keep don't use functions which start with`key_schedule_decrypt_` and keep the next line commented out.
/// //aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::cfb_dec(&cipher, &mut dec_cipher, &w_keys, &iv);
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i], "ERROR in decrypt {}", i);
/// }
/// ```
pub fn cfb_enc(plain: &[u8], cipher: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
    // If input has only one block, consider it as the last block, not the 1st.
    // If input has only two blocks, consider it has no middle blocks.
    // The 1st (head) block
    encryptor(iv, &mut buffer, keys);
    let block_number = plain.len() >> 4;
    let mut start = 0;
    if plain.len() >= BLOCKSIZE_IN_BYTES {
        for j in 0..BLOCKSIZE_IN_BYTES {
            cipher[j] = buffer[j] ^ plain[j];
        }
        // The middle blocks
        for i in 1..block_number {
            start = i << 4;
            encryptor(
                &cipher[(start - BLOCKSIZE_IN_BYTES)..start],
                &mut buffer,
                keys,
            );
            for j in 0..BLOCKSIZE_IN_BYTES {
                cipher[start + j] = buffer[j] ^ plain[start + j];
            }
        }
    }
    // The last (tail) block
    match plain.len() & 0b1111 {
        r if r != 0 => {
            if block_number != 0 {
                start = block_number << 4;
                encryptor(
                    &cipher[(start - BLOCKSIZE_IN_BYTES)..start],
                    &mut buffer,
                    keys,
                );
            }
            for j in 0..r {
                cipher[start + j] = buffer[j] ^ plain[start + j];
            }
            cipher[start..(start + r)].to_owned()
        }
        _ => cipher[start..(start + BLOCKSIZE_IN_BYTES)].to_owned(),
    }
}
/// CFB (Cipher Feedback) Decryption
///
/// The feedback size is fixed to 128 bits, which is the same as block size.  
/// This mode doesn't require padding.
///
/// This function decrypts a long cipher from the first parameter and put the long plain
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the final block of the cipher (NOT the plain).  
/// ![CFB decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/CFB_decryption.svg/1280px-CFB_decryption.svg.png)
/// (This picture comes from the Wikimedia Commons)
/// # Examples
/// Please refer to the [`cfb_enc`] function, codes are included there.
///
/// [`cfb_enc`]: ../aes_with_operation_mode/fn.cfb_enc.html
pub fn cfb_dec(cipher: &[u8], plain: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    // You may think this function is the same as the `cfb_enc` function, but in fact they differ
    // in the last line. Both functions return `&cipher[start..(start + BLOCKSIZE_IN_BYTES)]`, which is the first
    // parameter in this function, while it's the second parameter in the `cfb_enc` function.
    let encryptor = select_encrypt_function!(keys);
    let mut buffer: [u8; BLOCKSIZE_IN_BYTES] = [0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    encryptor(iv, &mut buffer, keys);
    let block_number = plain.len() >> 4;
    let mut start = 0;
    if cipher.len() >= BLOCKSIZE_IN_BYTES {
        for j in 0..BLOCKSIZE_IN_BYTES {
            plain[j] = buffer[j] ^ cipher[j]
        }
        // The middle blocks
        for i in 1usize..block_number {
            start = i << 4;
            encryptor(
                &cipher[(start - BLOCKSIZE_IN_BYTES)..start],
                &mut buffer,
                keys,
            );
            for j in 0..BLOCKSIZE_IN_BYTES {
                plain[start + j] = buffer[j] ^ cipher[start + j];
            }
        }
    }
    match cipher.len() & 0b1111 {
        // The last (tail) block
        r if r != 0 => {
            if block_number != 0 {
                start = block_number << 4;
                encryptor(
                    &cipher[(start - BLOCKSIZE_IN_BYTES)..start],
                    &mut buffer,
                    keys,
                );
            }
            for j in 0..r {
                plain[start + j] = buffer[j] ^ cipher[start + j];
            }
            cipher[start..(start + r)].to_owned()
        }
        _ => cipher[start..(start + BLOCKSIZE_IN_BYTES)].to_owned(),
    }
}
/// OFB (Output Feedback) Encryption and Decryption
///
/// The feedback size is fixed to 128 bits, which is the same as block size.  
/// This mode doesn't require depadding if you didn't add padding when encrypting.
///
/// This function encrypts a long plain from the first parameter and put the long cipher
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// However, if you use the corresponding [`key_schedule_decrypt_auto`], [`key_schedule_decrypt128`], [`key_schedule_decrypt192`]
/// or [`key_schedule_decrypt256`] function to schedule the keys, and then use this function again,
/// it will decrypt the first parameter into the second parameter.  
/// Finally, it returns the final block of the encryptor output (neither the plain nor cipher).  
/// ![OFB encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/OFB_encryption.svg/1280px-OFB_encryption.svg.png)
/// ![OFB decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/OFB_decryption.svg/1280px-OFB_decryption.svg.png)
/// (These pictures comes from the Wikimedia Commons)
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode, padding_128bit};
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let mut plain: Vec<u8> = vec![0x34, 0x63, 0xD0, 0x89, 0x1D, 0x71, 0x4A, 0xB0,
///                               0x08, 0x5D, 0x22, 0xE1, 0x8B, 0xFA, 0x77, 0xF0,
///                               0xEB, 0xE4, 0xB8, 0x9E, 0xF0, 0x05, 0x32, 0x7D,
///                               0x4F, 0xBD, 0x87, 0x69, 0x75, 0x76, 0x78, 0xAA,
///                               0x3D, 0x24, 0x06, 0x0C, 0xA4, 0xA5, 0x8C, 0xA0,
///                               0x21, 0x58, 0xB8, 0xA1, 0x86, 0xAD, 0xBB, 0x6D,
///                               0x9E, 0x09, 0x1C, 0x47, 0x06, 0x25, 0x4B, 0x2E,
///                               0x30, 0x53, 0x3A, 0x5F, 0xE9, 0xDF, 0x3A, 0x90];
/// let mut cipher = vec![0u8; length];
/// let mut dec_cipher = vec![0u8; length];
/// let mut o_key: Vec<u8> = vec![0x0F, 0x57, 0x9F, 0x79, 0x50, 0x99, 0x0A, 0xCE,
///                               0x66, 0x72, 0xA8, 0x17, 0x95, 0x1F, 0xF6, 0x06,
///                               0x24, 0x40, 0xDE, 0xF5, 0x08, 0xF1, 0x64, 0x34,
///                               0xD6, 0xEF, 0xEF, 0xFD, 0x26, 0x23, 0x04, 0x95];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
/// let mut iv: Vec<u8> = vec![0x04, 0x7C, 0xF3, 0xEA, 0xE1, 0x76, 0x45, 0x85,
///                            0x72, 0x52, 0x7B, 0xAA, 0x26, 0x0D, 0x65, 0xBB];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::ofb_enc_dec(&plain, &mut cipher, &w_keys, &iv);
///
/// let expected_encrypted = vec![0x9D, 0xF9, 0x3D, 0x71, 0xC1, 0x9E, 0x50, 0x22,
///                               0x36, 0x35, 0xF1, 0xB6, 0xED, 0xA6, 0x86, 0x74,
///                               0xE2, 0xB7, 0xA6, 0x41, 0x13, 0x87, 0xAB, 0x99,
///                               0x74, 0xE0, 0xF9, 0x9B, 0xC9, 0x05, 0xCE, 0x63,
///                               0x74, 0x54, 0x68, 0x8D, 0x7B, 0xDA, 0x6E, 0x9E,
///                               0xF6, 0xA6, 0x12, 0xB3, 0xB3, 0x06, 0x79, 0x68,
///                               0x62, 0x2E, 0x5A, 0xF9, 0x03, 0xE3, 0x5D, 0xEF,
///                               0xA2, 0x4B, 0xA8, 0xC1, 0xD7, 0xEC, 0x3E, 0x1B];
///
/// for i in 0..length {
///     assert_eq!(expected_encrypted[i], cipher[i], "ERROR in encrypt {}", i);
/// }
///
/// // Notice: OFB only uses block-encryption, no matter we use it as encryption or decryption.
/// // So, keep don't use functions which start with`key_schedule_decrypt_` and keep the next line commented out.
/// //aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::ofb_enc_dec(&cipher, &mut dec_cipher, &w_keys, &iv);
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i], "ERROR in decrypt {}", i);
/// }
/// ```
///
/// [`key_schedule_decrypt_auto`]: ../aes_core/fn.key_schedule_decrypt_auto.html
/// [`key_schedule_decrypt128`]: ../aes_core/fn.key_schedule_decrypt128.html
/// [`key_schedule_decrypt192`]: ../aes_core/fn.key_schedule_decrypt192.html
/// [`key_schedule_decrypt256`]: ../aes_core/fn.key_schedule_decrypt256.html
pub fn ofb_enc_dec(input: &[u8], output: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut buffer_new = vec![0; BLOCKSIZE_IN_BYTES];
    let mut buffer_last = vec![0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    encryptor(iv, &mut buffer_new, keys);
    let block_number = input.len() >> 4;
    let mut start;
    if input.len() >= BLOCKSIZE_IN_BYTES {
        for j in 0..BLOCKSIZE_IN_BYTES {
            output[j] = buffer_new[j] ^ input[j]
        }
        // The middle blocks
        for i in 1..block_number {
            start = i << 4;
            mem::swap(&mut buffer_new, &mut buffer_last);
            encryptor(&buffer_last, &mut buffer_new, keys);
            for j in 0..BLOCKSIZE_IN_BYTES {
                output[start + j] = buffer_new[j] ^ input[start + j];
            }
        }
    } else {
        buffer_new = Vec::from(iv);
    }
    match input.len() & 0b1111 {
        // The last (tail) block
        r if r != 0 => {
            start = block_number << 4;
            mem::swap(&mut buffer_new, &mut buffer_last);
            encryptor(&buffer_last, &mut buffer_new, keys);
            for j in 0..r {
                output[start + j] = buffer_new[j] ^ input[start + j];
            }
        }
        _ => {}
    }
    buffer_new
}
/// PCBC (Propagating Cipher Block Chaining) Encryption (**Experimental**)
///
/// This function encrypts a long plain from the first parameter and put the long cipher
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the XOR result of the final block of the cipher and the final block of the plain.
/// ![PCBC encryption](https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PCBC_encryption.svg/1280px-PCBC_encryption.svg.png)
/// (This picture comes from the Wikimedia Commons)  
/// **\[Attention!\]** On a message encrypted in PCBC mode, if two adjacent ciphertext blocks
/// are exchanged, this does not affect the decryption of subsequent blocks.
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode, padding_128bit};
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let mut plain: Vec<u8> = vec![0x30, 0xA3, 0xBC, 0xA0, 0xBA, 0x57, 0xFB, 0x27,
///                               0x2F, 0xE2, 0x31, 0xEC, 0xBB, 0x04, 0x5E, 0x93,
///                               0x40, 0xA1, 0x19, 0xB6, 0xE2, 0x60, 0x4F, 0x74,
///                               0x0E, 0xF2, 0xC0, 0x29, 0x1B, 0xF0, 0xF9, 0x9B,
///                               0xFD, 0x90, 0xFD, 0x0D, 0x97, 0xF8, 0x9B, 0x91,
///                               0x78, 0xF4, 0x90, 0x07, 0x66, 0x6C, 0xE8, 0x11,
///                               0x5F, 0xFE, 0x6F, 0xE9, 0x4F, 0x75, 0xB0, 0xCE,
///                               0x53, 0x48, 0x92, 0xC7, 0x96, 0xD2, 0x0B, 0x3E];
/// let mut cipher = vec![0u8; length + 16];
/// let mut dec_cipher = vec![0u8; length + 16];
/// let mut o_key: Vec<u8> = vec![0x0F, 0x57, 0x9F, 0x79, 0x50, 0x99, 0x0A, 0xCE,
///                               0x66, 0x72, 0xA8, 0x17, 0x95, 0x1F, 0xF6, 0x06,
///                               0x24, 0x40, 0xDE, 0xF5, 0x08, 0xF1, 0x64, 0x34,
///                               0xD6, 0xEF, 0xEF, 0xFD, 0x26, 0x23, 0x04, 0x95];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
/// let mut iv: Vec<u8> = vec![0x04, 0x7C, 0xF3, 0xEA, 0xE1, 0x76, 0x45, 0x85,
///                            0x72, 0x52, 0x7B, 0xAA, 0x26, 0x0D, 0x65, 0xBB];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
/// padding_128bit::pa_pkcs7(&mut plain);
/// aes_with_operation_mode::cbc_enc(&plain, &mut cipher, &w_keys, &iv);
///
/// aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::cbc_dec(&cipher, &mut dec_cipher, &w_keys, &iv);
/// padding_128bit::de_ansix923_pkcs7(&mut dec_cipher);
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i]);
/// }
/// ```
pub fn pcbc_enc(plain: &[u8], cipher: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut buffer = vec![0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    for j in 0..BLOCKSIZE_IN_BYTES {
        buffer[j] = iv[j] ^ plain[j];
    }
    encryptor(&buffer, &mut cipher[..BLOCKSIZE_IN_BYTES], keys);
    // The other blocks
    let block_number = plain.len() >> 4;
    let mut start = 0;
    for i in 1..block_number {
        start = i << 4;
        for j in 0..BLOCKSIZE_IN_BYTES {
            buffer[j] = cipher[start + j - BLOCKSIZE_IN_BYTES]
                ^ plain[start + j - BLOCKSIZE_IN_BYTES]
                ^ plain[start + j];
        }
        encryptor(
            &buffer,
            &mut cipher[start..(start + BLOCKSIZE_IN_BYTES)],
            keys,
        );
    }
    for j in 0..BLOCKSIZE_IN_BYTES {
        buffer[j] = cipher[start + j] ^ plain[start + j];
    }
    buffer
}
/// PCBC (Propagating Cipher Block Chaining) Decryption (**Experimental**)
///
/// This function decrypts a long cipher from the first parameter and put the long plain
/// into the second parameter, using the scheduled keys and the initialization vector (IV)
/// in the third and fourth parameters.  
/// Finally, it returns the XOR result of the final block of the cipher and the final block of the plain.
/// ![PCBC decryption](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/PCBC_decryption.svg/1280px-PCBC_decryption.svg.png)
/// (This picture comes from the Wikimedia Commons)  
/// **\[Attention!\]** On a message encrypted in PCBC mode, if two adjacent ciphertext blocks
/// are exchanged, this does not affect the decryption of subsequent blocks.
/// # Examples
/// Please refer to the [`pcbc_enc`] function, codes are included there.
///
/// [`pcbc_enc`]: ../aes_with_operation_mode/fn.pcbc_enc.html
pub fn pcbc_dec(cipher: &[u8], plain: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let decryptor = select_decrypt_function!(keys);
    let mut buffer = vec![0; BLOCKSIZE_IN_BYTES];
    // The 1st (head) block
    decryptor(&cipher[..BLOCKSIZE_IN_BYTES], &mut buffer, keys);
    for j in 0..BLOCKSIZE_IN_BYTES {
        plain[j] = iv[j] ^ buffer[j];
    }
    // The other block
    let block_number = cipher.len() >> 4;
    let mut start = 0;
    for i in 1usize..block_number {
        start = i << 4;
        decryptor(
            &cipher[start..(start + BLOCKSIZE_IN_BYTES)],
            &mut buffer,
            keys,
        );
        for j in 0..BLOCKSIZE_IN_BYTES {
            plain[start + j] = cipher[start + j - BLOCKSIZE_IN_BYTES]
                ^ plain[start + j - BLOCKSIZE_IN_BYTES]
                ^ buffer[j];
        }
    }
    for j in 0..BLOCKSIZE_IN_BYTES {
        buffer[j] = cipher[start + j] ^ plain[start + j];
    }
    buffer
}
/// CFB (Cipher Feedback) Encryption with 8-bit feedback size (**Experimental**)
/// # Examples
/// ```
/// use aes_frast::{aes_core, aes_with_operation_mode};
/// use aes_frast::N_SUBKEYS_256BIT;
/// let length: usize = 64;
/// let plain: Vec<u8> = vec![0x34, 0x63, 0xD0, 0x89, 0x1D, 0x71, 0x4A, 0xB0,
///                           0x08, 0x5D, 0x22, 0xE1, 0x8B, 0xFA, 0x77, 0xF0,
///                           0xEB, 0xE4, 0xB8, 0x9E, 0xF0, 0x05, 0x32, 0x7D,
///                           0x4F, 0xBD, 0x87, 0x69, 0x75, 0x76, 0x78, 0xAA,
///                           0x3D, 0x24, 0x06, 0x0C, 0xA4, 0xA5, 0x8C, 0xA0,
///                           0x21, 0x58, 0xB8, 0xA1, 0x86, 0xAD, 0xBB, 0x6D,
///                           0x9E, 0x09, 0x1C, 0x47, 0x06, 0x25, 0x4B, 0x2E,
///                           0x30, 0x53, 0x3A, 0x5F, 0xE9, 0xDF, 0x3A, 0x90];
/// let mut cipher = vec![0u8; length];
/// let mut dec_cipher = vec![0u8; length];
/// let o_key: Vec<u8> = vec![0x0F, 0x57, 0x9F, 0x79, 0x50, 0x99, 0x0A, 0xCE,
///                           0x66, 0x72, 0xA8, 0x17, 0x95, 0x1F, 0xF6, 0x06,
///                           0x24, 0x40, 0xDE, 0xF5, 0x08, 0xF1, 0x64, 0x34,
///                           0xD6, 0xEF, 0xEF, 0xFD, 0x26, 0x23, 0x04, 0x95];
/// let mut w_keys: Vec<u32> = vec![0u32; N_SUBKEYS_256BIT];
/// let iv: Vec<u8> = vec![0x04, 0x7C, 0xF3, 0xEA, 0xE1, 0x76, 0x45, 0x85,
///                        0x72, 0x52, 0x7B, 0xAA, 0x26, 0x0D, 0x65, 0xBB];
/// let expected_encrypted = vec![0x9D, 0x54, 0x96, 0xA3, 0x89, 0x1E, 0xC0, 0x40,
///                               0xA1, 0x4D, 0x00, 0xC3, 0x4F, 0x1C, 0x15, 0x47,
///                               0xDB, 0x2F, 0xE3, 0xEF, 0x9A, 0x95, 0x03, 0x95,
///                               0x5C, 0x4B, 0x8F, 0x8F, 0xBF, 0xCC, 0xB4, 0x72,
///                               0xF1, 0x90, 0x08, 0xCD, 0xF2, 0xDC, 0x04, 0x51,
///                               0xC0, 0x36, 0x00, 0x72, 0xDE, 0x59, 0x1F, 0x10,
///                               0xE6, 0x8A, 0xE5, 0x32, 0x88, 0x0B, 0x02, 0x95,
///                               0x26, 0x66, 0xD1, 0x48, 0x42, 0x58, 0xED, 0xF7];
///
/// aes_core::key_schedule_encrypt_auto(&o_key, &mut w_keys);
///
/// aes_with_operation_mode::cfb_8_enc(&plain, &mut cipher, &w_keys, &iv);
///
/// for i in 0..length {
///     assert_eq!(expected_encrypted[i], cipher[i], "ERROR in encrypt {}", i);
/// }
///
/// // Notice: CFB only uses block-encryption, no matter we use it as encryption or decryption.
/// // So, keep don't use functions which start with`key_schedule_decrypt_` and keep the next line commented out.
/// //aes_core::key_schedule_decrypt_auto(&o_key, &mut w_keys);
/// aes_with_operation_mode::cfb_8_dec(&cipher, &mut dec_cipher, &w_keys, &iv);
///
/// for i in 0..length {
///     assert_eq!(plain[i], dec_cipher[i], "ERROR in decrypt {}", i);
/// }
/// ```
pub fn cfb_8_enc(plain: &[u8], cipher: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut out_buffer = vec![0; BLOCKSIZE_IN_BYTES];
    let mut in_buffer = iv.to_owned();
    for i in 0..plain.len() {
        encryptor(&in_buffer, &mut out_buffer, keys);
        cipher[i] = out_buffer[0] ^ plain[i];
        in_buffer.rotate_left(1);
        in_buffer[15] = cipher[i];
    }
    out_buffer
}
/// CFB (Cipher Feedback) Decryption with 8-bit feedback size (**Experimental**)
/// # Examples
/// Please refer to the [`cfb_8_enc`] function, codes are included there.
///
/// [`cfb_8_enc`]: ../aes_with_operation_mode/fn.cfb_8_enc.html
pub fn cfb_8_dec(cipher: &[u8], plain: &mut [u8], keys: &[u32], iv: &[u8]) -> Vec<u8> {
    let encryptor = select_encrypt_function!(keys);
    let mut out_buffer = vec![0; BLOCKSIZE_IN_BYTES];
    let mut in_buffer = iv.to_owned();
    for i in 0..cipher.len() {
        encryptor(&in_buffer, &mut out_buffer, keys);
        plain[i] = out_buffer[0] ^ cipher[i];
        in_buffer.rotate_left(1);
        in_buffer[15] = cipher[i];
    }
    out_buffer
}
