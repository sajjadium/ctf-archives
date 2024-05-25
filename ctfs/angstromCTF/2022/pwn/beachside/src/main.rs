use poc_framework_osec::solana_sdk::signature::Keypair;
use poc_framework_osec::solana_sdk::signature::Signer;
use poc_framework_osec::Environment;
use sol_ctf_framework::ChallengeBuilder;
use solana_program::pubkey::Pubkey;
use solana_program::system_program;
use std::env;
use std::io::Write;
use std::{
    error::Error,
    net::{TcpListener, TcpStream},
};
use threadpool::ThreadPool;

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;
    let pool = ThreadPool::new(4);
    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream).unwrap();
        });
    }
    Ok(())
}

fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    let solve_pubkey = builder.input_program().unwrap();
    let program_pubkey = builder.chall_programs(&["./beachside.so"])[0];

    let user = Keypair::new();

    writeln!(socket, "program pubkey: {}", program_pubkey)?;
    writeln!(socket, "solve pubkey: {}", solve_pubkey)?;
    writeln!(socket, "user pubkey: {}", user.pubkey())?;

    let (vault, _) = Pubkey::find_program_address(&["vault".as_ref()], &program_pubkey);

    const TARGET_AMT: u64 = 50_000;
    const INIT_BAL: u64 = 10;
    const VAULT_BAL: u64 = 1_000_000;

    builder
        .builder
        .add_account_with_lamports(user.pubkey(), system_program::ID, INIT_BAL);
    builder
        .builder
        .add_account_with_lamports(vault, system_program::ID, VAULT_BAL);

    let mut challenge = builder.build();

    challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

    let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;

    writeln!(socket, "user bal: {:?}", balance)?;
    writeln!(
        socket,
        "vault bal: {:?}",
        challenge.env.get_account(vault).unwrap().lamports
    )?;

    if balance > TARGET_AMT {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    }

    Ok(())
}