use std::io::Read;

struct Random {
    seed: i32
}

impl Random {
    fn rand(&mut self) -> i32 {
        let a = 1103515245;
        let c = 12345;
        self.seed = self.seed.wrapping_mul(a) + c;
        (self.seed >> 16) & 0x7fff
    }
}

fn generate_password(rand: &mut Random, n: i32) -> String {
    (0..n).map(|_| (rand.rand() % (0x7f - 0x21) + 0x21) as u8 as char).collect::<String>()
}

fn main() -> std::io::Result<()> {
    let seed = {
        let mut os_rand = std::fs::File::open("/dev/urandom")?;
        let mut rand_bytes = [0; 4];
        os_rand.read(&mut rand_bytes)?;
        i32::from_le_bytes(rand_bytes)
    };
    let mut rand = Random {
        seed
    };

    let stdin = std::io::stdin();
    loop {
        println!("Howdy!  How many passwords would you like to generate? ");
        let mut line = String::new();
        stdin.read_line(&mut line)?;
        if let Ok(num) = line.trim().parse::<i32>() {
            for _ in 0..num {
                println!("{}", generate_password(&mut rand, 8));
            }
            std::process::exit(0)
        } else {
            println!("That doesn't look like a number...");
        }
    }
}
