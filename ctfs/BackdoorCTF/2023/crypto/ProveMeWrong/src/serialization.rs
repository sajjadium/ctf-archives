use ark_ec::short_weierstrass::Affine;
use base64::{engine::general_purpose, Engine as _};
use std::{io, str::FromStr};

use ark_bls12_381::{g1::Config, Fr};
use ark_serialize::CanonicalDeserialize;
use ark_std::Zero;

pub fn base64_to_bytes(base64: &str) -> Vec<u8> {
    general_purpose::STANDARD.decode(base64).expect("bad data")
}

pub fn bytes_to_base64(bytes: &[u8]) -> String {
    general_purpose::STANDARD.encode(bytes)
}

pub fn read_fr_element(prompt: &str) -> Fr {
    let mut line = String::new();

    println!("{}", prompt);
    io::stdin().read_line(&mut line).unwrap();

    let line = line.trim();
    let el = Fr::from_str(line).expect("bad data");

    if el.is_zero() {
        panic!("zero is not allowed");
    };

    el
}

pub fn read_affine_point(prompt: &str) -> Affine<Config> {
    let mut line = String::new();
    
    println!("{}", prompt);
    io::stdin().read_line(&mut line).unwrap();

    let line = line.trim();
    let bytes = base64_to_bytes(line);
    Affine::<Config>::deserialize_compressed(&bytes[..]).expect("bad data")
}
