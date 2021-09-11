use std::io::BufRead;
use getrandom::getrandom;
use rug::{
    rand::{RandGen,RandState},
    Integer
};
use sha2::{Sha256,Digest};
use aes::{Aes256,Aes256Ctr,NewBlockCipher,cipher::{FromBlockCipher,StreamCipher}};
use generic_array::GenericArray;

// Secret sauce
// N = p*q; p ≡ q ≡ 3 (mod 4); p, q prime
use hardcore::{dlog, N, G, ORDER, FLAG};

struct SystemRandom;
impl RandGen for SystemRandom {
    fn gen(&mut self) -> u32 {
        let mut buf: [u8; 4] = [0; 4];
        let _ = getrandom(&mut buf).unwrap();
        ((buf[0] as u32) << 24) | ((buf[1] as u32) << 16) | ((buf[2] as u32) << 8) | (buf[3] as u32)
    }
}

fn encrypt_flag(shared: Integer) {
    let mut hasher = Sha256::new();
    hasher.update(shared.to_string());
    let key = hasher.finalize();
    let mut cipher = Aes256Ctr::from_block_cipher(
        Aes256::new_from_slice(&key.as_slice()).unwrap(),
        &GenericArray::clone_from_slice(&[0; 16])
        );
    let mut flag = FLAG.clone();
    cipher.apply_keystream(&mut flag);
    println!("FLAG = {}", flag.iter().map(|c| format!("{:02x}", c)).collect::<String>());
}

fn main() {
    println!("+++++++++++++++++++++++++++++++++++++++++++++++\n\
              + I hear there's a mythical oracle at Delphi. +\n\
              +++++++++++++++++++++++++++++++++++++++++++++++\n");
    let mut sysrng = SystemRandom;
    let mut rnd = RandState::new_custom(&mut sysrng);
    let d = Integer::from(&*ORDER).random_below(&mut rnd);
    let publ = Integer::from(&*G).pow_mod(&d, &*N).unwrap();
    let nbits = ORDER.significant_bits();
    let alice = Integer::from(&*G).pow_mod(&Integer::from(&*ORDER).random_below(&mut rnd), &*N).unwrap();
    println!("N = {}\nG = {}\npubl = {}\nalice = {}\nnbits = {}",
        *N,
        *G,
        publ,
        alice,
        nbits);
    encrypt_flag(alice.pow_mod(&d, &N).unwrap());
    for line in std::io::stdin().lock().lines() {
        let input = line.unwrap().parse::<Integer>().unwrap();
        match dlog(input.clone()) {
            None => println!("-1"),
            Some(x) => {
                assert!(G.clone().pow_mod(&x, &*N).unwrap() == input % &*N);
                assert!(x < *ORDER);
                assert!(x >= 0);
                println!("{}", x.get_bit(nbits - 123) as i32)
            }
        }
    }
}
