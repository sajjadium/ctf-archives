use anchor_lang::{InstructionData, ToAccountMetas};
use solana_program::pubkey::Pubkey;
use std::net::TcpStream;
use std::{error::Error, fs, io::prelude::*, io::BufReader, str::FromStr};
use std::path::PathBuf;
use std::ptr::write;
use solana_program::pubkey;

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

fn read_until_line<R: Read>(reader: &mut BufReader<R>, s: &str) -> Result<String, Box<dyn Error>> {
    assert!(s.ends_with('\n'));

    let mut lines = String::new();
    reader.read_line(&mut lines)?;
    while !lines.contains(s) {
        reader.read_line(&mut lines)?;
    }

    Ok(lines)
}

fn read_forever<R: Read>(reader: &mut BufReader<R>) {
    let mut line = String::new();
    while match reader.read_line(&mut line) {
        Ok(0) => false,
        Ok(_) => {
            println!("Read: {}", line);
            line.clear();
            true
        }
        _ => false
    } {}
}

fn send_program(stream: &mut TcpStream, pubkey: Pubkey, path: &PathBuf) -> Result<(), std::io::Error> {
    let mut reader = BufReader::new(stream.try_clone().unwrap());
    let mut line = String::new();

    let so_data = fs::read(path)?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", pubkey)?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;

    stream.write_all(&so_data)
}

fn send_ix<IX: InstructionData, IXA: ToAccountMetas>(stream: &mut TcpStream, ix: &IX, ix_accounts: &IXA) -> Result<(), std::io::Error> {
    let metas = ix_accounts.to_account_metas(None);

    writeln!(stream, "{}", metas.len())?;
    for meta in metas {
        let mut meta_str = String::new();
        meta_str.push('m');
        if meta.is_writable {
            meta_str.push('w');
        }
        if meta.is_signer {
            meta_str.push('s');
        }
        meta_str.push(' ');
        meta_str.push_str(&meta.pubkey.to_string());

        writeln!(stream, "{}", meta_str)?;
        stream.flush()?;
    }

    let data = ix.data();
    writeln!(stream, "{}", data.len())?;
    stream.write_all(&data)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());

    // let chall = chall::ID;
    let solve = solve::ID;

    send_program(&mut stream, solve::ID, &PathBuf::from_str("./solve/target/deploy/solve.so").unwrap())?;

    println!("Sent program");

    read_until_line(&mut reader, "Accounts:\n")?;
    let program = Pubkey::from_str(&get_line(&mut reader)?)?;
    let mint = Pubkey::from_str(&get_line(&mut reader)?)?;
    let vault = Pubkey::from_str(&get_line(&mut reader)?)?;
    let vault_token = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_token = Pubkey::from_str(&get_line(&mut reader)?)?;

    dbg!(
        program,
        mint,
        vault,
        vault_token,
        user,
        user_token
    );

    println!("Sending ix");
    let ix = solve::instruction::Initialize{};
    let ix_accounts = solve::accounts::Initialize {
        // TODO
    };
    send_ix(&mut stream, &ix, &ix_accounts)?;

    println!("Sent ix");

    // It's important to keep the socket open, or the server will terminate early
    read_forever(&mut reader);

    Ok(())
}