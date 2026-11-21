use stream_cipher::StreamCipher;
use hex;
use std::{fs, io};
use std::io::{BufRead, Write};

use crate::stream_cipher::CounterMode;
use crate::block_cipher::ShuffledAes;

mod aes_util;
mod block_cipher;
mod stream_cipher;

fn main() {
    let flag = fs::read_to_string("flag.txt").expect("cannot read flag.txt");
    let cipher = CounterMode::new(Box::new(ShuffledAes::new()));

    let (flag_nonce, enc_flag) = cipher.encrypt(flag.as_bytes());

    println!("Here's your flag: {} {}", hex::encode(flag_nonce), hex::encode(enc_flag));

    loop {
        print!("pt> ");
        let _ = io::stdout().lock().flush();

        let mut line = String::new();
        match std::io::stdin().lock().read_line(&mut line) {
            Ok(_) => (),
            Err(_) => return,
        }
        let line = line.trim();

        if line.is_empty() {
            return;
        }

        let (nonce, encrypted) = cipher.encrypt(line.as_bytes());

        println!("ct: {} {}", hex::encode(nonce), hex::encode(encrypted));
    }
}