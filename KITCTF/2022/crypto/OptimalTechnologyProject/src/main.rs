use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::time::SystemTime;

mod secret;
use crate::secret::{MSG};

fn main() {
    const MSG_LEN: usize = MSG.len();

    let t = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .expect("Duration since UNIX_EPOCH failed");
    let mut rng = StdRng::seed_from_u64(t.as_micros() as u64);
    let mut random_bytes = [0u8; MSG_LEN];
    for x in &mut random_bytes {
        *x = rng.gen::<u8>();
    }
    let flag_bytes  = MSG.as_bytes();

    let enc: Vec<_> = random_bytes.iter().zip(flag_bytes).map(|(x, y)| x ^ y).collect();

    let enc_b64 = base64::encode(enc);
    println!("Here is your message: {}", enc_b64);
}