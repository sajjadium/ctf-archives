use rug::integer::Order;
use rug::rand::RandGen;
use rug::{rand::RandState, Complete, Integer};
use scanf::scanf;
use sha2::{Digest, Sha512};
use static_init::dynamic;
use std::fs::File;
use std::io::Read;
use std::str::FromStr;

#[dynamic]
static P192: Curve = Curve {
    p: Integer::from_str_radix("fffffffffffffffffffffffffffffffeffffffffffffffff", 16).unwrap(),
    a: Integer::from_str_radix("fffffffffffffffffffffffffffffffefffffffffffffffc", 16).unwrap(),
    b: Integer::from_str_radix("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16).unwrap(),
    G: Point {
        x: Integer::from_str_radix("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16).unwrap(),
        y: Integer::from_str_radix("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16).unwrap(),
    },
    n: Integer::from_str_radix("ffffffffffffffffffffffff99def836146bc9b1b4d22831", 16).unwrap(),
};

#[derive(PartialEq, Eq, Clone)]
pub struct Curve {
    pub p: Integer,
    pub a: Integer,
    pub b: Integer,
    pub n: Integer,
    pub G: Point,
}

#[derive(PartialEq, Eq, Clone)]
pub struct Point {
    pub x: Integer,
    pub y: Integer,
}

impl Point {
    pub fn new(x: &Integer, y: &Integer) -> Point {
        Point {
            x: x.clone(),
            y: y.clone(),
        }
    }

    pub fn add(&self, other: &Point) -> Point {
        if self.is_inf() {
            return other.clone();
        }
        if other.is_inf() {
            return self.clone();
        }
        if self == other {
            return self.double();
        }
        let dx = (&other.x - &self.x).complete();
        let dy = (&other.y - &self.y).complete();
        let s = (dy * dx.invert(&P192.p).unwrap()).modulo(&P192.p);
        let x = ((&s * &s).complete() - &self.x - &other.x).modulo(&P192.p);
        let y = (s * (&self.x - &x).complete() - &self.y).modulo(&P192.p);
        Point { x: x, y: y }
    }

    pub fn double(&self) -> Point {
        if self.is_inf() {
            return self.clone();
        }
        let s = (((&self.x * &self.x).complete() * Integer::from(3) + &P192.a)
            * (&self.y * Integer::from(2)).invert(&P192.p).unwrap())
        .modulo(&P192.p);
        let x = ((&s * &s).complete() - &self.x - &self.x).modulo(&P192.p);
        let y = (s * (&self.x - &x).complete() - &self.y).modulo(&P192.p);
        Point { x: x, y: y }
    }

    pub fn negate(&self) -> Point {
        Point {
            x: self.x.clone(),
            y: -self.y.clone(),
        }
    }

    pub fn mul(&self, n: &Integer) -> Point {
        let mut r = Point::new(&Integer::from(0), &Integer::from(0));
        let mut m = self.clone();
        let mut n = n.clone();
        while n > 0 {
            if n.is_odd() {
                r = r.add(&m);
            }
            m = m.double();
            n >>= 1;
        }
        r
    }

    pub fn is_inf(&self) -> bool {
        self.x == 0 && self.y == 0
    }
}

struct FileRandom {
    file: File,
}

impl FileRandom {
    fn new() -> FileRandom {
        FileRandom {
            file: File::open("/dev/urandom").unwrap(),
        }
    }
}

impl RandGen for FileRandom {
    fn gen(&mut self) -> u32 {
        let mut buf = [0u8; 4];
        self.file.read_exact(&mut buf).unwrap();
        as_u32_le(&buf)
    }
}

fn as_u32_le(array: &[u8; 4]) -> u32 {
    ((array[0] as u32) << 0)
        + ((array[1] as u32) << 8)
        + ((array[2] as u32) << 16)
        + ((array[3] as u32) << 24)
}

fn hash(data: &[u8]) -> [u8; 64] {
    let mut hasher = Sha512::new();
    hasher.update(data);
    hasher.finalize().into()
}

fn encrypt(data: &[u8], key: &[u8]) -> Vec<u8> {
    let mut result = Vec::new();
    for (i, b) in data.iter().enumerate() {
        result.push(b ^ key[i % key.len()]);
    }
    result
}

fn bytes_to_hex(bytes: &[u8]) -> String {
    let mut result = String::new();
    for b in bytes {
        result.push_str(&format!("{:02x}", b));
    }
    result
}

fn int_to_bytes(i: &Integer) -> [u8; 24] {
    let mut buf = [0u8; 24];
    i.write_digits(&mut buf, Order::Lsf);
    buf
}

fn main() {
    let flag = std::env::var("FLAG")
        .unwrap_or("potluck{fake_FLAG}".into())
        .into_bytes();
    let message = "Hello, Bob. What are you bringing to the potluck???".as_bytes();

    let mut urandom = FileRandom::new();
    let mut rng = RandState::new_custom(&mut urandom);

    let d_a: Integer = P192.n.clone().random_below(&mut rng);
    let Q_a = P192.G.mul(&d_a);
    println!("Alice public key: {}, {}", Q_a.x, Q_a.y);

    print!("Input Bob public key: ");
    let mut x = String::new();
    let mut y = String::new();
    if scanf!("{}, {}", x, y).is_err() || x.len().max(y.len()) > 77 {
        println!("Invalid input");
        return;
    }
    let Q_b = Point::new(
        &Integer::from_str(&x).unwrap().modulo(&P192.p),
        &Integer::from_str(&y).unwrap().modulo(&P192.p),
    );
    let Q_ab = Q_b.mul(&d_a);
    let key_ab = int_to_bytes(&Q_ab.x);
    println!("Alice to Bob: {}", bytes_to_hex(&encrypt(message, &key_ab)));

    let d_c = P192.n.clone().random_below(&mut rng);
    let Q_c = P192.G.mul(&d_c);
    println!("Charlie public key: {}, {}", Q_c.x, Q_c.y);

    let Q_ac = Q_c.mul(&d_a);
    let key_ac = hash(&int_to_bytes(&Q_ac.x));
    println!(
        "Alice to Charlie: {}",
        bytes_to_hex(&encrypt(&flag, &key_ac))
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_point() {
        let g = P192.G.clone();
        let d = Integer::from_str("187243752983459899230757820204359986210").unwrap();
        let x = Integer::from_str("2734289461486060021208464358266994623373410779064022859147")
            .unwrap();
        let y =
            Integer::from_str("771004581668539298815067901581675228092397393541746889966").unwrap();
        let p = g.mul(&d);
        assert_eq!(p.x, x);
        assert_eq!(p.y, y);
    }
}
