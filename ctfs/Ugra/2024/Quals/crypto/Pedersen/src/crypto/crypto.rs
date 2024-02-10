use curve25519_dalek_ng::ristretto::CompressedRistretto;
use curve25519_dalek_ng::scalar::Scalar;
use bulletproofs::PedersenGens;
use rand::thread_rng;

pub fn sign(secret_key: Scalar, value: Scalar) -> (CompressedRistretto, Scalar) {
    let mut rng = thread_rng();
    let pedersen_gen = PedersenGens::default();
    let blinding = Scalar::random(&mut rng);
    (pedersen_gen.commit(value + secret_key, blinding).compress(), blinding)
}

pub fn verify(commitment: CompressedRistretto, secret_key: Scalar, value: Scalar, blinding: Scalar) -> bool {
    let pedersen_gen = PedersenGens::default();
    Some(pedersen_gen.commit(value + secret_key, blinding)) == commitment.decompress()
}