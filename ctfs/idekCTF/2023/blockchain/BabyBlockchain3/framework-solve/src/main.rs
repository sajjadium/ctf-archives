use chall::anchor_lang::{InstructionData, ToAccountMetas, system_program};
use solana_program::pubkey::Pubkey;
use std::net::TcpStream;
use std::{error::Error, fs, io::prelude::*, io::BufReader, str::FromStr};


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
    let mut stream = TcpStream::connect("127.0.0.1:1337")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());

    let mut line = String::new();

    let so_data = fs::read("./solve/target/deploy/solve.so")?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", solve::ID)?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;
    stream.write_all(&so_data)?;


    let chall_id = chall::ID;

    let mint         = Pubkey::from_str(&get_line(&mut reader)?)?;
    let admin        = Pubkey::from_str(&get_line(&mut reader)?)?;
    let config       = Pubkey::from_str(&get_line(&mut reader)?)?;
    let reserve      = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user         = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_record  = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_account = Pubkey::from_str(&get_line(&mut reader)?)?;

    println!("");
    println!("mint         : {}", mint);
    println!("admin        : {}", admin);
    println!("config       : {}", config);
    println!("reserve      : {}", reserve);
    println!("user         : {}", user);
    println!("user_record  : {}", user_record);
    println!("user_account : {}", user_account);
    println!("");

    let ix = solve::instruction::Initialize {};
    let data = ix.data();

    let ix_accounts = solve::accounts::Initialize {
        admin,
        config,
        reserve,
        user_record,
        user_account,
        user,
        mint,
        token_program: spl_token::ID,
        system_program: system_program::ID,
        chall: chall_id,
        rent: solana_program::sysvar::rent::ID,
    };

    let metas = ix_accounts.to_account_metas(None);

    reader.read_line(&mut line)?;
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

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", data.len())?;
    stream.write_all(&data)?;

    stream.flush()?;

    line.clear();
    while reader.read_line(&mut line)? != 0 {
        print!("{}", line);
        line.clear();
    }

    Ok(())
}
