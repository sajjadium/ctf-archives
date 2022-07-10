// base: https://github.com/otter-sec/sol-ctf-framework/tree/main/examples/moar-horse-5

use poc_framework_osec::{
    solana_sdk::signature::{Keypair, Signer},
    Environment,
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::system_program;

use std::{
    error::Error,
    fs,
    io::Write,
    net::{TcpListener, TcpStream},
};

use threadpool::ThreadPool;

use solnote::get_vault;

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
    let program_pubkey = builder.chall_programs(&["./solnote.so"])[0];

    // make user
    let user = Keypair::new();

    writeln!(socket, "program: {}", program_pubkey)?;
    writeln!(socket, "user: {}", user.pubkey())?;

    // add accounts and lamports
    let (vault, _) = get_vault(program_pubkey);

    // beeg money
    const TARGET_AMT: u64 = 50_000_000_000_000;
    const INIT_BAL: u64 = 10_000;
    const VAULT_BAL: u64 = 100_000_000_000_000;

    builder
        .builder
        .add_account_with_lamports(user.pubkey(), system_program::ID, INIT_BAL);
    builder
        .builder
        .add_account_with_lamports(vault, program_pubkey, VAULT_BAL);

    let mut challenge = builder.build();

    // run solve
    challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

    // check solve
    let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;
    writeln!(socket, "lamports: {:?}", balance)?;

    if balance > TARGET_AMT {
        let flag = fs::read_to_string("flag.txt").unwrap();
        writeln!(socket, "your did it!\nFlag: {}", flag)?;
    }

    Ok(())
}
