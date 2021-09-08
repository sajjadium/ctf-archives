use arrayref::array_ref;
use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::AccountInfo,
    clock::Clock,
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    program_error::ProgramError,
    program_pack::Pack,
    pubkey::Pubkey,
    rent::Rent,
    system_instruction,
    sysvar::Sysvar,
};
use spl_token::state::Account;

use crate::{Bank, BankInstruction, UserAccount, BANK_LEN, DEFAULT_INTEREST_RATE};

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    match BankInstruction::try_from_slice(instruction_data)? {
        BankInstruction::Initialize { reserve_rate } => {
            initialize(program_id, accounts, reserve_rate)
        }
        BankInstruction::Open => open(program_id, accounts),
        BankInstruction::Deposit { amount } => deposit(program_id, accounts, amount),
        BankInstruction::Withdraw { amount } => withdraw(program_id, accounts, amount),
        BankInstruction::Invest { amount } => invest(program_id, accounts, amount),
    }
}

/// See struct BankInstruction for docs
fn initialize(program_id: &Pubkey, accounts: &[AccountInfo], reserve_rate: u8) -> ProgramResult {
    let [bank_info, manager_info, vault_info, vault_authority_info, mint_info, rent_info, _system_program, _token_program] =
        array_ref![accounts, 0, 8];

    let (bank_address, bank_seed) = Pubkey::find_program_address(&[], program_id);
    if *bank_info.key != bank_address {
        return Err(ProgramError::InvalidArgument);
    }

    if !manager_info.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let rent = Rent::from_account_info(rent_info)?;

    let (vault_key, vault_seed) =
        Pubkey::find_program_address(&[bank_address.as_ref()], program_id);
    if vault_info.key != &vault_key {
        return Err(ProgramError::InvalidArgument);
    }
    let (vault_authority, vault_authority_seed) =
        Pubkey::find_program_address(&[vault_key.as_ref()], program_id);
    if vault_authority_info.key != &vault_authority {
        return Err(ProgramError::InvalidArgument);
    }

    let bank = Bank {
        manager_key: manager_info.key.to_bytes(),
        vault_key: vault_key.to_bytes(),
        vault_authority: vault_authority.to_bytes(),
        vault_authority_seed,
        reserve_rate,
        total_deposit: 0,
    };

    invoke_signed(
        &system_instruction::create_account(
            &manager_info.key,
            &vault_key,
            rent.minimum_balance(Account::get_packed_len()),
            Account::get_packed_len() as u64,
            &spl_token::ID,
        ),
        &[manager_info.clone(), vault_info.clone()],
        &[&[bank_address.as_ref(), &[vault_seed]]],
    )?;

    invoke_signed(
        &spl_token::instruction::initialize_account(
            &spl_token::ID,
            &vault_key,
            mint_info.key,
            vault_authority_info.key,
        )?,
        &[
            vault_info.clone(),
            mint_info.clone(),
            vault_authority_info.clone(),
            rent_info.clone(),
        ],
        &[&[bank_address.as_ref(), &[vault_seed]]],
    )?;

    invoke_signed(
        &system_instruction::create_account(
            &manager_info.key,
            &bank_address,
            rent.minimum_balance(BANK_LEN as usize),
            BANK_LEN,
            &program_id,
        ),
        &[manager_info.clone(), bank_info.clone()],
        &[&[&[bank_seed]]],
    )?;

    bank.serialize(&mut &mut bank_info.data.borrow_mut()[..])?;
    Ok(())
}

/// See struct BankInstruction for docs
fn open(program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let [user_account_info, withdrawer_info, _system_program] = array_ref![accounts, 0, 3];

    // account must be program-derived account (PDA) from withdrawer
    let (address, seed) =
        Pubkey::find_program_address(&[&withdrawer_info.key.to_bytes()], program_id);
    if address != *user_account_info.key {
        return Err(0xfeedface.into());
    }

    // create a new account
    let user_account = UserAccount {
        balance: 0,
        interest_paid_time: 0,
        interest_rate: DEFAULT_INTEREST_RATE,
    };
    let data = user_account.try_to_vec()?;
    let rent_amount = Rent::default().minimum_balance(data.len());

    invoke_signed(
        &system_instruction::create_account(
            &withdrawer_info.key,
            &user_account_info.key,
            rent_amount,
            data.len() as u64,
            program_id,
        ),
        &[user_account_info.clone(), withdrawer_info.clone()],
        &[&[&withdrawer_info.key.to_bytes(), &[seed]]],
    )?;
    user_account_info.data.borrow_mut().copy_from_slice(&data);

    Ok(())
}

