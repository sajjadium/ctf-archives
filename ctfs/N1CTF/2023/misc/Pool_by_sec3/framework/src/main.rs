use borsh::BorshSerialize;
use std::env;
use std::io::Write;

use sol_ctf_framework::ChallengeBuilder;

use solana_sdk::compute_budget::ComputeBudgetInstruction;

use solana_program::instruction::{AccountMeta, Instruction};
use solana_program::system_instruction;
use solana_program::sysvar;
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

    let chall_id = builder.add_program("./chall/target/deploy/chall.so", Some(chall::id()));
    let solve_id = builder.input_program()?;

    let mut chall = builder.build().await;

    // -------------------------------------------------------------------------
    // [setup env] initialize
    // -------------------------------------------------------------------------
    let program_id = chall_id;

    println!("Program ID: {}\n", program_id);

    // admin has infinite money wauw
    let admin_keypair = chall.ctx.payer.insecure_clone();
    let admin = admin_keypair.pubkey();

    let mint_keypair = Keypair::new();
    let mint = mint_keypair.pubkey();

    let (pool, _pool_bump) = Pubkey::find_program_address(&[chall::state::Pool::SEED_PREFIX.as_bytes()], &program_id);

    // create pool
    let ix = chall::processor::PoolInstruction::InitPool(100); // 1% withdrawal fee

    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool, false),
                    AccountMeta::new(mint, true),
                    AccountMeta::new_readonly(sysvar::rent::id(), false),
                    AccountMeta::new(admin, true),
                    AccountMeta::new_readonly(spl_token::id(), false),
                    AccountMeta::new_readonly(solana_program::system_program::id(), false),
                ]
            )],
            &[&mint_keypair, &admin_keypair],
            &admin,
        ).await?;
    
    // -------------------------------------------------------------------------

    // admin deposit with 1 SOL
    let ix = chall::processor::PoolInstruction::Deposit(1_000_000_000, b"init".to_vec());

    let (deposit_record_account_pda, _) = Pubkey::find_program_address(&[chall::state::DepositRecord::SEED_PREFIX.as_bytes(), pool.as_ref(), admin.as_ref(), b"init".to_vec().as_ref()], &program_id);
    let admin_token_account = spl_associated_token_account::get_associated_token_address(&admin, &mint);

    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool, false),
                    AccountMeta::new(deposit_record_account_pda, false),
                    AccountMeta::new(admin, true),
                    AccountMeta::new(admin_token_account, false),
                    AccountMeta::new(mint, false),
                    AccountMeta::new_readonly(spl_token::id(), false),
                    AccountMeta::new_readonly(spl_associated_token_account::id(), false),
                    AccountMeta::new_readonly(solana_program::system_program::id(), false),
                ]
            )],
            &[&admin_keypair],
            &admin,
        ).await?;

    // -------------------------------------------------------------------------

    // Simulate some rewards (0.1 sol)
    chall
        .run_ix(system_instruction::transfer(
            &admin,
            &pool,
            100_000_000,
        ))
        .await?;

    // -------------------------------------------------------------------------

    // Admin withdraw 0.2 SOL
    let ix = chall::processor::PoolInstruction::Withdraw(200_000_000, b"init".to_vec());

    chall
        .run_ixs_full(
            &[Instruction::new_with_bytes(
                program_id,
                &ix.try_to_vec().unwrap(),
                vec![
                    AccountMeta::new(pool, false),
                    AccountMeta::new(deposit_record_account_pda, false),
                    AccountMeta::new(admin, true),
                    AccountMeta::new(admin_token_account, false),
                    AccountMeta::new(mint, false),
                    AccountMeta::new_readonly(spl_token::id(), false),
                    AccountMeta::new_readonly(spl_associated_token_account::id(), false),
                    AccountMeta::new_readonly(solana_program::system_program::id(), false),
                ]
            )],
            &[&admin_keypair],
            &admin,
        ).await?;

    let user_keypair = Keypair::new();
    let user = user_keypair.pubkey();

    let user_token_account = spl_associated_token_account::get_associated_token_address(&user, &mint);

    // you have 1 SOL
    chall
        .run_ix(system_instruction::transfer(&admin, &user, 1_000_000_000))
        .await?;

        
    // -------------------------------------------------------------------------

    // provided info
    writeln!(socket, "admin: {}", admin)?;
    writeln!(socket, "user: {}", user)?;
    writeln!(socket, "user_token_account: {}", user_token_account)?;
    writeln!(socket, "pool: {}", pool)?;
    writeln!(socket, "mint: {}", mint)?;

    // -------------------------------------------------------------------------

    let pool_balance_before = chall.ctx.banks_client.get_balance(pool).await? as i128;
    let user_balance_before = chall.ctx.banks_client.get_balance(user).await? as i128;

    // run the exploit 3 times
    let solve_ix = chall.read_instruction(solve_id)?;
    
    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_000);
    chall
        .run_ixs_full(&[bump_budget, solve_ix.clone()], &[&user_keypair], &user)
        .await?;

    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_001);
    chall
        .run_ixs_full(&[bump_budget, solve_ix.clone()], &[&user_keypair], &user)
        .await?;

    let bump_budget = ComputeBudgetInstruction::set_compute_unit_limit(10_000_002);
    chall
        .run_ixs_full(&[bump_budget, solve_ix.clone()], &[&user_keypair], &user)
        .await?;

    // -------------------------------------------------------------------------

    // check wining condition
    let pool_balance = chall.ctx.banks_client.get_balance(pool).await? as i128;
    let user_balance = chall.ctx.banks_client.get_balance(user).await? as i128;

    
    println!("pool balance before : {}", pool_balance_before);
    println!("user balance before : {}", user_balance_before);
    println!("pool balance        : {}", pool_balance);
    println!("user balance        : {}", user_balance);

    // if 80% of the pool is drained by you, you win
    let target = pool_balance_before * 8 / 10;
    if (pool_balance_before - pool_balance) > target && user_balance > user_balance_before + target {
        writeln!(socket, "Congrats!")?;
        if let Ok(flag) = env::var("FLAG") {
            writeln!(socket, "flag: {:?}", flag)?;
        } else {
            writeln!(socket, "flag not found, please contact admin")?;
        }
    } else {
        writeln!(socket, "...?")?;
    }

    Ok(())
}