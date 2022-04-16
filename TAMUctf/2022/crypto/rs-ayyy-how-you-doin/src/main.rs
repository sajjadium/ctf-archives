use rand::distributions::Alphanumeric;
use rand::Rng;
use rand_chacha::rand_core::SeedableRng;
use rand_chacha::ChaCha20Rng;
use rngcache::RngCache;
use rsa::pkcs8::ToPublicKey;
use rsa::{PaddingScheme, PublicKey, RsaPrivateKey, RsaPublicKey};
use std::io::{stdin, BufRead};

fn main() -> anyhow::Result<()> {
    let rng = ChaCha20Rng::from_entropy();
    let mut rng = RngCache::new(rng);
    let privkey = RsaPrivateKey::new(&mut rng, 4096)?;
    let pubkey = RsaPublicKey::from(&privkey);
    let encoded = pubkey.to_public_key_pem()?;

    println!("{}", encoded);

    let message = std::iter::repeat_with(|| rng.sample(&Alphanumeric))
        .take(1 << 6)
        .collect::<Vec<_>>();

    println!("Please decrypt the following message: ");
    let cipher = pubkey.encrypt(&mut rng, PaddingScheme::PKCS1v15Encrypt, &message)?;
    println!("{}", hex::encode(cipher));

    let mut attempt = String::new();
    stdin().lock().read_line(&mut attempt)?;
    if attempt.trim().as_bytes() == message {
        println!("{}", include_str!("../flag.txt"));
    } else {
        println!("That was not the correct string. Sorry!");
    }

    Ok(())
}
