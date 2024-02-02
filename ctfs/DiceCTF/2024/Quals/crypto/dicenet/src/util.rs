use fancy_garbling::util as numbers;
use itertools::Itertools;
use ndarray::Array3;
use serde_json::Value;
use std::fs::File;
use std::io::prelude::*;
use std::io::{BufReader, Lines};

pub fn index_of_max(xs: &[i64]) -> usize {
    let mut max_val = i64::min_value();
    let mut max_ix = 0;
    for (i, &x) in xs.iter().enumerate() {
        if x > max_val {
            max_ix = i;
            max_val = x;
        }
    }
    max_ix
}

pub fn get_lines(file: &str) -> Lines<BufReader<File>> {
    let f = File::open(file).expect("file not found");
    let r = BufReader::new(f);
    r.lines()
}

pub fn to_mod_q(x: i64, q: u128) -> u128 {
    assert!(
        ((x as i128) >= 0 && (x as i128) < q as i128 / 2)
            || ((x as i128) < 0 && (x as i128) >= -(q as i128 / 2)),
        "x={} is too large/small for q={}",
        x,
        q
    );
    ((q as i128 + x as i128) % q as i128) as u128
}

pub fn from_mod_q(x: u128, q: u128) -> i64 {
    if x >= q / 2 {
        (x as i128 - q as i128) as i64
    } else {
        x as i64
    }
}

pub fn to_mod_q_crt(x: i64, q: u128) -> Vec<u16> {
    numbers::crt_factor(to_mod_q(x, q), q)
}

pub fn from_mod_q_crt(xs: &[u16], q: u128) -> i64 {
    from_mod_q(numbers::crt_inv_factor(xs, q), q)
}

pub fn twos_complement_negate(x: u128, nbits: usize) -> u128 {
    let mask = (1 << nbits) - 1;
    ((!x) & mask) + 1
}

pub fn i64_to_twos_complement(x: i64, nbits: usize) -> u128 {
    if x >= 0 {
        x as u128
    } else {
        twos_complement_negate((-x) as u128, nbits)
    }
}

pub fn i64_from_twos_complement(x: u128, nbits: usize) -> i64 {
    if x >= 1 << (nbits - 1) {
        -(twos_complement_negate(x, nbits) as i64)
    } else {
        x as i64
    }
}

pub fn i64_to_bits(x: i64, nbits: usize) -> Vec<u16> {
    let twos = i64_to_twos_complement(x, nbits);
    numbers::u128_to_bits(twos, nbits)
}

pub fn i64_from_bits(bits: &[u16]) -> i64 {
    let x = numbers::u128_from_bits(bits);
    i64_from_twos_complement(x, bits.len())
}

pub fn value_to_array3(v: &Value) -> Array3<i64> {
    let rows = v.as_array().expect("value is not an array!");

    let data = rows
        .into_iter()
        .map(|cols| {
            if cols.is_array() {
                cols.as_array()
                    .unwrap()
                    .into_iter()
                    .map(|deps| {
                        if deps.is_array() {
                            deps.as_array()
                                .expect("expected colors!")
                                .into_iter()
                                .map(|val| val.as_i64().expect("expected a number!"))
                                .collect_vec()
                        } else {
                            vec![deps.as_i64().unwrap()]
                        }
                    })
                    .collect_vec()
            } else {
                vec![vec![cols.as_i64().unwrap()]]
            }
        })
        .collect_vec();

    let height = data.len();
    let width = data[0].len();
    let depth = data[0][0].len();

    Array3::from_shape_vec(
        (height, width, depth),
        data.into_iter().flatten().flatten().collect(),
    )
    .expect("couldnt create array!")
}

/// encode the inputs into CRT
pub fn encode_crt(input: impl Iterator<Item = i64>, modulus: u128) -> Vec<u16> {
    input.flat_map(|x| to_mod_q_crt(x, modulus)).collect()
}

/// decode the inputs from CRT
pub fn decode_crt(output: &[u16], modulus: u128) -> Vec<i64> {
    let nprimes = numbers::factor(modulus).len();
    output
        .chunks(nprimes)
        .map(|xs| from_mod_q_crt(xs, modulus))
        .collect()
}

/// Encode some inputs as bits.
pub fn encode_binary(input: impl Iterator<Item = i64>, nbits: usize) -> Vec<u16> {
    input.flat_map(|x| i64_to_bits(x, nbits)).collect()
}

/// Decode the output array from bits.
pub fn decode_binary(output: &[u16], nbits: usize) -> Vec<i64> {
    output.chunks(nbits).map(|xs| i64_from_bits(xs)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::{thread_rng, Rng};

    #[test]
    fn convert_crt() {
        let mut rng = thread_rng();
        for _ in 0..1024 {
            let nprimes = 2_usize + (rng.gen::<usize>() % 16);
            let q = numbers::modulus_with_nprimes(nprimes);
            let x = rng.gen::<i64>() % (q / 2) as i64;
            assert_eq!(x, from_mod_q_crt(&to_mod_q_crt(x, q), q));
        }
    }

    #[test]
    fn convert_binary() {
        let mut rng = thread_rng();
        let nbits = 2 + rng.gen::<usize>() % 120;
        for _ in 0..128 {
            let x = rng.gen::<i64>() % nbits as i64;
            assert_eq!(
                x,
                i64_from_twos_complement(i64_to_twos_complement(x, nbits), nbits)
            );
        }
    }

    #[test]
    fn binary_encoding() {
        let mut rng = thread_rng();
        let nbits = 64;
        let x = rng.gen::<i64>() % (1 << 32);
        let bits = i64_to_bits(x, nbits);
        let y = i64_from_bits(&bits);
        assert_eq!(x, y);
    }
}
