use anchor_lang::InstructionData;
use anchor_lang::ToAccountMetas;
use chall;
use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_sdk::compute_budget::ComputeBudgetInstruction;

use solana_program::instruction::Instruction;
use solana_program::system_instruction;
use solana_program_test::tokio;
use solana_sdk::pubkey::Pubkey;
use solana_sdk::pubkey;
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

    let valid_pubkey = pubkey!("N1CTF11111111111111111111111111111111111111");
    if solve_id != valid_pubkey {
        writeln!(socket, "bad pubkey, got: {} expected: {}", solve_id, valid_pubkey)?;
        return Ok(());
    }

    // Initialize the challenge
    writeln!(socket, "Initializing the challenge")?;

    let mut chall = builder.build().await;

    let token_mint = chall.add_mint().await?;

    let admin_keypair = &chall.ctx.payer;
    let admin = admin_keypair.pubkey().clone();
    let admin_token = chall.add_associated_token_account(&token_mint, &admin).await?;

    let vault = Pubkey::find_program_address(&[b"vault"], &chall_id).0;
    let vault_token = Pubkey::find_program_address(&[b"token", vault.as_ref()], &chall_id).0;
    
    let ix = chall::instruction::Initialize {};
    let ix_accounts = chall::accounts::Initialize {
        vault,
        vault_token,
        mint: token_mint,
        payer: admin,
        system_program: solana_program::system_program::ID,
        token_program: spl_token::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall.run_ix(Instruction::new_with_bytes(
        chall_id,
        &ix.data(),
        ix_accounts.to_account_metas(None),
    )).await?;

    chall.mint_to(100_000_000_000_000, &token_mint, &vault_token).await?;

    let ix = chall::instruction::Deposit { amount: 100_000_000_000 };
    let ix_accounts = chall::accounts::Deposit {
        vault,
        vault_token,
        user: admin,
        user_token: admin_token,
        mint: token_mint,
        system_program: solana_program::system_program::ID,
        token_program: spl_token::ID,     
    };
    chall.run_ix(Instruction::new_with_bytes(
        chall_id,
        &ix.data(),
        ix_accounts.to_account_metas(None),
    )).await?;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();
    let user_token = chall.add_associated_token_account(&token_mint, &user).await?;

    writeln!(socket, "Accounts:")?;
    writeln!(socket, "program: {}", chall_id)?;
    writeln!(socket, "mint: {}", token_mint)?;
    writeln!(socket, "vault: {}", vault)?;
    writeln!(socket, "vault_token: {}", vault_token)?;
    writeln!(socket, "user: {}", user)?;
    writeln!(socket, "user_token: {}", user_token)?;

    // Fund the user account
    chall.run_ix(system_instruction::transfer(&admin, &user, 100_000_000)).await?;

    // Run the user transaction
    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_000u32);
    let solve_ix = chall.read_instruction(solve_id)?;

    chall
        .run_ixs_full(
            &[bump_budget, solve_ix],
            &[&user_keypair],
            &user_keypair.pubkey(),
        )
        .await?;

    // Check win condition
    let user_lamports = chall.ctx.banks_client.get_balance(user).await?;
    if user_lamports > 50_000_000_000 {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    } else {
        writeln!(socket, "keep trying")?;
    }

    Ok(())
}