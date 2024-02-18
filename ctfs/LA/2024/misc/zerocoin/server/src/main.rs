use anchor_lang::{InstructionData, ToAccountMetas};
use solana_sdk::{
    instruction::Instruction,
    pubkey::Pubkey,
    signature::{Keypair, Signer},
};

use sol_ctf_framework::ChallengeBuilder;

use solana_program::{program_pack::Pack, system_instruction, system_program};

use std::{
    error::Error,
    fs,
    io::Write,
    net::{TcpListener, TcpStream},
};

use rand::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:5000")?;

    println!("Server listening on port 5000");

    for stream in listener.incoming() {
        let mut stream = stream.unwrap();

        tokio::spawn(async move {
            if let Err(err) = handle_connection(&mut stream).await {
                writeln!(stream, "error: {:?}", err).ok();
            }
        });
    }
    Ok(())
}

async fn handle_connection(socket: &mut TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone()?)?;

    let mut rng = StdRng::from_seed([123; 32]);

    // put program at a fixed pubkey to make anchor happy
    let prog = Keypair::generate(&mut rng);

    // load programs
    builder.add_program("zerocoin.so", Some(prog.pubkey()));

    // make user
    let user = Keypair::new();
    let (vault, _) = Pubkey::find_program_address(&[b"vault"], &prog.pubkey());
    let (mint, _) = Pubkey::find_program_address(&[b"mint"], &prog.pubkey());
    let (user_token, _) =
        Pubkey::find_program_address(&[b"token", user.pubkey().as_ref()], &prog.pubkey());

    writeln!(socket, "program: {}", prog.pubkey())?;
    writeln!(socket, "user: {}", user.pubkey())?;
    writeln!(socket, "user_token: {}", user_token)?;
    writeln!(socket, "vault: {}", vault)?;
    writeln!(socket, "mint: {}", mint)?;
    writeln!(socket, "token_program: {}", spl_token::ID)?;
    writeln!(socket, "system_program: {}", system_program::ID)?;

    let solve = builder.input_program()?;
    writeln!(socket, "solve: {}", solve)?;
    if [
        prog.pubkey(),
        user.pubkey(),
        user_token,
        vault,
        mint,
        system_program::ID,
        spl_token::ID,
    ]
    .into_iter()
    .any(|x| x == solve)
    {
        writeln!(socket, "cannot overlap solve with existing account")?;
        return Ok(());
    }

    if !solve.is_on_curve() {
        writeln!(socket, "solve pubkey must be on curve")?;
        return Ok(());
    }

    let mut challenge = builder.build().await;

    let payer_keypair = challenge.ctx.payer.insecure_clone();
    let payer = challenge.ctx.payer.pubkey();

    const STARTING_BAL: u64 = 1_000_000;
    const VAULT_BAL: u64 = 1_000_000_000;

    challenge
        .run_ix(Instruction::new_with_bytes(
            prog.pubkey(),
            &zerocoin::instruction::Initialize { bal: VAULT_BAL }.data(),
            zerocoin::accounts::Initialize {
                mint,
                payer,
                vault,
                token_program: spl_token::ID,
                system_program: system_program::ID,
            }
            .to_account_metas(None),
        ))
        .await?;

    challenge
        .run_ixs_full(
            &[system_instruction::create_account(
                &payer,
                &user.pubkey(),
                STARTING_BAL,
                0,
                &system_program::ID,
            )],
            &[&payer_keypair, &user],
            &payer,
        )
        .await?;

    let ix = challenge.read_instruction(solve)?;
    challenge
        .run_ixs_full(&[ix], &[&user], &user.pubkey())
        .await?;

    let balance = challenge
        .ctx
        .banks_client
        .get_account(user.pubkey())
        .await?
        .map(|acct| acct.lamports);
    writeln!(
        socket,
        "Ending balance: {}",
        balance
            .map(|x| x.to_string())
            .unwrap_or_else(|| "invalid user account".to_owned())
    )?;
    let token_amt = challenge
        .ctx
        .banks_client
        .get_account(user_token)
        .await?
        .and_then(|acct| spl_token::state::Account::unpack(&acct.data).ok())
        .map(|acct| acct.amount);
    writeln!(
        socket,
        "Ending zerocoin: {}",
        token_amt
            .map(|x| x.to_string())
            .unwrap_or_else(|| "invalid token account".to_owned())
    )?;
    if token_amt.unwrap_or(0) > 0 {
        let flag = fs::read_to_string("flag.txt")?;
        writeln!(
            socket,
            "Wow! You're clearly an entrepreneur just like me! Have a flag: {}",
            flag.trim()
        )?;
    } else {
        writeln!(
            socket,
            "I don't talk to broke peasants like you. Get some zerocoin and I'll give you a flag."
        )?;
    }

    Ok(())
}
