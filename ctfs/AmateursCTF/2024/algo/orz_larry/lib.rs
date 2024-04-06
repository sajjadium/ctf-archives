pub const MOD: u32 = 1e9 as u32 + 9;

pub mod omniscient_god;

pub mod gen {
    use rand::prelude::*;

    const ALPHABET: &[u8] = b"orzlarryhowistheomniscientgodsoorzomgiwanttobelikehim:place_of_worship::star_struck:15969056191281289460760WOIGHOPWAPWQOPHAZQSWDFGBHJOP;L.HQWUORFHPztajawehuiprvgiugIP";

    pub fn rand_string(rng: &mut impl Rng, min_n: usize, max_n: usize) -> String {
        let n = rng.gen_range(min_n..=max_n);

        (0..n)
            .map(|_| ALPHABET[rng.gen_range(0..ALPHABET.len())] as char)
            .collect()
    }
}

pub mod my_code {
    use super::MOD;
    use std::collections::HashSet;

    fn on(mask: usize, bit: usize) -> bool {
        ((mask >> bit) & 1) == 1
    }

    pub fn solve(s: &str) -> u32 {
        let n = s.len();
        let arr = s.as_bytes();
        let mut ans = HashSet::new();

        for mask in 0..(1usize << n) {
            ans.insert(
                (0..n)
                    .filter(|&i| on(mask, i))
                    .map(|i| arr[i])
                    .collect::<Vec<_>>(),
            );
        }

        (ans.len() % (MOD as usize)) as u32
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// verify my brute force by comparing against the omniscient god
    #[test]
    fn stress_test() {
        let mut rng = rand::thread_rng();

        for _ in 0..1000 {
            let s = gen::rand_string(&mut rng, 1, 15);

            assert_eq!(my_code::solve(&s), omniscient_god::solve(&s));
        }
    }
}
