use rand::rngs::OsRng;
use rand::RngCore;

use crate::aes_util::*;

const NUMROUNDS: usize = 10;
const NUMKEYS: usize = 2 * NUMROUNDS + 1;

pub trait BlockCipher {
    fn encrypt(&self, pt: [u8; 16]) -> [u8; 16];
    fn decrypt(&self, ct: [u8; 16]) -> [u8; 16];
}

pub struct ShuffledAes {
    round_keys: [[u8; 16]; NUMKEYS],
}

impl ShuffledAes {
    pub fn new() -> ShuffledAes {
        let mut round_keys = [[0u8; 16]; NUMKEYS];
        for i in 0..NUMKEYS {
            OsRng.fill_bytes(&mut round_keys[i]);
        }
        let result = ShuffledAes { round_keys };
        return result;
    }
}

impl BlockCipher for ShuffledAes {
    fn encrypt(&self, pt: [u8; 16]) -> [u8; 16] {
        let mut state = pt;

        xor(&mut state, &self.round_keys[0]);

        // sub bytes
        for key_idx in 1..NUMROUNDS + 1 {
            sub_bytes(&mut state);
            xor(&mut state, &self.round_keys[key_idx]);
        }

        // shift rows mix columns
        for key_idx in NUMROUNDS + 1..2 * NUMROUNDS + 1 {
            shift_rows(&mut state);
            mix_columns(&mut state);
            xor(&mut state, &self.round_keys[key_idx]);
        }

        return state;
    }

    fn decrypt(&self, ct: [u8; 16]) -> [u8; 16] {
        let mut state = ct;

        // shift rows mix columns
        for key_idx in (NUMROUNDS + 1..2 * NUMROUNDS + 1).rev() {
            xor(&mut state, &self.round_keys[key_idx]);
            inv_mix_columns(&mut state);
            inv_shift_rows(&mut state);
        }

        // sub bytes
        for key_idx in (1..NUMROUNDS + 1).rev() {
            xor(&mut state, &self.round_keys[key_idx]);
            inv_sub_bytes(&mut state);
        }

        xor(&mut state, &self.round_keys[0]);

        return state;
    }
}
