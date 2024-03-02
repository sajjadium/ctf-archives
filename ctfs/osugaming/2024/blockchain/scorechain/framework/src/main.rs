use chall::Play;
use chall::anchor_lang::InstructionData;
use chall::anchor_lang::ToAccountMetas;

use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_sdk::compute_budget::ComputeBudgetInstruction;

use solana_program::instruction::Instruction;
use solana_program::system_instruction;
use solana_program_test::tokio;
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
            if let Err(err) = handle_connection(stream).await {
                println!("error: {:?}", err);
            }
        });
    }
    Ok(())
}

async fn handle_connection(mut socket: TcpStream) -> Result<(), Box<dyn Error>> {
    let mut builder = ChallengeBuilder::try_from(socket.try_clone().unwrap()).unwrap();

    let chall_id = builder.add_program("./chall/target/deploy/chall.so", Some(chall::ID));
    let solve_id = builder.input_program()?;

    let mut chall = builder.build().await;

    // -------------------------------------------------------------------------
    // [setup env] initialize
    // -------------------------------------------------------------------------
    let program_id = chall_id;

    // admin has infinite money wauw
    let admin_keypair = chall.ctx.payer.insecure_clone();
    let admin = admin_keypair.pubkey();

    let (db, _) = Pubkey::find_program_address(&[ b"wysi" ], &program_id);

    let player_keypair = Keypair::new();
    let player = player_keypair.pubkey();

    let cookiezi_keypair = Keypair::new();
    let cookiezi = cookiezi_keypair.pubkey();

    chall
        .run_ix(system_instruction::transfer(
            &admin,
            &cookiezi,
            500_000_000_000_000,
        ))
        .await?;

    // ur poor :^c
    chall
        .run_ix(system_instruction::transfer(&admin, &player, 100_000_000))
        .await?;

    println!("\nNon-PDA Accounts created...\n");

    let ix = chall::instruction::InitDb {};
    let ix_accounts = chall::accounts::InitDb {
        db,
        user: admin,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.data(),
                ix_accounts.to_account_metas(None)
            )],
            &[&admin_keypair],
            &admin,
        ).await?;

    let ix = chall::instruction::SubmitPlay {
        play: Play {
            map: String::from("blue zenith"),
            player: String::from("chocomint"),
            pp: 727,
            bounty: 1_000_000_000_000,
        },
    };
    let ix_accounts = chall::accounts::SubmitPlay {
        db,
        player: cookiezi,
        system_program: solana_program::system_program::ID,
    };
    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.data(),
                ix_accounts.to_account_metas(None)
            )],
            &[&cookiezi_keypair],
            &cookiezi,
        ).await?;

    writeln!(socket, "player: {}", player)?;
    writeln!(socket, "db: {}", db)?;

    // snipe shige :^)
    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_000);
    let solve_ix = chall.read_instruction(solve_id)?;
    chall
        .run_ixs_full(&[bump_budget, solve_ix], &[&player_keypair], &player)
        .await.ok();

    let player_account = chall.ctx.banks_client.get_account(player).await?.unwrap();

    if player_account.lamports > 500_000_000_000 {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    } else {
        writeln!(socket, "shige lives to see another day")?;
    }

    Ok(())
}
