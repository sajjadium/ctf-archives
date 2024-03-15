use std::{fs, io::BufRead};

use bulletproofs::{
    r1cs::{self, *},
    BulletproofGens, PedersenGens,
};

use curve25519_dalek::{ristretto::CompressedRistretto, scalar::Scalar};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Proof {
    c: [Scalar; 2],
    x: CompressedRistretto,
    pf: bulletproofs::r1cs::R1CSProof,
}

impl Proof {
    fn verify(&self) -> bool {
        let mut ts = merlin::Transcript::new(b"kalmar-ctf");
        let mut cs = r1cs::Verifier::new(&mut ts);

        let x = cs.commit(self.x);
        let y = cs.allocate(None).unwrap();
        let z = cs.allocate(None).unwrap();

        impossible_relation(&mut cs, x, y, z, &self.c);

        let bp = BulletproofGens::new(8, 1);
        let pc = PedersenGens::default();

        cs.verify(&self.pf, &pc, &bp).is_ok()
    }
}

/// An unsatisfiable relation
fn impossible_relation<CS: ConstraintSystem>(
    cs: &mut CS,
    x: Variable,
    y: Variable,
    z: Variable,
    c: &[Scalar; 2],
) {
    // require x != 0
    let (_, _, one) = cs.multiply(x.into(), y.into());
    cs.constrain(one - Scalar::one());

    // require x == 0
    cs.constrain(x.into());

    // z * c.0 == c.1
    cs.constrain(z * c[0] - c[1])
}

fn main() {
    println!("provide proof:");

    // read a hex encoded proof
    let stdin = std::io::stdin();
    let mut lines = stdin.lock().lines();
    let bs = hex::decode(lines.next().unwrap().unwrap()).unwrap();
    let proof: Proof = bincode::deserialize(&bs).unwrap();

    // check validity
    if proof.verify() {
        // give them the flag
        let flag = fs::read_to_string("./flag.txt").unwrap();
        println!("{}", flag);
    }
}
