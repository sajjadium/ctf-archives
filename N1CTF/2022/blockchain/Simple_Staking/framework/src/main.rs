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

    let mut chall = builder.build().await;

    // -------------------------------------------------------------------------
    // [setup env] initialize
    // -------------------------------------------------------------------------
    let program_id = chall_id;

    let mint = chall.add_mint().await?;

    let payer_keypair = &chall.ctx.payer;
    let payer = payer_keypair.pubkey();

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();
    chall
        .run_ix(system_instruction::transfer(&payer, &user, 100_000_000_000))
        .await?;

    let catalog = Pubkey::find_program_address(&[b"CATALOG"], &program_id).0;
    let reserve = Pubkey::find_program_address(&[b"RESERVE"], &program_id).0;

    println!("\nAccounts created...\n");

    let ix = chall::instruction::Initialize {};
    let ix_accounts = chall::accounts::Initialize {
        catalog,
        reserve,
        mint,
        payer,
        token_program: spl_token::ID,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };

    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    // -------------------------------------------------------------------------
    // [setup env] register
    // -------------------------------------------------------------------------
    let org_name = String::from("product");
    let employee_id = String::from("employ_A");
    let ix = chall::instruction::Register {
        org_name: org_name.clone(),
        employee_id: employee_id.clone(),
    };
    let employee_record = Pubkey::find_program_address(&[payer.as_ref()], &program_id).0;
    let reg_accounts = chall::accounts::Register {
        catalog,
        employee_record,
        user: payer,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            reg_accounts.to_account_metas(None),
        ))
        .await?;

    // -------------------------------------------------------------------------
    // [setup env] deposits 1_000
    // -------------------------------------------------------------------------
    let payer_token_account = chall.add_token_account(&mint, &payer).await?;
    chall
        .mint_to(1_000_u64, &mint, &payer_token_account)
        .await?;

    let vault = Pubkey::find_program_address(
        &[org_name.clone().as_bytes(), employee_id.clone().as_bytes()],
        &program_id,
    )
    .0;
    let ix = chall::instruction::Deposit {
        org_name: org_name.clone(),
        employee_id: employee_id.clone(),
        amount: 500_u64,
    };
    let ix_accounts = chall::accounts::Deposit {
        vault,
        employee_record,
        reserve,
        user_token_account: payer_token_account,
        mint,
        user: payer,
        token_program: spl_token::ID,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    chall
        .run_ix(Instruction::new_with_bytes(
            program_id,
            &ix.data(),
            ix_accounts.to_account_metas(None),
        ))
        .await?;

    // TDOD: comment out
    let reserve_account = chall.read_token_account(reserve).await?;
    let reserve_balance = reserve_account.amount;
    println!(
        "\nvault = {}\nreserve balance = {}\n",
        vault, reserve_balance
    );
    // ----------------------------------------------------------------------------
    // [setup env] done
    // ----------------------------------------------------------------------------
    
    
    let init_amount = 100_u64;
    let user_record = Pubkey::find_program_address(&[user.as_ref()], &program_id).0;
    let user_token_account_pubkey = chall.add_token_account(&mint, &user).await?;
    chall
        .mint_to(init_amount, &mint, &user_token_account_pubkey)
        .await?;

    writeln!(socket, "user: {}", user)?;
    writeln!(socket, "user_record: {}", user_record)?;
    writeln!(socket, "catalog: {}", catalog)?;
    writeln!(socket, "mint: {}", mint)?;
    writeln!(socket, "user_token_account: {}", user_token_account_pubkey)?;
    writeln!(socket, "reserve: {}", reserve)?;

    let bump_budget = ComputeBudgetInstruction::request_units(10_000_000u32, 0u32);
    let solve_ix = chall.read_instruction(solve_id)?;
    chall
        .run_ixs_full(
            &[bump_budget, solve_ix],
            &[&user_keypair],
            &user_keypair.pubkey(),
        )
        .await?;

    let user_token_account = chall.read_token_account(user_token_account_pubkey).await?;
    writeln!(
        socket,
        "player_account_amount: {:?}",
        user_token_account.amount
    )?;

    println!(
        "\nplayer_account_amount balance = {}\n",
        user_token_account.amount
    );

    if user_token_account.amount > init_amount {
        writeln!(socket, "congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    }

    Ok(())
}
