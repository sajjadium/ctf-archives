use ark_ec::{pairing::Pairing, scalar_mul::fixed_base::FixedBase, CurveGroup};
use ark_ff::{fields::PrimeField, One, UniformRand};
use ark_poly_commit::kzg10::{Powers, UniversalParams, VerifierKey};
use ark_poly_commit::Error;
use rand_core::RngCore;
use std::{collections::BTreeMap, ops::Mul};

pub fn setup_with_beta<E: Pairing, R: RngCore>(
    max_degree: usize,
    produce_g2_powers: bool,
    beta: E::ScalarField,
    rng: &mut R,
) -> Result<UniversalParams<E>, Error> {
    if max_degree < 1 {
        return Err(Error::DegreeIsZero);
    }
    let g = E::G1::rand(rng);
    let gamma_g = E::G1::rand(rng);
    let h = E::G2::rand(rng);

    let mut powers_of_beta = vec![E::ScalarField::one()];

    let mut cur = beta;
    for _ in 0..max_degree {
        powers_of_beta.push(cur);
        cur *= &beta;
    }

    let window_size = FixedBase::get_mul_window_size(max_degree + 1);

    let scalar_bits = E::ScalarField::MODULUS_BIT_SIZE as usize;
    let g_table = FixedBase::get_window_table(scalar_bits, window_size, g);
    let powers_of_g = FixedBase::msm::<E::G1>(scalar_bits, window_size, &g_table, &powers_of_beta);
    let gamma_g_table = FixedBase::get_window_table(scalar_bits, window_size, gamma_g);
    let mut powers_of_gamma_g =
        FixedBase::msm::<E::G1>(scalar_bits, window_size, &gamma_g_table, &powers_of_beta);
    // Add an additional power of gamma_g, because we want to be able to support
    // up to D queries.
    powers_of_gamma_g.push(powers_of_gamma_g.last().unwrap().mul(&beta));

    let powers_of_g = E::G1::normalize_batch(&powers_of_g);
    let powers_of_gamma_g = E::G1::normalize_batch(&powers_of_gamma_g)
        .into_iter()
        .enumerate()
        .collect();

    let neg_powers_of_h = if produce_g2_powers {
        let mut neg_powers_of_beta = vec![E::ScalarField::one()];
        let mut cur = E::ScalarField::one() / beta;
        for _ in 0..max_degree {
            neg_powers_of_beta.push(cur);
            cur /= &beta;
        }

        let neg_h_table = FixedBase::get_window_table(scalar_bits, window_size, h);
        let neg_powers_of_h =
            FixedBase::msm::<E::G2>(scalar_bits, window_size, &neg_h_table, &neg_powers_of_beta);

        let affines = E::G2::normalize_batch(&neg_powers_of_h);
        let mut affines_map = BTreeMap::new();
        affines.into_iter().enumerate().for_each(|(i, a)| {
            affines_map.insert(i, a);
        });
        affines_map
    } else {
        BTreeMap::new()
    };

    let h = h.into_affine();
    let beta_h = h.mul(beta).into_affine();
    let prepared_h = h.into();
    let prepared_beta_h = beta_h.into();

    let pp = UniversalParams {
        powers_of_g,
        powers_of_gamma_g,
        h,
        beta_h,
        neg_powers_of_h,
        prepared_h,
        prepared_beta_h,
    };
    Ok(pp)
}

pub fn trim<E: Pairing>(
    pp: &UniversalParams<E>,
    mut supported_degree: usize,
) -> Result<(Powers<E>, VerifierKey<E>), Error> {
    if supported_degree == 1 {
        supported_degree += 1;
    }
    let powers_of_g = pp.powers_of_g[..=supported_degree].to_vec();
    let powers_of_gamma_g = (0..=supported_degree)
        .map(|i| pp.powers_of_gamma_g[&i])
        .collect();

    let powers = Powers {
        powers_of_g: ark_std::borrow::Cow::Owned(powers_of_g),
        powers_of_gamma_g: ark_std::borrow::Cow::Owned(powers_of_gamma_g),
    };
    let vk = VerifierKey {
        g: pp.powers_of_g[0],
        gamma_g: pp.powers_of_gamma_g[&0],
        h: pp.h,
        beta_h: pp.beta_h,
        prepared_h: pp.prepared_h.clone(),
        prepared_beta_h: pp.prepared_beta_h.clone(),
    };
    Ok((powers, vk))
}
