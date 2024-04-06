pub const MOD: u32 = 1e9 as u32 + 9;

pub mod gen;
pub mod omniscient_god;

pub fn validate_string(s: &str) {
    for c in s.chars() {
        // orz larry
        assert!("ozly".contains(c));
    }
}

pub mod my_code {
    use super::{validate_string, MOD};
    use std::collections::HashSet;

    struct Solver {
        str: Vec<u8>,
        vis: HashSet<Vec<u8>>,
        ans: u32,
    }

    impl Solver {
        fn solve(s: String) -> u32 {
            validate_string(&s);

            let mut solver = Self {
                str: s.into_bytes(),
                vis: HashSet::new(),
                ans: 0,
            };
            solver.str.sort_unstable();

            for &c in b"ozly" {
                solver.dfs(vec![c]);
            }

            solver.ans
        }

        fn dfs(&mut self, mut s: Vec<u8>) {
            if !self.vis.insert(s.clone()) {
                return;
            } else if s.len() == self.str.len() {
                // check s is a permutation of `self.str`
                s.sort_unstable();

                if s == self.str {
                    self.ans = (self.ans + 1) % MOD;
                }
                return;
            }

            for i in 0..s.len() {
                // perform an expansion - replace s[i] with some 2 character string
                let expansions = match s[i] {
                    b'o' => [b"lo", b"oy"],
                    b'z' => [b"yz", b"zl"],
                    b'l' => [b"ll", b"oz"],
                    b'y' => [b"yy", b"zo"],
                    _ => unreachable!(),
                };

                for expansion in expansions {
                    let mut next = s.clone();
                    next.splice(i..=i, expansion.iter().copied());

                    self.dfs(next);
                }
            }
        }
    }

    pub fn solve(s: &str) -> u32 {
        Solver::solve(s.to_string())
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
            let s = gen::rand_string(&mut rng, 1, 10);

            assert_eq!(my_code::solve(&s), omniscient_god::solve(&s));
        }
    }
}
