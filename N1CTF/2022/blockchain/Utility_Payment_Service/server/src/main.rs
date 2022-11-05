use poc_framework_osec::{
    solana_sdk::signature::{Keypair, Signer},
    Environment,
    // setup_logging, LogLevel,
    // PrintableTransaction,
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::{system_program};

use std::{
    error::Error,
    fs,
    io::Write,
    net::{TcpListener, TcpStream},
};

use threadpool::ThreadPool;

use utility_payment::{processor::{get_reserve}};

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:5000")?;
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

    // load programs
    let solve_pubkey = builder.input_program().unwrap();
    let program_pubkey = builder.chall_programs(&["./utility_payment.so"])[0];

    // make user
    let user = Keypair::new();

    writeln!(socket, "program pubkey: {}", program_pubkey)?;
    writeln!(socket, "solve pubkey: {}", solve_pubkey)?;
    writeln!(socket, "user pubkey: {}", user.pubkey())?;

    // println!("program: {}", program_pubkey);

    // add accounts and lamports
    let (reserve, _) = get_reserve(program_pubkey);
    // let (escrow, _) =  get_escrow(program_pubkey, user.pubkey());

    const TARGET_AMT: u64 = 60_000;
    const INIT_BAL: u64 = 50;
    const RESERVE_BAL: u64 = 1_000_000;

    builder
        .builder
        .add_account_with_lamports(user.pubkey(), system_program::ID, INIT_BAL);
    builder
        .builder
        .add_account_with_lamports(reserve, system_program::ID, RESERVE_BAL);

    let mut challenge = builder.build();

    let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;
    writeln!(socket, "user lamport before: {:?}", balance)?;

    // run solve
    challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

    // check solve
    let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;
    writeln!(socket, "user lamport after: {:?}", balance)?;

    if balance > TARGET_AMT {
        let flag = fs::read_to_string("flag.txt").unwrap();
        writeln!(
            socket,
            "Flag: {}",
            flag
        )?;
    }

    Ok(())
}
