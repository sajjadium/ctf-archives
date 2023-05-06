use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    msg,
    program::{invoke, invoke_signed},
    pubkey::Pubkey,
    system_instruction,
};

use crate::{Escrow, ServiceInstruction, ESCROW_ACCOUNT_SIZE};

pub fn process_instruction(
    program: &Pubkey,
    accounts: &[AccountInfo],
    mut data: &[u8],
) -> ProgramResult {
    match ServiceInstruction::deserialize(&mut data)? {
        ServiceInstruction::Init {} => init_escrow(program, accounts),
        ServiceInstruction::DepositEscrow { amount } => deposit_escrow(program, accounts, amount),
        ServiceInstruction::WithdrawEscrow {} => withdraw_escrow(program, accounts),
        ServiceInstruction::Pay { amount } => pay_utility_fees(program, accounts, amount),
    }
}

pub fn get_escrow(program: Pubkey, user: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&["ESCROW".as_bytes(), &user.to_bytes()], &program)
}

pub fn get_reserve(program: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&["RESERVE".as_bytes()], &program)
}


///
/// init escrow
///
fn init_escrow(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();

    let user = next_account_info(account_iter)?;
    let _reserve = next_account_info(account_iter)?;
    let escrow_account = next_account_info(account_iter)?;
    let sys_prog = next_account_info(account_iter)?;
  
    assert!(user.is_signer);
    assert!(escrow_account.data_is_empty());
    let (expected_escrow, escrow_bump) = get_escrow(*program, *user.key);

    invoke_signed(
      &system_instruction::create_account(
        &user.key,
        &expected_escrow,
        1,
        ESCROW_ACCOUNT_SIZE as u64,
        &program,
      ),
      &[user.clone(), escrow_account.clone(), sys_prog.clone()],
      &[&["ESCROW".as_bytes(), &user.key.to_bytes(), &[escrow_bump]]],
    )?;
  
    let escrow_data = Escrow {
        user: *user.key,
        amount: 0,
        bump: escrow_bump,
    };
  
    escrow_data.serialize(&mut &mut (*escrow_account.data).borrow_mut()[..]).unwrap();
  
    Ok(())
}

///
/// deposit escrow
///
fn deposit_escrow(
    program: &Pubkey,
    accounts: &[AccountInfo],
    deposit_amount: u16,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();

    let user = next_account_info(account_iter)?;
    let reserve = next_account_info(account_iter)?;
    let escrow_account = next_account_info(account_iter)?;
    let sys_prog = next_account_info(account_iter)?;

    assert!(user.is_signer);
    let (expected_reserve, _reserve_bump) = get_reserve(*program);
    assert_eq!(expected_reserve, *reserve.key);
    let (expected_escrow, _escrow_bump) = get_escrow(*program, *user.key);
    assert_eq!(expected_escrow, *escrow_account.key);

    invoke(
        &system_instruction::transfer(&user.key, &reserve.key, deposit_amount as u64),
        &[
            user.clone(),
            reserve.clone(),
            sys_prog.clone()
        ],
    )?;

    let escrow_data = &mut Escrow::deserialize(&mut &(*escrow_account.data).borrow_mut()[..])?;
    escrow_data.amount += deposit_amount;
    escrow_data
        .serialize(&mut &mut (*escrow_account.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

///
/// withdraw all balance in escrow
///
fn withdraw_escrow(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let account_iter = &mut accounts.iter();

    let user = next_account_info(account_iter)?;
    let reserve = next_account_info(account_iter)?;
    let escrow_account = next_account_info(account_iter)?;
    let sys_prog = next_account_info(account_iter)?;

    assert!(user.is_signer);
    let (expected_reserve, reserve_bump) = get_reserve(*program);
    assert_eq!(expected_reserve, *reserve.key);
    let (expected_escrow, _escrow_bump) = get_escrow(*program, *user.key);
    assert_eq!(expected_escrow, *escrow_account.key);

    let escrow_data = &mut Escrow::deserialize(&mut &(*escrow_account.data).borrow_mut()[..])?;
    let balance = escrow_data.amount;
    invoke_signed(
        &system_instruction::transfer(&reserve.key, &user.key, balance as u64),
        &[user.clone(), reserve.clone(), sys_prog.clone()],
        &[&["RESERVE".as_bytes(), &[reserve_bump]]],
    )?;

    escrow_data.amount = 0;
    escrow_data
        .serialize(&mut &mut (*escrow_account.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

///
/// pay utility
///
fn pay_utility_fees(program: &Pubkey, accounts: &[AccountInfo], amount: u16) -> ProgramResult {
    let account_iter = &mut accounts.iter();

    let user = next_account_info(account_iter)?;
    let reserve = next_account_info(account_iter)?;
    let escrow_account = next_account_info(account_iter)?;
    let _sys_prog = next_account_info(account_iter)?;

    assert!(user.is_signer);
    let (expected_reserve, _reserve_bump) = get_reserve(*program);
    assert_eq!(expected_reserve, *reserve.key);
    let (expected_escrow, _escrow_bump) = get_escrow(*program, *user.key);
    assert_eq!(expected_escrow, *escrow_account.key);

    let escrow_data = &mut Escrow::deserialize(&mut &(*escrow_account.data).borrow_mut()[..])?;

    let base_fee = 15_u16;
    if escrow_data.amount >= 10 {
        if amount < base_fee {
            escrow_data.amount -= base_fee;
        } else {
            assert!(escrow_data.amount >= amount);
            escrow_data.amount -= amount;
        }
    } else {
        msg!("ABORT: Cannot make payments when the escrow account has a balance less than 10 lamports.");
    }

    escrow_data
        .serialize(&mut &mut (*escrow_account.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}
