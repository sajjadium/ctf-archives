const P: u128 = 1054189786189;
const ROUNDS: usize = 2_usize.pow(24);
const BLOCK_SIZE: usize = 36;

pub fn mimc(bits: &[bool], key: u64) -> Vec<bool> {
    let chunks = bits
        .chunks(BLOCK_SIZE)
        .map(|chunk| {
            chunk
                .iter()
                .fold(0u64, |acc, &bit| (acc << 1) + if bit { 1 } else { 0 })
        })
        .collect::<Vec<u64>>();

    let chunks = mimc_chunks(&chunks, key);

    let mut bits = vec![false; 4];
    for chunk in chunks {
        let mut chunk_bits = Vec::new();
        for i in 0..BLOCK_SIZE {
            chunk_bits.push(((chunk >> i) & 1) == 1);
        }
        chunk_bits.reverse();
        bits.extend(chunk_bits);
    }

    bits
}

fn mimc_chunks(chunks: &[u64], key: u64) -> Vec<u64> {
    chunks.iter().map(|chunk| mimc_block(chunk, &key)).collect()
}

fn mimc_block(x: &u64, key: &u64) -> u64 {
    (0..ROUNDS).fold(*x, |acc, _| mimc_round(acc, *key))
}

fn mimc_round(x: u64, key: u64) -> u64 {
    let x = (x as u128) % P;
    let key = (key as u128) % P;
    let c = (x + key) % P;
    (c.wrapping_mul(c).wrapping_mul(c) % P) as u64
}
