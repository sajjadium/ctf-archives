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
pub enum SolInstruction {
  Initialize,
  Propose { proposal_id: u32 },
  Vote { proposal_id: u32, amount: u32 },
  Withdraw { amount: u64 }
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Config {
  pub admin: Pubkey,
  pub total_balance: u64
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Proposal {
  pub creator: Pubkey, 
  pub balance: u32,
  pub proposal_id: u32
}

pub const CONFIG_SIZE: usize = size_of::<Config>();
pub const PROPOSAL_SIZE: usize = size_of::<Proposal>();

pub fn get_config(program: Pubkey) -> (Pubkey, u8) {
  Pubkey::find_program_address(&["CONFIG".as_bytes()], &program)
}
pub fn get_vault(program: Pubkey) -> (Pubkey, u8) {
  Pubkey::find_program_address(&["VAULT".as_bytes()], &program)
}
pub fn get_proposal(program: Pubkey, proposal_id: u32) -> (Pubkey, u8) {
  Pubkey::find_program_address(&["PROPOSAL".as_bytes(), &proposal_id.to_be_bytes()], &program)
}

pub fn initialize(program: Pubkey, user: Pubkey) -> Instruction {
  let (config, _) = get_config(program);
  let (vault, _) = get_vault(program);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(config, false),
      AccountMeta::new(vault, false),
      AccountMeta::new(user, true),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: SolInstruction::Initialize.try_to_vec().unwrap(),
  }
}

pub fn propose(program: Pubkey, user: Pubkey, creator: Pubkey, proposal_id: u32) -> Instruction {
  let (config, _) = get_config(program);
  let (proposal, _) = get_proposal(program, proposal_id);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(config, false),
      AccountMeta::new(user, true),
      AccountMeta::new(creator, true),
      AccountMeta::new(proposal, false),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: SolInstruction::Propose{ proposal_id }.try_to_vec().unwrap(),
  }
}

pub fn vote(program: Pubkey, user: Pubkey, proposal_id: u32, amount: u32) -> Instruction {
  let (config, _) = get_config(program);
  let (vault, _) = get_vault(program);
  let (proposal, _) = get_proposal(program, proposal_id);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(config, false),
      AccountMeta::new(vault, false),
      AccountMeta::new(user, true),
      AccountMeta::new(proposal, false),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: SolInstruction::Vote{ proposal_id, amount }.try_to_vec().unwrap(),
  }
}

pub fn withdraw(program: Pubkey, user: Pubkey, amount: u64) -> Instruction {
  let (config, _) = get_config(program);
  let (vault, _) = get_vault(program);
  Instruction {
    program_id: program,
    accounts: vec![
      AccountMeta::new(config, false),
      AccountMeta::new(vault, false),
      AccountMeta::new(user, true),
      AccountMeta::new_readonly(system_program::id(), false),
    ],
    data: SolInstruction::Withdraw{ amount }.try_to_vec().unwrap(),
  }
}