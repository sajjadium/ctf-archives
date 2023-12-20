use ark_bls12_381::{Bls12_381, Fr};
use ark_poly::{univariate::DensePolynomial as DensePoly, DenseUVPolynomial};
use ark_poly_commit::kzg10::{Proof, KZG10};
use ark_serialize::CanonicalSerialize;

use rand::rngs::OsRng;

mod kzg;
mod serialization;
mod trusted_setup;

use serialization::*;

#[allow(non_camel_case_types)]
type KZG10_Bls12_381 = KZG10<Bls12_381, DensePoly<Fr>>;

fn main() {
    let rng = &mut OsRng;

    // x^2 - 177013
    let p =
        DensePoly::from_coefficients_slice(&[Fr::from(-177013i64), Fr::from(0u64), Fr::from(1u64)]);

    // Generate beta using trusted setup
    println!("Starting trusted setup...");
    let beta = trusted_setup::do_trusted_setup();

    // Generate global parameters
    println!("\nGenerating global parameters...");
    let max_deg = 4;
    let pp = kzg::setup_with_beta::<Bls12_381, _>(max_deg, false, beta, rng).unwrap();
    let (ck, vk) = kzg::trim(&pp, max_deg).unwrap();

    let mut ck_bytes = Vec::new();
    ck.serialize_compressed(&mut ck_bytes).unwrap();
    println!("Committing Key:\n{}\n", bytes_to_base64(&ck_bytes));

    // Request the square root of 177013
    let x = read_fr_element(
        "What do you claim the square root of 177013 in the scalar field of BLS12-381 to be?",
    );

    // Request the proof of the square root
    let proof_point = read_affine_point("Give me the proof for your claim:");
    proof_point.to_string();

    // Verify the proof
    let (comm, _) = KZG10_Bls12_381::commit(&ck, &p, None, None).unwrap();

    let point = x;
    let value = Fr::from(0u64);

    let proof: Proof<Bls12_381> = Proof {
        w: proof_point,
        random_v: None,
    };

    let valid = KZG10_Bls12_381::check(&vk, &comm, point, value, &proof).unwrap();
    if valid {
        println!("flag{{REDACTED}}");
    } else {
        println!("Nope!");
    }
}
