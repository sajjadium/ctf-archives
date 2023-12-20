use rand::{rngs::OsRng, RngCore};
use std::str::FromStr;

use ark_bls12_381::Fr;
use ark_ff::{BigInt, BigInteger, PrimeField};

use crate::serialization::*;

mod mimc;
use mimc::mimc;

pub(crate) type FrBigInt = BigInt<4>;

pub fn do_trusted_setup() -> Fr {
    // I take some randomness from you
    let r_bits = read_fr_element("Give me your randomness:")
        .into_bigint()
        .to_bits_be();

    // I insert some randomness of my own
    let mut rng = OsRng;
    let k = rng.next_u64();

    println!("\nFinalizing setup...");
    let fr_big_int = FrBigInt::from_bits_be(&mimc(&r_bits[4..], k));
    Fr::from_str(&fr_big_int.to_string()).expect("internal error")
}
