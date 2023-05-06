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
  SolInstruction,
  Config,
  Proposal,
  CONFIG_SIZE,
  PROPOSAL_SIZE,

  get_config,
  get_vault,
  get_proposal
};

pub fn process_instruction(program: &Pubkey, accounts: &[AccountInfo], mut data: &[u8]) -> ProgramResult {
  match SolInstruction::deserialize(&mut data)? {
    SolInstruction::Initialize => initialize(program, accounts),
    SolInstruction::Propose { proposal_id } => propose(program, accounts, proposal_id),
    SolInstruction::Vote { proposal_id, amount } => vote(program, accounts, proposal_id, amount),
    SolInstruction::Withdraw { amount } => withdraw(program, accounts, amount)
  }
}

// initialize solidarity config, should only run once
fn initialize(program: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let config = next_account_info(account_iter)?;
  let vault = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;

  let (config_addr, config_seed) = get_config(*program);
  let (vault_addr, vault_seed) = get_vault(*program);

  // assert that the config passed in is at the right address and is empty
  assert_eq!(*config.key, config_addr);
  if !config.data_is_empty() {
    return Err(ProgramError::AccountAlreadyInitialized);
  }

  // create config
  invoke_signed(
    &system_instruction::create_account(
      &user.key,
      &config_addr,
      1,
      CONFIG_SIZE as u64,
      &program,
    ),
    &[user.clone(), config.clone()],
    &[&["CONFIG".as_bytes(), &[config_seed]]]
  )?;

  // save config data
  let config_data = Config {
    admin: *user.key,
    total_balance: 0
  };

  config_data
    .serialize(&mut &mut (*config.data).borrow_mut()[..])
    .unwrap();

  // create vault
  invoke_signed(
    &system_instruction::create_account(
      &user.key,
      &vault_addr,
      1,
      0,
      &program,
    ),
    &[user.clone(), vault.clone()],
    &[&["VAULT".as_bytes(), &[vault_seed]]]
  )?;

  Ok(())
}

// create a proposal, only allowed by admin (since we don't want dumb proposals)
fn propose(program: &Pubkey, accounts: &[AccountInfo], proposal_id: u32) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let config = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;
  let creator = next_account_info(account_iter)?;
  let proposal = next_account_info(account_iter)?;

  // assert that the config is valid
  assert_eq!(config.owner, program);

  // retrieve config data
  let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;

  // assert that the user is an admin
  assert_eq!(*user.key, config_data.admin);

  let (proposal_addr, proposal_seed) = get_proposal(*program, proposal_id);

  // assert that the proposal passed in is at the right address and is empty
  assert_eq!(*proposal.key, proposal_addr);
  if !proposal.data_is_empty() {
    return Err(ProgramError::AccountAlreadyInitialized);
  }

  // create proposal
  invoke_signed(
    &system_instruction::create_account(
      &creator.key,
      &proposal_addr,
      1,
      PROPOSAL_SIZE as u64,
      &program,
    ),
    &[creator.clone(), proposal.clone()],
    &[&["PROPOSAL".as_bytes(), &proposal_id.to_be_bytes(), &[proposal_seed]]]
  )?;

  // save proposal data
  let proposal_data = Proposal {
    creator: *creator.key,
    balance: 0,
    proposal_id
  };

  proposal_data
    .serialize(&mut &mut (*proposal.data).borrow_mut()[..])
    .unwrap();

  Ok(())
}

fn vote(program: &Pubkey, accounts: &[AccountInfo], proposal_id: u32, lamports: u32) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let config = next_account_info(account_iter)?;
  let vault = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;
  let proposal = next_account_info(account_iter)?;

  // positive amount
  if lamports <= 0 {
    return Err(ProgramError::InvalidArgument);
  }

  // assert that the config, vault, and proposal are correct
  assert_eq!(config.owner, program);
  assert_eq!(vault.owner, program);
  assert_eq!(proposal.owner, program);

  let (proposal_addr, _) = get_proposal(*program, proposal_id);
  assert_eq!(*proposal.key, proposal_addr);

  // update the config total balance
  let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;
  config_data.total_balance = config_data.total_balance.checked_add(lamports.into()).unwrap();
  config_data
    .serialize(&mut &mut (*config.data).borrow_mut()[..])
    .unwrap();

  // update the proposal balance
  let proposal_data = &mut Proposal::deserialize(&mut &(*proposal.data).borrow_mut()[..])?;
  proposal_data.balance = proposal_data.balance.checked_add(lamports).unwrap();
  proposal_data
    .serialize(&mut &mut (*proposal.data).borrow_mut()[..])
    .unwrap();

  // transfer money to vault
  invoke(
    &system_instruction::transfer(
      &user.key,
      &vault.key,
      lamports.into(),
    ),
    &[user.clone(), vault.clone()],
  )?;

  Ok(())
}

fn withdraw(program: &Pubkey, accounts: &[AccountInfo], lamports: u64) -> ProgramResult {
  let account_iter = &mut accounts.iter();
  let config = next_account_info(account_iter)?;
  let vault = next_account_info(account_iter)?;
  let user = next_account_info(account_iter)?;

  // positive amount
  if lamports <= 0 {
    return Err(ProgramError::InvalidArgument);
  }

  // assert that the config, vault, and proposal are correct
  assert_eq!(config.owner, program);
  assert_eq!(vault.owner, program);

  // assert that we actually have the vault
  let (vault_addr, _) = get_vault(*program);
  assert_eq!(*vault.key, vault_addr);

  // retrieve config data
  let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;

  // assert that the user is an admin
  assert_eq!(*user.key, config_data.admin);

  // make sure you can withdraw that much
  if lamports > config_data.total_balance {
    return Err(ProgramError::InsufficientFunds);
  }

    // update the config total balance
  let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;
  config_data.total_balance = config_data.total_balance.checked_sub(lamports.into()).unwrap();
  config_data
    .serialize(&mut &mut (*config.data).borrow_mut()[..])
    .unwrap();

  // withdraw safely
  let mut vault_lamports = vault.lamports.borrow_mut();
  **vault_lamports = (**vault_lamports).checked_sub(lamports).unwrap();
  let mut user_lamports = user.lamports.borrow_mut();
  **user_lamports = (**user_lamports).checked_add(lamports).unwrap();

  Ok(())
}