use chall::anchor_lang::InstructionData;
use chall::anchor_lang::ToAccountMetas;
use chall::FLAG_SEED;
use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_sdk::compute_budget::ComputeBudgetInstruction;

use solana_program::instruction::Instruction;
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
    let listener = TcpListener::bind("0.0.0.0:8080")?;

    println!("starting server at port 8080!");

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

    let valid_pubkey = pubkey!("osecio1111111111111111111111111111111111111");

    if solve_id != valid_pubkey {
        writeln!(
            socket,
            "bad pubkey, got: {} expected: {}",
            solve_id, valid_pubkey
        )?;
        return Ok(());
    }

    let mut chall = builder.build().await;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();

    chall
        .run_ix(system_instruction::transfer(&payer, &user, 100_000_000_000))
        .await?;

    {
        let ix = chall::instruction::Init {};
        let state = Pubkey::find_program_address(&[FLAG_SEED], &chall_id).0;
        let ix_accounts = chall::accounts::Init {
            state,
            payer,
            system_program: solana_program::system_program::ID,
            rent: solana_program::sysvar::rent::ID,
        };
        chall
            .run_ix(Instruction::new_with_bytes(
                chall_id,
                &ix.data(),
                ix_accounts.to_account_metas(None),
            ))
            .await?;
    }

    {
        let ix = chall::instruction::InitVirtualBalance {
            x: 1_000_000,
            y: 1_000_001,
        };
        let state = Pubkey::find_program_address(&[FLAG_SEED], &chall_id).0;
        let ix_accounts = chall::accounts::Auth {
            state,
            payer,
            system_program: solana_program::system_program::ID,
            rent: solana_program::sysvar::rent::ID,
        };
        chall
            .run_ix(Instruction::new_with_bytes(
                chall_id,
                &ix.data(),
                ix_accounts.to_account_metas(None),
            ))
            .await?;
    }

    {
        let ix = chall::instruction::SetEnabled { enabled: true };
        let state = Pubkey::find_program_address(&[FLAG_SEED], &chall_id).0;
        let ix_accounts = chall::accounts::Auth {
            state,
            payer,
            system_program: solana_program::system_program::ID,
            rent: solana_program::sysvar::rent::ID,
        };
        chall
            .run_ix(Instruction::new_with_bytes(
                chall_id,
                &ix.data(),
                ix_accounts.to_account_metas(None),
            ))
            .await?;
    }

    writeln!(socket, "user: {}", user)?;

    let solve_ix = chall.read_instruction(solve_id)?;
    println!("{:?}", solve_ix);

    println!("start");
    chall
        .run_ixs_full(&[solve_ix], &[&user_keypair], &user_keypair.pubkey())
        .await?;
    println!("end");

    let flag = Pubkey::find_program_address(&[FLAG_SEED], &chall_id).0;

    if let Some(acct) = chall.ctx.banks_client.get_account(flag).await? {
        let state = bytemuck::from_bytes::<chall::State>(
            &acct.data[8..std::mem::size_of::<chall::State>() + 8],
        );
        if state.x == 0 && state.y == 0 {
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
