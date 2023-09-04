use solana_sdk::{
    signature::{Keypair, Signer},
    pubkey::Pubkey,
    instruction::{Instruction, AccountMeta},
};
use solana_program_test::tokio;
use solana_program::{system_program, system_instruction};
use sol_ctf_framework::ChallengeBuilder;
use rand::{
    rngs::StdRng,
    SeedableRng,
    Rng,
    distributions::{Alphanumeric, DistString},
};
use borsh::ser::BorshSerialize;

use std::{
    fs,
    io::Write,
    error::Error,
    str::FromStr,
    net::{TcpListener, TcpStream},
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080")?;
    println!("Listening on port 8080 ...");
    for stream in listener.incoming() {
        let stream = stream.unwrap();

        tokio::spawn(async move {
            if let Err(err) = handle_connection(stream).await {
                println!("error: {:?}", err);
            }
        });
    }
    Ok(())
}

async fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    // load programs
    let pub_str = "ArciEpQvGwZk5yegHEiy27afRZaDLKU8B3kj5MWc38rq";
    let program_id = builder.add_program("Arcade.so", Some(Pubkey::from_str(&pub_str)?));
    let solve_id = builder.input_program().unwrap();

    let mut chall = builder.build().await;
    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();

    // create user
    let user = Keypair::new();

    // fund user
    chall.run_ix(system_instruction::transfer(
        &payer,
        &user.pubkey(),
        1_000_000_000,  // 1 SOL
    )).await?;

    // create data account
    let data_account = Keypair::new();

    let mut constructor_data = vec![0x87, 0x2c, 0xcd, 0xc6, 0x19, 0x01, 0x48, 0xbc];    // discriminator

    let mut rng = StdRng::from_entropy();
    constructor_data.extend_from_slice(&rng.gen::<u64>().to_be_bytes());
    constructor_data.extend_from_slice(&rng.gen::<u64>().to_be_bytes());
    constructor_data.extend_from_slice(&rng.gen::<u64>().to_be_bytes());

    let random_address = Keypair::new().pubkey();
    constructor_data.extend_from_slice(&random_address.to_bytes());

    let random_string = Alphanumeric.sample_string(&mut rng, 8);
    constructor_data.extend_from_slice(&BorshSerialize::try_to_vec(&random_string)?);

    // initialize
    chall.run_ixs_full(
        &[Instruction::new_with_bytes(
            program_id,
            &constructor_data,
            vec![
                AccountMeta::new(data_account.pubkey(), true),
                AccountMeta::new(user.pubkey(), true),
                AccountMeta::new_readonly(system_program::id(), false),
            ],
        )],
        &[&data_account, &user],
        &user.pubkey(),
    ).await?;

    // create data account for user program
    let user_data = Keypair::new();

    writeln!(socket, "program: {}", program_id)?;
    writeln!(socket, "data account: {}", data_account.pubkey())?;
    writeln!(socket, "user: {}", user.pubkey())?;
    writeln!(socket, "user data: {}", user_data.pubkey())?;
    
    // run solve
    let solve_ix = chall.read_instruction(solve_id)?;
    chall.run_ixs_full(
        &[solve_ix],
        &[&user_data, &user],
        &user.pubkey(),
    ).await?;

    // check solve
    let account_data = chall.ctx.banks_client.get_account(data_account.pubkey()).await?.unwrap().data;
    let play_count = u32::from_le_bytes(account_data[20..24].try_into().unwrap());
    if play_count > 0 {
        let flag = fs::read_to_string("flag.txt").unwrap();
        writeln!(socket, "Oops, new registered players can also play 1pc for free > <")?;
        writeln!(socket, "{}", flag)?;
    } else {
        writeln!(socket, "You haven't played yet :<")?;
    }

    Ok(())
}