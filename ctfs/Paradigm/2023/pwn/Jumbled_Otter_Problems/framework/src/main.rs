use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_program::system_instruction;
use solana_program_test::tokio;
use solana_sdk::pubkey;
use solana_sdk::pubkey::Pubkey;
use solana_sdk::signature::Signer;
use solana_sdk::signer::keypair::Keypair;
use std::error::Error;

use std::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:1337")?;

    println!("starting server at port 1337!");

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        tokio::spawn(async {
            println!("handling new user");
            if let Err(err) = handle_connection(stream).await {
                println!("error: {:?}", err);
            }
        });
    }
    Ok(())
}

async fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    assert!(builder.add_program("/home/user/framework/chall.so", Some(chall::ID)) == chall::ID);

    let mut chall = builder.build().await;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();

    chall
        .run_ix(system_instruction::transfer(&payer, &user, 100_000_000_000))
        .await?;

    writeln!(socket, "user: {}", user)?;

    let solve_ix = chall.read_instruction(chall::ID)?;

    chall
        .run_ixs_full(&[solve_ix], &[&user_keypair], &user)
        .await?;

    let flag = Pubkey::create_program_address(&["FLAG".as_ref()], &chall::ID)?;

    if let Some(acct) = chall.ctx.banks_client.get_account(flag).await? {
        if acct.data.len() == 0x1337
            && u64::from_le_bytes(acct.data[..8].try_into().unwrap()) == 0x4337
        {
            writeln!(socket, "congrats!")?;
            if let Ok(flag) = env::var("FLAG") {
                writeln!(socket, "flag: {:?}", flag)?;
            } else {
                writeln!(socket, "flag not found, please contact admin")?;
            }
        }
    }

    Ok(())
}
