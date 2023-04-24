use borsh::BorshSerialize;

use poc_framework_osec::{
    solana_sdk::{
        instruction::{AccountMeta, Instruction},
        pubkey::Pubkey,
        signature::{Keypair, Signer},
    },
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

use rand::prelude::*;

use threadpool::ThreadPool;

#[derive(Debug, Clone, BorshSerialize, PartialEq, Eq, PartialOrd, Ord)]
pub enum SailorInstruction {
    CreateUnion(u64),
    PayDues(u64),
    StrikePay(u64),
    RegisterMember([u8; 32]),
}

fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:5000")?;
    let pool = ThreadPool::new(4);
    for stream in listener.incoming() {
        let mut stream = stream.unwrap();

        pool.execute(move || {
            if let Err(e) = handle_connection(&mut stream) {
                println!("got error: {:?}", e);
                writeln!(stream, "Got error, exiting...").ok();
            }
            stream.shutdown(std::net::Shutdown::Both).ok();
        });
    }
    Ok(())
}

fn handle_connection(socket: &mut TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone()?)?;

    let mut rng = StdRng::from_seed([42; 32]);

    // put program at a fixed pubkey to make anchor happy
    let prog = Keypair::generate(&mut rng);

    // load programs
    let solve_pubkey = builder.input_program()?;
    builder
        .builder
        .add_program(prog.pubkey(), "sailors_revenge.so");

    // make user
    let user = Keypair::new();
    let rich_boi = Keypair::new();
    let (vault, _) = Pubkey::find_program_address(&[b"vault"], &prog.pubkey());
    let (sailor_union, _) =
        Pubkey::find_program_address(&[b"union", rich_boi.pubkey().as_ref()], &prog.pubkey());
    let (registration, _) = Pubkey::find_program_address(
        &[
            b"registration",
            rich_boi.pubkey().as_ref(),
            user.pubkey().as_ref(),
        ],
        &prog.pubkey(),
    );

    writeln!(socket, "program: {}", prog.pubkey())?;
    writeln!(socket, "user: {}", user.pubkey())?;
    writeln!(socket, "vault: {}", vault)?;
    writeln!(socket, "sailor union: {}", sailor_union)?;
    writeln!(socket, "registration: {}", registration)?;
    writeln!(socket, "rich boi: {}", rich_boi.pubkey())?;
    writeln!(socket, "system program: {}", system_program::id())?;

    // add accounts and lamports

    const TARGET_AMT: u64 = 100_000_000;
    const INIT_BAL: u64 = 1337;
    const TOTAL_BAL: u64 = 1_000_000_000;
    const VAULT_BAL: u64 = 500_000_000;

    builder
        .builder
        .add_account_with_lamports(vault, system_program::id(), INIT_BAL)
        .add_account_with_lamports(rich_boi.pubkey(), system_program::id(), TOTAL_BAL)
        .add_account_with_lamports(user.pubkey(), system_program::id(), INIT_BAL);

    let mut challenge = builder.build();

    challenge.env.execute_as_transaction(
        &[Instruction::new_with_borsh(
            prog.pubkey(),
            &SailorInstruction::CreateUnion(VAULT_BAL),
            vec![
                AccountMeta::new(sailor_union, false),
                AccountMeta::new(rich_boi.pubkey(), true),
                AccountMeta::new(vault, false),
                AccountMeta::new_readonly(system_program::id(), false),
            ],
        )],
        &[&rich_boi],
    );

    challenge.env.execute_as_transaction(
        &[Instruction::new_with_borsh(
            prog.pubkey(),
            &SailorInstruction::RegisterMember(user.pubkey().to_bytes()),
            vec![
                AccountMeta::new(registration, false),
                AccountMeta::new_readonly(sailor_union, false),
                AccountMeta::new(rich_boi.pubkey(), true),
                AccountMeta::new_readonly(system_program::id(), false),
            ],
        )],
        &[&rich_boi],
    );

    // run solve
    challenge.input_instruction(solve_pubkey, &[&user])?;

    // check solve
    let balance = challenge
        .env
        .get_account(user.pubkey())
        .ok_or("could not find user")?
        .lamports;
    writeln!(socket, "lamports: {:?}", balance)?;

    if balance > TARGET_AMT {
        let flag = fs::read_to_string("flag.txt")?;
        writeln!(
            socket,
            "You successfully exploited the working class and stole their union dues! Congratulations!\nFlag: {}",
            flag.trim()
        )?;
    } else {
        writeln!(socket, "That's not enough to get the flag!")?;
    }

    Ok(())
}
