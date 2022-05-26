mod entrypoint;
pub mod processor;

use borsh::{
  BorshDeserialize,
  BorshSerialize,
};

use solana_program::{
  instruction::{
    AccountMeta,
    Instruction,
  },
  pubkey::Pubkey,
  system_program,
};

use std::mem::size_of;

#[derive(BorshDeserialize, BorshSerialize)]
pub enum HorseInstruction {
  Create { horse_bump: u8, wallet_bump: u8 },
  Buy { amount: u64 },
  Sell { amount: u64 },
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct HorseWallet {
  pub user: Pubkey,
  pub horse: Pubkey,
  pub amount: u64,
  pub horse_bump: u8,
}

pub const WALLET_SIZE: usize = size_of::<HorseWallet>();
pub const HORSE_COST: u64 = 1000;

pub fn get_horse(program: Pubkey) -> (Pubkey, u8) {
  Pubkey::find_program_address(&["HORSE".as_bytes()], &program)
}

pub fn get_wallet(program: Pubkey, user: Pubkey) -> (Pubkey, u8) {
  Pubkey::find_program_address(&["WALLET".as_bytes(), &user.to_bytes()], &program)
}

pub fn create(program: Pubkey, user: Pubkey) -> Instruction {
  let (horse, horse_bump) = get_horse(program);
  let (wallet, wallet_bump) = get_wallet(program, user);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(horse, false),
      AccountMeta::new(wallet, false),
      AccountMeta::new(user, true),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: HorseInstruction::Create { horse_bump, wallet_bump } .try_to_vec().unwrap(),
  }
}

pub fn buy(program: Pubkey, user: Pubkey, amount: u64) -> Instruction {
  let (horse, _) = get_horse(program);
  let (wallet, _) = get_wallet(program, user);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(horse, false),
      AccountMeta::new(wallet, false),
      AccountMeta::new(user, true),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: HorseInstruction::Buy { amount }.try_to_vec().unwrap(),
  }
}

pub fn sell(program: Pubkey, user: Pubkey, amount: u64) -> Instruction {
  let (horse, _) = get_horse(program);
  let (wallet, _) = get_wallet(program, user);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(horse, false),
      AccountMeta::new(wallet, false),
      AccountMeta::new(user, true),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: HorseInstruction::Sell { amount }.try_to_vec().unwrap(),
  }
}
