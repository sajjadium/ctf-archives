use chall::anchor_lang::{InstructionData, ToAccountMetas};
use chall::{POOL_A_SEED, POOL_B_SEED, SWAP_SEED};
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
    let mut stream = TcpStream::connect("127.0.0.1:8080")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());

    let mut line = String::new();

    let so_data = fs::read("./solve/target/deploy/solve.so")?;

    reader.read_line(&mut line)?;
    writeln!(stream, "{}", solve::ID)?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;
    stream.write_all(&so_data)?;

    let chall_id = chall::ID;

    let payer = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user = Pubkey::from_str(&get_line(&mut reader)?)?;
    let _mint_a = Pubkey::from_str(&get_line(&mut reader)?)?;
    let _mint_b = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_in_account = Pubkey::from_str(&get_line(&mut reader)?)?;
    let user_out_account = Pubkey::from_str(&get_line(&mut reader)?)?;

    let ix = solve::instruction::Initialize {};
    let data = ix.data();

    let swap = Pubkey::find_program_address(&[SWAP_SEED, payer.as_ref()], &chall_id).0;
    let pool_a = Pubkey::find_program_address(&[POOL_A_SEED, swap.as_ref()], &chall_id).0;
    let pool_b = Pubkey::find_program_address(&[POOL_B_SEED, swap.as_ref()], &chall_id).0;

    let ix_accounts = solve::accounts::Initialize {
        swap,
        pool_a,
        pool_b,
        user_in_account,
        user_out_account,
        payer: user,
        token_program: spl_token::ID,
        chall: chall_id,
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
