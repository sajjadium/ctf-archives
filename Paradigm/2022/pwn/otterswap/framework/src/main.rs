use chall::anchor_lang::InstructionData;
use chall::anchor_lang::ToAccountMetas;
use chall::{POOL_A_SEED, POOL_B_SEED, SWAP_SEED};
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

    let valid_pubkey = pubkey!("osecio1111111111111111111111111111111111111");

    if solve_id != valid_pubkey {
        writeln!(socket, "bad pubkey, got: {} expected: {}", solve_id, valid_pubkey)?;
        return Ok(());
    }

    let mut chall = builder.build().await;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    let mint_a = chall.add_mint().await?;
    let mint_b = chall.add_mint().await?;

    let program_id = chall_id;
    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();
    let swap = Pubkey::find_program_address(&[SWAP_SEED, payer.as_ref()], &program_id).0;
    let pool_a = Pubkey::find_program_address(&[POOL_A_SEED, swap.as_ref()], &program_id).0;
    let pool_b = Pubkey::find_program_address(&[POOL_B_SEED, swap.as_ref()], &program_id).0;

    let ix = chall::instruction::Initialize {};
    let ix_accounts = chall::accounts::Initialize {
        swap,
        pool_a,
        pool_b,
        mint_a,
        mint_b,
        payer,
        system_program: solana_program::system_program::ID,
        token_program: spl_token::ID,
        rent: solana_program::sysvar::rent::ID,
    };

    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    chall
        .run_ix(system_instruction::transfer(&payer, &user, 100_000_000_000))
        .await?;

    let user_in_account = chall.add_token_account(&mint_a, &user).await?;
    let user_out_account = chall.add_token_account(&mint_b, &user).await?;

    let AMT = 10;

    chall.mint_to(AMT, &mint_a, &pool_a).await?;
    chall.mint_to(AMT, &mint_b, &pool_b).await?;

    chall.mint_to(AMT, &mint_a, &user_in_account).await?;

    writeln!(socket, "payer: {}", chall.ctx.payer.pubkey())?;
    writeln!(socket, "user: {}", user)?;
    writeln!(socket, "mint_a: {}", mint_a)?;
    writeln!(socket, "mint_b: {}", mint_b)?;
    writeln!(socket, "user_in_account: {}", user_in_account)?;
    writeln!(socket, "user_out_account: {}", user_out_account)?;

    let bump_budget = ComputeBudgetInstruction::request_units(10_000_000u32, 0u32);
    let solve_ix = chall.read_instruction(solve_id)?;

    chall
        .run_ixs_full(
            &[bump_budget, solve_ix],
            &[&user_keypair],
            &user_keypair.pubkey(),
        )
        .await?;

    let in_token_account = chall.read_token_account(user_in_account).await?;
    let out_token_account = chall.read_token_account(user_out_account).await?;

    let amt_a = in_token_account.amount;
    let amt_b = out_token_account.amount;

    writeln!(socket, "funds 1: {:?}", amt_a)?;
    writeln!(socket, "funds 2: {:?}", amt_b)?;

    if amt_a + amt_b == 3 * AMT - 1 {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    }

    Ok(())
}
