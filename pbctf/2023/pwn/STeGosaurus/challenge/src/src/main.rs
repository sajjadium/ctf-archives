#![feature(slice_as_chunks)]
#[macro_use]
mod obj;
mod il;
mod interp;

use std::{
    io::{stdin, stdout, Write},
    error::Error,
    process::ExitCode,
};

use base64::{Engine as _, engine::general_purpose};

fn main_with_err() -> Result<(), Box<dyn Error>>{
    let mut line = String::new();
    print!("Code: ");
    stdout().flush()?;
    stdin().read_line(&mut line)?;
    let data = general_purpose::STANDARD.decode(line.trim().as_bytes())?;
    let mut code = interp::RunState::new(bincode::deserialize(&data)?);
    code.entrypoint()?;

    Ok(())
}

fn main() -> ExitCode {
    match main_with_err() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("ERROR: {e}");
            ExitCode::FAILURE
        }
    }
}
