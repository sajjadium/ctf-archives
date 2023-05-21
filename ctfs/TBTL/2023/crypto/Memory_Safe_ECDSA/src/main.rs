use ecdsa::{
    elliptic_curve::{
        generic_array::{
            typenum::Unsigned,
            GenericArray,
        },
        Curve,
        PublicKey,
        Scalar,
    },
    hazmat::{
        SignPrimitive,
        VerifyPrimitive,
    },
    Signature,
};
use p224::{
    AffinePoint,
    NistP224,
    NonZeroScalar,
};
use rdrand::RdRand;
use std::{
    io::{
        stdin,
        stdout,
        Write,
    },
};

const BANNER: &str = "
              /\\                   /\\
             ( /   @ @    ()      ( /   @ @    ()
              \\  __| |__  /        \\  __| |__  /
               -/   \"   \\-          -/   \"   \\-
              /-|       |-\\        /-|       |-\\
             / /-\\     /-\\ \\      / /-\\     /-\\ \\
              / /-`---'-\\ \\        / /-`---'-\\ \\
               /         \\          /         \\

    /\\                   /\\                    /\\
   ( /   @ @    ()      ( /   @ @    ()       ( /   @ @    ()
    \\  __| |__  /        \\  __| |__  /         \\  __| |__  /
     -/   \"   \\-          -/   \"   \\-           -/   \"   \\-
    /-|       |-\\        /-|       |-\\         /-|       |-\\
   / /-\\     /-\\ \\      / /-\\     /-\\ \\       / /-\\     /-\\ \\
    / /-`---'-\\ \\        / /-`---'-\\ \\         / /-`---'-\\ \\
     /         \\          /         \\           /         \\


                /\\                      /\\
               ( /   @ @    ()         ( /   @ @    ()
                \\  __| |__  /           \\  __| |__  /
                 -/   \"   \\-             -/   \"   \\-
                /-|       |-\\           /-|       |-\\
               / /-\\     /-\\ \\         / /-\\     /-\\ \\
                / /-`---'-\\ \\           / /-`---'-\\ \\
                 /         \\             /         \\

";

const BASE_POINT_ORDER_BYTE_SIZE: usize = <NistP224 as Curve>::FieldBytesSize::USIZE;
const MAX_QUERIES: usize = 10usize;

#[derive(Default)]
struct Scanner {
    buffer: Vec<String>,
}

impl Scanner {
    fn next<T: std::str::FromStr>(&mut self) -> T {
        loop {
            if let Some(token) = self.buffer.pop() {
                return token.parse().ok().expect("Failed parse");
            }
            let mut input = String::new();
            stdin().read_line(&mut input).expect("Failed read");
            self.buffer = input.split_whitespace().rev().map(String::from).collect();
        }
    }
}

fn output(out: &str) {
    print!("{}", out);
    stdout().flush().expect("Error");
}

fn done() {
    output("\n");
    output("🦀: Ok, bye!\n");
    std::process::exit(0x0)
}

fn bytes_into_scalar(bytes: &[u8]) -> Scalar<NistP224> {
    Scalar::<NistP224>::from_bytes(bytes.into()).unwrap()
}

fn random_byte_array<const SIZE: usize>() -> [u8; SIZE] {
    let mut rng = RdRand::new().expect("Error");
    let mut ret = [0u8; SIZE];
    rng.try_fill_bytes(&mut ret).expect("Error");
    ret
}

fn sign(private_key: &[u8], m_bytes: &[u8]) -> (Vec<u8>, Vec<u8>) {
    let d = bytes_into_scalar(private_key);

    let k_bytes = random_byte_array::<BASE_POINT_ORDER_BYTE_SIZE>();
    let k = bytes_into_scalar(&k_bytes);

    let e = hex::decode(sha256::digest(m_bytes)).expect("Error");
    let z = GenericArray::clone_from_slice(&e[..BASE_POINT_ORDER_BYTE_SIZE]);

    let sig = d.try_sign_prehashed(k, &z).expect("Error");
    (sig.0.r().to_bytes().to_vec(), sig.0.s().to_bytes().to_vec())
}

fn verify(q: &AffinePoint, m_bytes: &[u8], sig: (&[u8], &[u8])) -> bool {
    let e = hex::decode(sha256::digest(m_bytes)).expect("Error");
    let z = GenericArray::clone_from_slice(&e[..BASE_POINT_ORDER_BYTE_SIZE]);

    let sig = Signature::from_scalars(
        GenericArray::clone_from_slice(sig.0),
        GenericArray::clone_from_slice(sig.1),
    )
    .expect("Error");

    q.verify_prehashed(&z, &sig).is_ok()
}

fn main() {
    output(BANNER);

    output("The 🚩 is guarded by a group of crustaceans and an ECDSA implementation\n");
    output("in the safest programming language. Hacking is futile...\n");

    let flag = std::fs::read_to_string("resources/flag.txt").expect("Error");

    output("\n");
    output("OPTIONS: \n");
    output("  1) Sign something\n");
    output("  2) Give us a signed flag\n");
    output("\n");

    output(format!("🦀: sha256(🚩) = {}\n", sha256::digest(&*flag)).as_str());
    output("\n");

    let private_key = random_byte_array::<BASE_POINT_ORDER_BYTE_SIZE>();
    let d = NonZeroScalar::new(bytes_into_scalar(&private_key)).unwrap();
    let public_key = PublicKey::<NistP224>::from_secret_scalar(&d);
    let q = public_key.as_affine();

    let mut scanner = Scanner::default();

    for _ in 0..MAX_QUERIES {
        output("\n");
        output("🤡: ");

        let option = scanner.next::<usize>();

        match option {
            1 => {
                output("\n");
                output("🦀: What do you want to sign?\n");
                output("\n");
                output("🤡: ");

                let message = scanner.next::<String>();
                let (r, s) = sign(&private_key, message.as_bytes());

                output("\n");
                output(format!("🦀: signature = {} {}\n", hex::encode(r), hex::encode(s)).as_str());
            }
            2 => {
                output("\n");
                output("🦀: So... you have a signed flag?\n");
                output("\n");
                output("🤡: ");

                let r = scanner.next::<String>();
                let s = scanner.next::<String>();

                let r_bytes = hex::decode(r).expect("Error");
                let s_bytes = hex::decode(s).expect("Error");

                match verify(q, flag.as_bytes(), (&r_bytes, &s_bytes)) {
                    false => {
                        output("\n");
                        output("🦀: hahaha... you clown... your efforts are futile!!\n");
                        std::process::exit(0x0);
                    }
                    true => {
                        output("\n");
                        output("🦀: Wow... looks like you're not a clown after all!\n");
                        output("\n");
                        output(format!("🦀: 🚩 = {}\n", flag).as_str());
                        std::process::exit(0x0);
                    }
                };
            }
            _ => done(),
        }
    }

    done();
}
