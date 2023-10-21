use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    program_pack::Pack,
    msg,
    pubkey::Pubkey,
    rent::Rent,
    sysvar::Sysvar,
    system_instruction,
};
use spl_associated_token_account::instruction as associated_token_account_instruction;
use spl_token::{instruction as token_instruction, state::Mint};

use crate::state::Pool;
use crate::state::DepositRecord;

pub fn deposit(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64, account_name: Vec<u8>) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let pool_account = next_account_info(accounts_iter)?;
    let deposit_record_account = next_account_info(accounts_iter)?;
    let user = next_account_info(accounts_iter)?;
    let user_token_account = next_account_info(accounts_iter)?;
    let lp_token_mint = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;
    let associated_token_program = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    // Signer check
    assert!(user.is_signer);

    // Program checks
    assert_eq!(token_program.key, &spl_token::id());
    assert_eq!(system_program.key, &solana_program::system_program::id());
    assert_eq!(associated_token_program.key, &spl_associated_token_account::id());
    assert_eq!(lp_token_mint.key, &Pool::try_from_slice(&pool_account.data.borrow())?.lp_token_mint);

    // PDA checks
    let (deposit_record, deposit_record_bump) =
        Pubkey::find_program_address(&[DepositRecord::SEED_PREFIX.as_bytes(), pool_account.key.as_ref(), user.key.as_ref(), account_name.as_ref()], program_id);
    assert_eq!(deposit_record_account.key, &deposit_record);

    let (pool_pda, pool_bump) =
        Pubkey::find_program_address(&[Pool::SEED_PREFIX.as_bytes()], program_id);
    assert_eq!(pool_account.key, &pool_pda);
    
    if deposit_record_account.data_is_empty() {
        // First time deposit
        assert_eq!(deposit_record_account.owner, system_program.key);
        msg!("Creating deposit record account...");
        msg!("Deposit record: {}", deposit_record_account.key);

        // Allocate the deposit record account
        invoke_signed(
            &system_instruction::allocate(
                deposit_record_account.key, 
                std::mem::size_of::<DepositRecord>() as u64,
            ),
            &[deposit_record_account.clone(), system_program.clone()],
            &[&[DepositRecord::SEED_PREFIX.as_bytes(), pool_account.key.as_ref(), user.key.as_ref(), account_name.as_ref(), &[deposit_record_bump]]],
        )?;

        // Assign the deposit record account to the program
        invoke_signed(
            &system_instruction::assign(
                deposit_record_account.key, 
                program_id
            ),
            &[deposit_record_account.clone(), system_program.clone()],
            &[&[DepositRecord::SEED_PREFIX.as_bytes(), pool_account.key.as_ref(), user.key.as_ref(), account_name.as_ref(), &[deposit_record_bump]]],
        )?;

        // Create associated token account if it doesn't exist
        if user_token_account.lamports() == 0 {
            msg!("Creating associated token account...");
            msg!("associated_token_program {}", associated_token_program.key);
            invoke(
                &associated_token_account_instruction::create_associated_token_account(
                    user.key,
                    user.key,
                    lp_token_mint.key,
                    token_program.key,
                ),
                &[
                    lp_token_mint.clone(),
                    user_token_account.clone(),
                    user.clone(),
                    system_program.clone(),
                    token_program.clone(),
                    associated_token_program.clone(),
                ],
            )?;
        } else {
            assert_eq!(user_token_account.owner, token_program.key);
        }
    
        // Calculate the amount of LP tokens to mint
        let total_supply = Mint::unpack(&lp_token_mint.data.borrow())?.supply;
        let lp_token_amount = if total_supply == 0 {
            amount
        } else {
            (amount as u128)
                .checked_mul(total_supply as u128)
                .and_then(|mul_result| mul_result.checked_div(**pool_account.lamports.borrow() as u128))
                .unwrap() as u64
        };

        // Deposit
        invoke(
            &system_instruction::transfer(
                user.key,
                pool_account.key,
                amount,
            ),
            &[
                user.clone(),
                pool_account.clone(),
                system_program.clone(),
            ],
        )?;
    
        let deposit_record_data = DepositRecord {
            amount,
            lp_token_amount,
            pool: *pool_account.key,
            user: *user.key,
        };
        deposit_record_data.serialize(&mut *deposit_record_account.data.borrow_mut())?;
        // Mint LP tokens
        if lp_token_amount > 0 {
            msg!("Minting {} LP tokens...", lp_token_amount);
            invoke_signed(
                &token_instruction::mint_to(
                    token_program.key,
                    lp_token_mint.key,
                    user_token_account.key,
                    pool_account.key,
                    &[pool_account.key],
                    lp_token_amount,
                )?,
                &[
                    lp_token_mint.clone(),
                    pool_account.clone(),
                    user_token_account.clone(),
                    token_program.clone(),
                ],
                &[&[Pool::SEED_PREFIX.as_bytes(), &[pool_bump]]],
            )?;
        }

        // Fund the deposit record account
        let lamports_required_for_deposit_record = (Rent::get()?).minimum_balance(DepositRecord::LEN);
        **pool_account.lamports.borrow_mut() -= lamports_required_for_deposit_record;
        **deposit_record_account.lamports.borrow_mut() += lamports_required_for_deposit_record;

    } else {
        let mut deposit_record_data = DepositRecord::try_from_slice(&deposit_record_account.data.borrow())?;
        assert_eq!(deposit_record_data.pool, *pool_account.key);
        assert_eq!(deposit_record_data.user, *user.key);

        // Create associated token account if it doesn't exist
        if user_token_account.lamports() == 0 {
            msg!("Creating associated token account...");
            msg!("associated_token_program {}", associated_token_program.key);
            invoke(
                &associated_token_account_instruction::create_associated_token_account(
                    user.key,
                    user.key,
                    lp_token_mint.key,
                    token_program.key,
                ),
                &[
                    lp_token_mint.clone(),
                    user_token_account.clone(),
                    user.clone(),
                    system_program.clone(),
                    token_program.clone(),
                    associated_token_program.clone(),
                ],
            )?;
        } else {
            assert_eq!(user_token_account.owner, token_program.key);
        }
    
        // Calculate the amount of LP tokens to mint
        let total_supply = Mint::unpack(&lp_token_mint.data.borrow())?.supply;
        let lp_token_amount = if total_supply == 0 {
            amount
        } else {
            (amount as u128)
                .checked_mul(total_supply as u128)
                .and_then(|mul_result| mul_result.checked_div(**pool_account.lamports.borrow() as u128))
                .unwrap() as u64
        };
        
        // Deposit
        invoke(
            &system_instruction::transfer(
                user.key,
                pool_account.key,
                amount,
            ),
            &[
                user.clone(),
                pool_account.clone(),
                system_program.clone(),
            ],
        )?;

        deposit_record_data.amount += amount;
    
        deposit_record_data.lp_token_amount += lp_token_amount;
        deposit_record_data.serialize(&mut *deposit_record_account.data.borrow_mut())?;
        // Mint LP tokens
        if lp_token_amount > 0 {
            msg!("Minting {} LP tokens...", lp_token_amount);
            invoke_signed(
                &token_instruction::mint_to(
                    token_program.key,
                    lp_token_mint.key,
                    user_token_account.key,
                    pool_account.key,
                    &[pool_account.key],
                    lp_token_amount,
                )?,
                &[
                    lp_token_mint.clone(),
                    pool_account.clone(),
                    user_token_account.clone(),
                    token_program.clone(),
                ],
                &[&[Pool::SEED_PREFIX.as_bytes(), &[pool_bump]]],
            )?;
        }
    }

    Ok(())
}

