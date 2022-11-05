
mod arm64;
mod vm;
use crate::vm::{VM};
use std::{io, io::Read, io::Write};

fn get_code() -> Result<Vec<u8>, io::Error> {
    print!("Enter code size: ");
    io::stdout().flush().unwrap();

    let mut input_line = String::new();
    io::stdin()
        .read_line(&mut input_line)
        .expect("Failed to read Code size");
    let len: usize = input_line.trim().parse().expect("Code size not an integer");
    let mut stdin = io::stdin();
    let mut v = vec![0u8; len];

    print!("Enter code: ");
    io::stdout().flush().unwrap();
    stdin.read_exact(&mut v)?;
    return Ok(v);
}

fn main() {
    let mut vm = VM::new(0x10000);
    let code = get_code().expect("Could not read input");
    vm.compile(code.as_slice());

    // Get input integer
    print!("Enter input (u64): ");
    io::stdout().flush().unwrap();

    let mut input_line = String::new();
    io::stdin()
        .read_line(&mut input_line)
        .expect("Failed to read size");
    let input: u64 = input_line.trim().parse().expect("Input not an integer");

    let result = vm.execute(input);
    println!("result: {}", result);
}
