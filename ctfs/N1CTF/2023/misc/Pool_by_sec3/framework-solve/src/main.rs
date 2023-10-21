use solana_program::pubkey::Pubkey;
use std::net::TcpStream;
use std::{error::Error, fs, io::prelude::*, io::BufReader, str::FromStr};
use solana_program::system_program;


fn get_line<R: Read>(reader: &mut BufReader<R>) -> Result<String, Box<dyn Error>> {
    let mut line = String::new();
    reader.read_line(&mut line)?;
    let ret = line
        .split(':')
        .nth(1)
        .ok_or("invalid input")?
        .trim()
        .to_string();
    Ok(ret)
}


fn main() -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::connect("localhost:1337")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());

    let mut line = String::new();

    let so_data = fs::read("./solve/target/deploy/solve.so")?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", solve::ID)?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;
    stream.write_all(&so_data)?;

    let chall_id = chall::ID;

    let admin               = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user                = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_token_account  = Pubkey::from_str(&get_line(&mut reader)?)?;
    let pool                = Pubkey::from_str(&get_line(&mut reader)?)?;
    let mint                = Pubkey::from_str(&get_line(&mut reader)?)?;

    println!("");
    println!("admin              : {}", admin);
    println!("user               : {}", user);
    println!("user_token_account : {}", user_token_account);
    println!("pool               : {}", pool);
    println!("mint               : {}", mint);
    println!("");

    
    // if you don't know what this is doing, look at server code and also sol-ctf-framework read_instruction:
    // https://github.com/otter-sec/sol-ctf-framework/blob/rewrite-v2/src/lib.rs#L237
    // feel free to change the accounts and ix data etc. to whatever you want

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", 10)?; // # of accounts

    writeln!(stream, "m {}", admin)?;
    writeln!(stream, "mws {}", user)?;
    writeln!(stream, "mw {}", user_token_account)?;
    writeln!(stream, "mw {}", pool)?;
    writeln!(stream, "mw {}", mint)?;
    writeln!(stream, "m {}", chall_id)?;
    writeln!(stream, "m {}", solana_program::sysvar::rent::ID)?;
    writeln!(stream, "m {}", spl_token::id())?;
    writeln!(stream, "m {}", spl_associated_token_account::id())?;
    writeln!(stream, "m {}", system_program::ID)?;

    stream.flush()?;

    reader.read_line(&mut line)?;
    writeln!(stream, "0")?; // ix data len

    stream.flush()?;

    line.clear();
    while reader.read_line(&mut line)? != 0 {
        print!("{}", line);
        line.clear();
    }

    Ok(())
}