use rand::prelude::*;

pub fn rand_string(rng: &mut impl Rng, min_n: usize, max_n: usize) -> String {
    let n = rng.gen_range(min_n..=max_n);

    let mut arr = vec![];

    {
        let m = rng.gen_range(n / 4..=3 * n / 4);
        let mut o = m / 2;
        let mut z = m - o;

        if rng.gen::<bool>() {
            std::mem::swap(&mut o, &mut z);
        }

        arr.extend(std::iter::repeat('o').take(o));
        arr.extend(std::iter::repeat('z').take(z));
    }

    while arr.len() < n {
        arr.push(if rng.gen::<bool>() { 'l' } else { 'y' });
    }

    arr.shuffle(rng);

    arr.into_iter().collect()
}
