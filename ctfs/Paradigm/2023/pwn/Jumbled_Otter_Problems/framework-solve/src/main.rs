use solana_program::{instruction::AccountMeta, pubkey::Pubkey};
use std::net::TcpStream;
use std::{error::Error, io::prelude::*, io::BufReader, str::FromStr};

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
    println!("running");

    let mut stream = TcpStream::connect("127.0.0.1:1337")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());

    let mut line = String::new();

    let _user = Pubkey::from_str(&get_line(&mut reader)?)?;

    // TODO
    let data: Vec<u8> = vec![];
    let metas: Vec<AccountMeta> = vec![];
    // TODO

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
