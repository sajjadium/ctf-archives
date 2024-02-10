use std::fs::File;
use std::io::Read;
use std::path::Path;
use curve25519_dalek_ng::scalar::Scalar;

pub fn read_flag(path: &Path) -> String {
    let mut file_reader = File::open(path).expect("Can't open flag file");
    let mut flag = String::new();
    file_reader.read_to_string(&mut flag).expect("Can't read flag");
    flag
}

pub fn read_key(path: &Path) -> Scalar {
    let mut file_reader = File::open(path).expect("Can't open key file");
    let mut bytes: [u8; 32] = [0; 32];
    file_reader.read_exact(&mut bytes).expect("Can't read key file");
    Scalar::from_bytes_mod_order(bytes)
}
