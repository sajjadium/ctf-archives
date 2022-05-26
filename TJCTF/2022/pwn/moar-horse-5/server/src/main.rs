use poc_framework_osec::{
    solana_sdk::signature::{
        Keypair,
        Signer,
    },
    Environment,
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::system_program;

use std::{
    fs,
    io::Write,
    error::Error,
    net::{
        TcpListener,
        TcpStream
    },
};

use threadpool::ThreadPool;

use moar_horse::{
    create, get_horse,
};

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
    let program_pubkey = builder.chall_programs(&["./moar_horse.so"])[0];

    // make user
    let user = Keypair::new();

    writeln!(socket, "program: {}", program_pubkey)?;
    writeln!(socket, "user: {}", user.pubkey())?;


    // add accounts and lamports
    let (horse, _) = get_horse(program_pubkey);

    const TARGET_AMT: u64 = 100_000;
    const INIT_BAL: u64 = 2_000;
    const VAULT_BAL: u64 = 1_000_000;

    builder
        .builder
        .add_account_with_lamports(user.pubkey(), system_program::ID, INIT_BAL);
    builder
        .builder
        .add_account_with_lamports(horse, system_program::ID, VAULT_BAL);

    let mut challenge = builder.build();

    // create a horsewallet
    challenge.env.execute_as_transaction(
        &[create(program_pubkey, user.pubkey())],
        &[&user],
    );

    // run solve
    challenge.input_instruction(solve_pubkey, &[&user]).unwrap();

    // check solve
    let balance = challenge.env.get_account(user.pubkey()).unwrap().lamports;
    writeln!(socket, "lamports: {:?}", balance)?;

    if balance > TARGET_AMT {
        let flag = fs::read_to_string("flag.txt").unwrap();
        writeln!(socket, "hhhhhhhoooooooooooorrrrrrrrrrrrrrrssssssssssssssssseeeeeeeeeeeeeeeeeee\nFlag: {}", flag)?;
    }

    Ok(())
}
