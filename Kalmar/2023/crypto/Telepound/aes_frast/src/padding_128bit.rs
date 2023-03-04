//! # padding_128bit
//! `padding_128bit` is a padding mod for block cipher which use 128 bits blocks, especially the
//! `aes_core` module.

use super::aes_core::BLOCKSIZE_IN_BYTES;

/// Add PKCS #7 padding
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the added bytes' length.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::pa_pkcs7;
///
/// let mut origin = vec![0xFFu8; 7];
///
/// let padding_length = pa_pkcs7(&mut origin);
///
/// assert_eq!(padding_length, 9);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x09u8,
///                         0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8]);
/// ```
pub fn pa_pkcs7(input_vec: &mut Vec<u8>) -> usize {
    let r = BLOCKSIZE_IN_BYTES - (input_vec.len() & 0b1111);
    input_vec.append(&mut vec![r as u8; r]);
    r
}

/// Add ANSIX923 padding
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the added bytes' length.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::pa_ansix923;
///
/// let mut origin = vec![0xFFu8; 7];
///
/// let padding_length = pa_ansix923(&mut origin);
///
/// assert_eq!(padding_length, 9);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x00u8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x09u8]);
/// ```
pub fn pa_ansix923(input_vec: &mut Vec<u8>) -> usize {
    let r = BLOCKSIZE_IN_BYTES - (input_vec.len() & 0b1111);
    let mut tail = vec![0u8; r];
    *tail.last_mut().unwrap() = r as u8;
    input_vec.append(&mut tail);
    r
}

/// Remove ANSIX923 or PKCS #7 padding
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the removed bytes' length.
///
/// **Attention!** Please be sure the parameter ends with exactly the ANSIX923 or PKCS #7 padding
/// string. This function does NOT perform checks.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::de_ansix923_pkcs7;
///
/// let mut ansix923 = vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x00u8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x09u8];
///
/// let padding_ansix923_length = de_ansix923_pkcs7(&mut ansix923);
///
/// let mut pkcs7 = vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x09u8,
///                      0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8, 0x09u8];
///
/// let padding_pkcs7_length = de_ansix923_pkcs7(&mut pkcs7);
///
/// let expected = vec![0xFFu8; 7];
/// assert_eq!(padding_ansix923_length, 9);
/// assert_eq!(padding_pkcs7_length, 9);
/// assert_eq!(ansix923, expected);
/// assert_eq!(pkcs7, expected);
/// ```
pub fn de_ansix923_pkcs7(input_vec: &mut Vec<u8>) -> usize {
    let r = input_vec.pop().unwrap() as usize;
    input_vec.truncate(input_vec.len() + 1 - r);
    r
}

/// Add Zeros padding
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the added bytes' length.
///
/// This padding has never been standardized in cryptography specifications. So, **NOT**
/// recommended. This padding here maybe differ from it in other implements, because this function
/// still adds a complete block after the complete end-block, while maybe some other implements
/// don't and only add to the incomplete end-block. If you are looking for function like that, see
/// [`pa_zeros_ifnotcomplete`].
///
/// **Attention!** If the origin data ends with zero(s) (one or more 0xFF), depadding will remove
/// all these zeros.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::pa_zeros;
///
/// let mut origin = vec![0xFFu8; 7];
/// let padding_length = pa_zeros(&mut origin);
///
/// assert_eq!(padding_length, 9);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x00u8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8]);
///
/// origin = vec![0xFFu8; 16];
/// let padding_length = pa_zeros(&mut origin);
///
/// assert_eq!(padding_length, 16);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8,
///                         0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8]);
/// ```
///
/// [`pa_zeros_ifnotcomplete`]: ../padding_128bit/fn.pa_zeros_ifnotcomplete.html
pub fn pa_zeros(input_vec: &mut Vec<u8>) -> usize {
    let r = BLOCKSIZE_IN_BYTES - (input_vec.len() & 0b1111);
    input_vec.append(&mut vec![0u8; r]);
    r
}

/// Add Zeros padding only if the last block is not a complete block
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the added bytes' length.
///
/// This padding has never been standardized in cryptography specifications. So, **NOT**
/// recommended.
///
/// Different from the [`pa_zeros`] function, this function only adds zeros to the incomplete
/// end-block. When the end-block is complete, it keeps it unchanged.
///
/// **Attention!** If the origin data ends with zero(s) (one or more 0xFF), depadding will remove
/// all these zeros.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::pa_zeros_ifnotcomplete;
///
/// let mut origin = vec![0xFFu8; 7];
/// let padding_length = pa_zeros_ifnotcomplete(&mut origin);
///
/// assert_eq!(padding_length, 9);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x00u8,
///                         0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8]);
///
/// origin = vec![0xFFu8; 16];
/// let padding_length = pa_zeros_ifnotcomplete(&mut origin);
///
/// assert_eq!(padding_length, 0);
/// assert_eq!(origin, vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8,
///                         0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8]);
/// ```
///
/// [`pa_zeros`]: ../padding_128bit/fn.pa_zeros.html
pub fn pa_zeros_ifnotcomplete(input_vec: &mut Vec<u8>) -> usize {
    let r = BLOCKSIZE_IN_BYTES - (input_vec.len() & 0b1111);
    if r < BLOCKSIZE_IN_BYTES {
        input_vec.append(&mut vec![0u8; r]);
        r
    } else {
        0
    }
}

/// Remove Zeros padding
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the removed bytes' length.
///
/// **Attention!** If the origin data ends with zero(s) (one or more 0xFF), depadding will remove
/// all these zeros.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::de_zeros;
///
/// let mut zeros = vec![0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0xFFu8, 0x00u8,
///                      0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8, 0x00u8];
///
/// let padding_length = de_zeros(&mut zeros);
///
/// assert_eq!(padding_length, 9);
/// assert_eq!(zeros, vec![0xFFu8; 7]);
/// ```
pub fn de_zeros(input_vec: &mut Vec<u8>) -> usize {
    let mut tmp: u8;
    let mut count = 0;
    loop {
        tmp = input_vec.pop().unwrap();
        if tmp != 0 {
            input_vec.push(tmp);
            break count;
        }
        count += 1;
    }
}

/// Drop the last incomplete or complete block.
///
/// * *parameter* `input_vec`: the vec that contains original data.
/// * *return* : the removed bytes' length.
/// # Examples
/// ```
/// use aes_frast::padding_128bit::drop_last_block;
///
/// // Drop the last incomplete block.
/// let mut origin = vec![0xFFu8; 21];
/// let dropped_length = drop_last_block(&mut origin);
///
/// assert_eq!(dropped_length, 5);
/// assert_eq!(origin, vec![0xFFu8; 16]);
///
/// // Drop the last incomplete block.
/// origin = vec![0xFFu8; 32];
/// let dropped_length = drop_last_block(&mut origin);
///
/// assert_eq!(dropped_length, 16);
/// assert_eq!(origin, vec![0xFFu8; 16]);
/// ```
pub fn drop_last_block(input_vec: &mut Vec<u8>) -> usize {
    let r = match input_vec.len() & 0b1111 {
        0 => BLOCKSIZE_IN_BYTES,
        r => r,
    };
    input_vec.truncate(input_vec.len() - r);
    r
}