/// See struct BankInstruction for docs
fn deposit(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let [bank_info, vault_info, user_account_info, source_token_account_info, source_authority_info, _spl_token_program, clock_info] =
        array_ref![accounts, 0, 7];

    // check that the bank account is correct
    let (bank_address, _) = Pubkey::find_program_address(&[], program_id);
    if *bank_info.key != bank_address {
        return Err(ProgramError::InvalidArgument);
    }

    let (vault_key, _) = Pubkey::find_program_address(&[bank_address.as_ref()], program_id);
    if vault_info.key != &vault_key {
        return Err(ProgramError::InvalidArgument);
    }

    // check that the user account is an account owned by the program
    // and not the bank itself
    if user_account_info.owner != program_id || *user_account_info.key == bank_address {
        return Err(ProgramError::InvalidArgument);
    }

    let clock = Clock::from_account_info(clock_info)?;

    let mut bank: Bank = Bank::try_from_slice(&bank_info.data.borrow())?;
    let mut user_account: UserAccount =
        UserAccount::try_from_slice(&user_account_info.data.borrow())?;

    bank.total_deposit += amount + user_account.pay_interest(clock.unix_timestamp);
    user_account.balance += amount;

    invoke(
        &spl_token::instruction::transfer(
            &spl_token::ID,
            &source_token_account_info.key,
            &vault_info.key,
            &source_authority_info.key,
            &[],
            amount,
        )?,
        &[
            vault_info.clone(),
            source_token_account_info.clone(),
            source_authority_info.clone(),
        ],
    )?;

    user_account.serialize(&mut &mut user_account_info.data.borrow_mut()[..])?;
    bank.serialize(&mut &mut bank_info.data.borrow_mut()[..])?;
    Ok(())
}

/// See struct BankInstruction for docs
fn withdraw(program_id: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let [bank_info, vault_info, vault_authority_info, user_account_info, dest_token_account_info, withdrawer_info, _spl_token_program, clock_info] =
        array_ref![accounts, 0, 8];

    let (bank_address, _) = Pubkey::find_program_address(&[], program_id);
    if *bank_info.key != bank_address {
        return Err(ProgramError::InvalidArgument);
    }

    let mut bank: Bank = Bank::try_from_slice(&bank_info.data.borrow())?;

    if vault_info.key.as_ref() != &bank.vault_key {
        return Err(ProgramError::InvalidArgument);
    }

    // check that authorized withdrawer signed the transaction
    let (address, _) = Pubkey::find_program_address(&[&withdrawer_info.key.to_bytes()], program_id);
    if address != *user_account_info.key {
        return Err(0xfeedface.into());
    };
    if !withdrawer_info.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    let clock = Clock::from_account_info(clock_info)?;

    let mut user_account: UserAccount =
        UserAccount::try_from_slice(&user_account_info.data.borrow())?;

    bank.total_deposit += user_account.pay_interest(clock.unix_timestamp);
    if user_account.balance < amount {
        return Err(ProgramError::InsufficientFunds);
    }
    bank.total_deposit -= amount;
    user_account.balance -= amount;

    invoke_signed(
        &spl_token::instruction::transfer(
            &spl_token::ID,
            &vault_info.key,
            &dest_token_account_info.key,
            &vault_authority_info.key,
            &[],
            amount,
        )?,
        &[
            vault_info.clone(),
            dest_token_account_info.clone(),
            vault_authority_info.clone(),
        ],
        &[&[vault_info.key.as_ref(), &[bank.vault_authority_seed]]],
    )?;

    Ok(())
}

/// See struct BankInstruction for docs
fn invest(_program_id: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
    let [bank_info, vault_info, vault_authority_info, dest_token_account_info, manager_info, _spl_token_program] =
        array_ref![accounts, 0, 6];
    // verify that manager has approved
    if !manager_info.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // verify that manager is correct
    let bank: Bank = Bank::try_from_slice(&bank_info.data.borrow())?;
    if bank.manager_key != manager_info.key.to_bytes() {
        return Err(0xbeefbeef.into());
    }

    // verify that the vault is correct
    if vault_info.key.as_ref() != &bank.vault_key {
        return Err(ProgramError::InvalidArgument);
    }

    // verify that enough money is left in reserve
    let vault = spl_token::state::Account::unpack(&vault_info.data.borrow())?;
    if (vault.amount - amount) * 100 < bank.total_deposit * u64::from(bank.reserve_rate) {
        return Err(0xfeedf00d.into());
    }

    // transfer tokens to manager
    invoke_signed(
        &spl_token::instruction::transfer(
            &spl_token::ID,
            &vault_info.key,
            &dest_token_account_info.key,
            &vault_authority_info.key,
            &[],
            amount,
        )?,
        &[
            vault_info.clone(),
            dest_token_account_info.clone(),
            vault_authority_info.clone(),
        ],
        &[&[vault_info.key.as_ref(), &[bank.vault_authority_seed]]],
    )?;

    Ok(())
}
