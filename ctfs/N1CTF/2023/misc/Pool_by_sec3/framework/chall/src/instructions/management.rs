use borsh::BorshSerialize;
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    program_pack::Pack,
    msg,
    pubkey::Pubkey,
    rent::Rent,
    system_instruction,
    sysvar::Sysvar,
};
use spl_token::{instruction as token_instruction, state::Mint};

use crate::state::Pool;

pub fn init_pool(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    withdrawal_fee: u64,
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let pool_account = next_account_info(accounts_iter)?;
    let mint_account = next_account_info(accounts_iter)?;
    let rent = next_account_info(accounts_iter)?;
    let payer = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;
    
    assert!(payer.is_signer);
    assert!(pool_account.data_is_empty());

    let (pool_pda, pool_bump) = 
        Pubkey::find_program_address(&[Pool::SEED_PREFIX.as_bytes()], program_id);
    assert_eq!(pool_account.key, &pool_pda);

    // First create the account for the Mint
    //
    msg!("Creating mint account...");
    msg!("Mint: {}", mint_account.key);
    invoke(
        &system_instruction::create_account(
            payer.key,
            mint_account.key,
            (Rent::get()?).minimum_balance(Mint::LEN),
            Mint::LEN as u64,
            token_program.key,
        ),
        &[
            mint_account.clone(),
            payer.clone(),
            system_program.clone(),
            token_program.clone(),
        ],
    )?;

    // Now initialize that account as a Mint
    //
    msg!("Initializing mint account...");
    msg!("Mint: {}", mint_account.key);
    invoke(
        &token_instruction::initialize_mint(
            token_program.key,
            mint_account.key,
            pool_account.key,
            Some(pool_account.key),
            0,
        )?,
        &[
            mint_account.clone(),
            pool_account.clone(),
            token_program.clone(),
            rent.clone(),
        ],
    )?;

    // Now create the account for the Pool
    //
    msg!("Creating pool account...");
    msg!("Pool: {}", pool_account.key);
    invoke_signed(
        &system_instruction::create_account(
            payer.key,
            pool_account.key,
            (Rent::get()?).minimum_balance(std::mem::size_of::<Pool>()),
            std::mem::size_of::<Pool>() as u64,
            program_id,
        ),
        &[
            payer.clone(),
            pool_account.clone(),
            system_program.clone(),
        ],
        &[&[Pool::SEED_PREFIX.as_bytes(), &[pool_bump]]],
    )?;

    let pool_data = Pool {
        withdrawal_fee,
        lp_token_mint: *mint_account.key,
    };
    pool_data.serialize(&mut *pool_account.data.borrow_mut())?;

    Ok(())
}