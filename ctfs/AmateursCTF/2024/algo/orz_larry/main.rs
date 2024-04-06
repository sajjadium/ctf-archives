use orz_larry::{gen, omniscient_god};
use std::io::{self, BufRead, BufWriter, Write};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stdin = io::stdin().lock();

    let mut rng = rand::thread_rng();
    let mut queries = vec![];

    queries.push(gen::rand_string(&mut rng, 9e4 as usize, 1e5 as usize));
    for _ in 0..100 {
        queries.push(gen::rand_string(&mut rng, 1, 1000));
    }

    let mut out = BufWriter::new(io::stdout().lock());
    writeln!(out, "{}", queries.len())?;
    for s in &queries {
        writeln!(out, "{s}")?;
    }
    out.flush()?;

    for s in &queries {
        let ans = omniscient_god::solve(s);
        let mut your_ans = String::new();
        stdin.read_line(&mut your_ans)?;

        if ans.to_string() != your_ans.trim() {
            panic!("the omniscient god disagrees - maybe you should worship him more?");
        }
    }

    println!(
        "Yay! Good job, here's your flag and remember to orz larry: {}",
        std::fs::read_to_string("./flag.txt")?
    );

    Ok(())
}