pub fn withdraw(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64, account_name: Vec<u8>) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let pool_account = next_account_info(accounts_iter)?;
    let deposit_record_account = next_account_info(accounts_iter)?;
    let user = next_account_info(accounts_iter)?;
    let user_token_account = next_account_info(accounts_iter)?;
    let lp_token_mint = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;
    let associated_token_program = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    // Signer check
    assert!(user.is_signer);

    // Program checks
    assert_eq!(token_program.key, &spl_token::id());
    assert_eq!(system_program.key, &solana_program::system_program::id());
    assert_eq!(associated_token_program.key, &spl_associated_token_account::id());
    assert_eq!(lp_token_mint.key, &Pool::try_from_slice(&pool_account.data.borrow())?.lp_token_mint);

    // PDA checks
    let (deposit_record, _deposit_record_bump) =
        Pubkey::find_program_address(&[DepositRecord::SEED_PREFIX.as_bytes(), pool_account.key.as_ref(), user.key.as_ref(), account_name.as_ref()], program_id);
    assert_eq!(deposit_record_account.key, &deposit_record);

    let (pool_pda, _pool_bump) =
        Pubkey::find_program_address(&[Pool::SEED_PREFIX.as_bytes()], program_id);
    assert_eq!(pool_account.key, &pool_pda);
    
    // Calculate the amount of SOL to withdraw
    let total_supply = Mint::unpack(&lp_token_mint.data.borrow())?.supply;
    let mut lamport_amount = (amount as u128)
        .checked_mul(**pool_account.lamports.borrow() as u128)
        .and_then(|mul_result| mul_result.checked_div(total_supply as u128))
        .unwrap() as u64;
    let pool_data = Pool::try_from_slice(&pool_account.data.borrow())?;
    lamport_amount = lamport_amount.saturating_sub(lamport_amount * pool_data.withdrawal_fee / 10000);
    msg!("Withdrawing {} lamports...", lamport_amount);

    // Burn LP tokens
    if amount > 0 {
        msg!("Burning {} LP tokens...", amount);
        invoke(
            &token_instruction::burn(
                token_program.key,
                user_token_account.key,
                lp_token_mint.key,
                user.key,
                &[],
                amount,
            )?,
            &[
                user_token_account.clone(),
                lp_token_mint.clone(),
                user.clone(),
            ],
        )?;
    }

    // Withdraw
    **pool_account.lamports.borrow_mut() -= lamport_amount;
    **user.lamports.borrow_mut() += lamport_amount;

    let mut deposit_record_data = DepositRecord::try_from_slice(&deposit_record_account.data.borrow())?;

    // Calculate PnL
    let origin = amount / deposit_record_data.lp_token_amount * deposit_record_data.amount;
    if lamport_amount > origin  {
        // Profit
        let profit = lamport_amount - origin;
        msg!("User {} profited {} lamports", user.key, profit);
    } else {
        // Loss
        let loss = origin - lamport_amount;
        msg!("User {} lost {} lamports", user.key, loss);
    }

    // Update deposit record
    assert_eq!(deposit_record_data.pool, *pool_account.key);
    assert_eq!(deposit_record_data.user, *user.key);
    deposit_record_data.amount = deposit_record_data.amount.saturating_sub(lamport_amount);
    deposit_record_data.lp_token_amount = deposit_record_data.lp_token_amount.saturating_sub(amount);
    
    if deposit_record_data.lp_token_amount == 0 {
        // close deposit record account
        **pool_account.lamports.borrow_mut() += deposit_record_account.lamports();
        **deposit_record_account.lamports.borrow_mut() = 0;
        deposit_record_account.realloc(0, true)?;
        deposit_record_account.assign(system_program.key);
    }
    else {
        deposit_record_data.serialize(&mut *deposit_record_account.data.borrow_mut())?;
    }
    
    Ok(())
}