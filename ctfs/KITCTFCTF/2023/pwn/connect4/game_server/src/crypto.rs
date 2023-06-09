use std::{
    net::TcpStream,
    io::{prelude::*, BufReader, Error, ErrorKind}
};


use aes::{Aes128, Block};
use aes::cipher::{
    BlockEncrypt, BlockDecrypt, KeyInit,
    generic_array::GenericArray
};


pub fn mod_exp(base: u32, exponent: u32, modulus: u32) -> u32 {
    let mut base: u64 = (base % modulus) as u64;
    let mut exponent = exponent;
    let mut c: u64 = 1;

    loop {
        if exponent == 0 {
            break;
        }

        if exponent % 2 == 1 {
            c = (c * base) % (modulus as u64);
        }

        exponent = exponent >> 1;
        base = (base * base) % (modulus as u64);
    }

    c as u32
}


pub struct XSRng {
    state: u32
}

impl XSRng {
    pub fn from_seed(seed: u32) -> XSRng {
        XSRng { state: seed }
    }

    pub fn next(&mut self) -> u32 {
        let mut x: u32 = self.state;
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        self.state = x;
        x
    }
}


pub struct EncHandler {
    aes_instance: Aes128
}


impl EncHandler {
    pub fn new(key: u128) -> EncHandler {
        let key = GenericArray::from(key.to_le_bytes());
        EncHandler { aes_instance: Aes128::new(&key) }
    }

    pub fn encrypt(&self, data: Vec<u8>) -> Result<Vec<u8>, Error> {
        if data.len() != 0 {
            let mut encrypted_data: Vec<u8> = Vec::new(); 

            let full_blocks = data.len() >> 4;
            
            for i in 0..full_blocks {
                let block_arr: [u8; 16] = data[i*16..(i+1)*16].try_into().unwrap();
                let mut block = Block::from(block_arr);
                self.aes_instance.encrypt_block(&mut block);
                encrypted_data.append(&mut block.to_vec());
            }

            let mut last_block = self.pad(data[full_blocks*16..].to_vec());
            self.aes_instance.encrypt_block(&mut last_block);
            encrypted_data.append(&mut last_block.to_vec());
            
            Ok(encrypted_data)
        } else {
            Err(Error::new(ErrorKind::Other, "Data has invalid length"))
        }
    }

    pub fn decrypt(&self, data: Vec<u8>) -> Result<Vec<u8>, Error> {
        if data.len() % 16 == 0 && data.len() != 0 {
            let mut decrypted_data: Vec<u8> = Vec::new();
            let blocks = data.len() >> 4;

            for i in 0..blocks-1 {
                let block_arr: [u8; 16] = data[i*16..(i+1)*16].try_into().unwrap();
                let mut block = Block::from(block_arr);
                self.aes_instance.decrypt_block(&mut block);
                decrypted_data.append(&mut block.to_vec());
            }

            let last_block_arr: [u8; 16] = data[(blocks-1)*16..].try_into().unwrap();
            let mut last_block = Block::from(last_block_arr);
                
            self.aes_instance.decrypt_block(&mut last_block);
            decrypted_data.append(&mut self.unpad(last_block.to_vec()));

            Ok(decrypted_data)
        } else {
            Err(Error::new(ErrorKind::Other, "Data has invalid length"))
        }
    }

    fn pad(&self, mut data: Vec<u8>) -> Block {
        assert!(data.len() <= 16);
        let padlen = (16 - data.len()) as u8;
        for _ in 0..padlen {
            data.push(padlen);
        }
        assert!(data.len() == 16);
        let block: [u8; 16] = data.try_into().unwrap();
        Block::from(block)
    }

    fn unpad(&self, mut data: Vec<u8>) -> Vec<u8> {
        assert!(data.len() <= 16);
        let padlen = data[data.len() - 1];
        for _ in 0..padlen {
            data.pop();
        }
        data
    }
}


pub struct EncStreamClient {
    enc_handler: EncHandler,
    writer: TcpStream,
    reader: BufReader<TcpStream>,
}


impl EncStreamClient {
    pub fn new(key: u128, stream: TcpStream) -> EncStreamClient {
        let enc_handler = EncHandler::new(key);
        let buf_reader = BufReader::new(stream.try_clone().unwrap());
        EncStreamClient { enc_handler: enc_handler, writer: stream.try_clone().unwrap(), reader: buf_reader }
    }

    pub fn read_line(&mut self, buf: &mut String) -> Result<usize, Error> {
        let mut tmp_buf = String::new();
        self.reader.read_line(&mut tmp_buf)?;
        
        // strip newline
        tmp_buf.pop();

        // println!("Received hex: {:?}", tmp_buf);
        // hex decode
        let decoded_string = hex::decode(tmp_buf).map_err(|_| Error::new(ErrorKind::Other, "Invalid hex string"))?;
        let decrypted_vec = self.enc_handler.decrypt(decoded_string)?;
        let decrypted_string = String::from_utf8(decrypted_vec).map_err(|_| Error::new(ErrorKind::Other, "Invalid data found after decryption"))?;

        buf.push_str(&decrypted_string);

        // println!("Decrypted: {:?}", decrypted_string);

        Ok(buf.len())
    }

    pub fn write_all(&mut self, buf: &[u8]) -> Result<(), Error> {
        let encrypted_data = self.enc_handler.encrypt(buf.to_vec())?;
        let encoded_string = hex::encode(encrypted_data);

        // println!("Sending: {:?} -> {}", buf.to_vec(), encoded_string);
        self.writer.write_all(format!("{}\n", encoded_string).as_bytes())?;

        Ok(())
    }
}