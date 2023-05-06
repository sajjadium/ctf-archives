use borsh::{
  BorshDeserialize,
  BorshSerialize,
};

use solana_program::{
  account_info::{
    next_account_info,
    AccountInfo,
  },
  entrypoint::ProgramResult,
  program::{
    invoke,
    invoke_signed,
  },
  program_error::ProgramError,
  pubkey::Pubkey,
  system_instruction,
};

use crate::{
  HorseInstruction,
  HorseWallet,
  HORSE_COST,
  WALLET_SIZE,
};

pub fn process_instruction(program: &Pubkey, accounts: &[AccountInfo], mut data: &[u8]) -> ProgramResult {
  match HorseInstruction::deserialize(&mut data)? {
    HorseInstruction::Create { horse_bump, wallet_bump } => create(program, accounts, horse_bump, wallet_bump),
    HorseInstruction::Buy { amount } => buy(program, accounts, amount),
    HorseInstruction::Sell { amount } => sell(program, accounts, amount),
  }
}

fn create(program: &Pubkey, accounts: &[AccountInfo], horse_bump: u8, wallet_bump: u8) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let horse = next_account_info(account_iter)?;
  let wallet = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;

  let horse_address = Pubkey::create_program_address(&["HORSE".as_bytes(), &[horse_bump]], &program)?;
  let wallet_address = Pubkey::create_program_address(&["WALLET".as_bytes(), &user.key.to_bytes(), &[wallet_bump]], &program)?;

  assert_eq!(*horse.key, horse_address);
  assert_eq!(*wallet.key, wallet_address);
  assert!(wallet.data_is_empty());
  assert!(user.is_signer);

  invoke_signed(
    &system_instruction::create_account(
      &user.key,
      &wallet_address,
      1,
      WALLET_SIZE as u64,
      &program,
    ),
    &[user.clone(), wallet.clone()],
    &[&["WALLET".as_bytes(), &user.key.to_bytes(), &[wallet_bump]]],
  )?;

  let wallet_data = HorseWallet {
    user: *user.key,
    horse: horse_address,
    amount: 0,
    horse_bump: horse_bump,
  };

  wallet_data.serialize(&mut &mut (*wallet.data).borrow_mut()[..]).unwrap();

  Ok(())
}

fn buy(program: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let horse = next_account_info(account_iter)?;
  let wallet = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;

  assert_eq!(wallet.owner, program);
  assert!(user.is_signer);
  let wallet_data = &mut HorseWallet::deserialize(&mut &(*wallet.data).borrow_mut()[..])?;
  assert_eq!(wallet_data.horse, *horse.key);
  assert_eq!(wallet_data.user, *user.key);

  invoke(
    &system_instruction::transfer(
      &user.key,
      &horse.key,
      HORSE_COST * amount,
    ),
    &[user.clone(), horse.clone()],
  )?;

  wallet_data.amount += amount;
  wallet_data.serialize(&mut &mut (*wallet.data).borrow_mut()[..]).unwrap();

  Ok(())
}

fn sell(program: &Pubkey, accounts: &[AccountInfo], amount: u64) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let horse = next_account_info(account_iter)?;
  let wallet = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;

  assert_eq!(wallet.owner, program);
  assert!(user.is_signer);
  let wallet_data = &mut HorseWallet::deserialize(&mut &(*wallet.data).borrow_mut()[..])?;
  assert_eq!(wallet_data.horse, *horse.key);
  assert_eq!(wallet_data.user, *user.key);

  if amount > wallet_data.amount {
    return Err(ProgramError::InsufficientFunds);
  }

  invoke_signed(
    &system_instruction::transfer(
      &horse.key,
      &user.key,
      HORSE_COST * amount,
    ),
    &[horse.clone(), user.clone()],
    &[&["HORSE".as_bytes(), &[wallet_data.horse_bump]]],
  )?;

  wallet_data.amount -= amount;
  wallet_data.serialize(&mut &mut (*wallet.data).borrow_mut()[..]).unwrap();

  Ok(())
}
