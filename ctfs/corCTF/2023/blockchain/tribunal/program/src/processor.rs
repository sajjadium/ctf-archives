use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    program_error::ProgramError,
    pubkey::Pubkey,
    rent::Rent,
    system_instruction,
};

#[derive(BorshDeserialize, BorshSerialize)]
pub enum TribunalInstruction {
    Initialize { config_bump: u8, vault_bump: u8 },
    Propose { proposal_id: u8, proposal_bump: u8 },
    Vote { proposal_id: u8, amount: u64 },
    Withdraw { amount: u64 },
}

#[repr(u8)]
#[derive(BorshSerialize, BorshDeserialize, PartialEq)]
pub enum Types {
    Config,
    Proposal,
    Vault,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Config {
    pub discriminator: Types,
    pub admin: Pubkey,
    pub total_balance: u64,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Proposal {
    pub discriminator: Types,
    pub creator: Pubkey,
    pub balance: u64,
    pub proposal_id: u8,
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Vault {
    pub discriminator: Types,
}

pub const CONFIG_SIZE: usize = std::mem::size_of::<Config>();
pub const PROPOSAL_SIZE: usize = std::mem::size_of::<Proposal>();
pub const VAULT_SIZE: usize = std::mem::size_of::<Vault>();

pub fn process_instruction(
    program: &Pubkey,
    accounts: &[AccountInfo],
    mut data: &[u8],
) -> ProgramResult {
    match TribunalInstruction::deserialize(&mut data)? {
        TribunalInstruction::Initialize {
            config_bump,
            vault_bump,
        } => initialize(program, accounts, config_bump, vault_bump),
        TribunalInstruction::Propose {
            proposal_id,
            proposal_bump,
        } => propose(program, accounts, proposal_id, proposal_bump),
        TribunalInstruction::Vote {
            proposal_id,
            amount,
        } => vote(program, accounts, proposal_id, amount),
        TribunalInstruction::Withdraw { amount } => withdraw(program, accounts, amount),
    }
}

// initialize config, should only run once
fn initialize(
    program: &Pubkey,
    accounts: &[AccountInfo],
    config_bump: u8,
    vault_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let config = next_account_info(account_iter)?;
    let vault = next_account_info(account_iter)?;

    // ensure that the user signed this
    if !user.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // get config and vault
    let Ok(config_addr) = Pubkey::create_program_address(&[b"CONFIG", &[config_bump]], &program) else {
        return Err(ProgramError::InvalidSeeds);
    };

    let Ok(vault_addr) = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], &program) else {
        return Err(ProgramError::InvalidSeeds);
    };

    // assert that the config passed in is at the right address
    if *config.key != config_addr {
        return Err(ProgramError::InvalidAccountData);
    }

    // ensure that the config passed in is empty (we only want to initialize once)
    if !config.data_is_empty() {
        return Err(ProgramError::AccountAlreadyInitialized);
    }

    // create config
    invoke_signed(
        &system_instruction::create_account(
            &user.key,
            &config_addr,
            Rent::minimum_balance(&Rent::default(), CONFIG_SIZE),
            CONFIG_SIZE as u64,
            &program,
        ),
        &[user.clone(), config.clone()],
        &[&[b"CONFIG", &[config_bump]]],
    )?;

    // save config data
    let config_data = Config {
        discriminator: Types::Config,
        admin: *user.key,
        total_balance: 0,
    };

    config_data
        .serialize(&mut &mut (*config.data).borrow_mut()[..])
        .unwrap();

    // create vault
    invoke_signed(
        &system_instruction::create_account(
            &user.key,
            &vault_addr,
            Rent::minimum_balance(&Rent::default(), VAULT_SIZE),
            VAULT_SIZE as u64,
            &program,
        ),
        &[user.clone(), vault.clone()],
        &[&[b"VAULT", &[vault_bump]]],
    )?;

    // save vault data
    let vault_data = Vault {
        discriminator: Types::Vault,
    };

    vault_data
        .serialize(&mut &mut (*vault.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

// create a proposal, only allowed by admin (since we don't want dumb proposals)
fn propose(
    program: &Pubkey,
    accounts: &[AccountInfo],
    proposal_id: u8,
    proposal_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let config = next_account_info(account_iter)?;
    let proposal = next_account_info(account_iter)?;

    // ensure that the user signed this
    if !user.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // require that the config is valid
    if config.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    // retrieve config data
    let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;
    if config_data.discriminator != Types::Config {
        return Err(ProgramError::InvalidAccountData);
    }

    // require that the user is an admin
    if *user.key != config_data.admin {
        return Err(ProgramError::IllegalOwner);
    }

    let Ok(proposal_addr) = Pubkey::create_program_address(&[b"PROPOSAL", &proposal_id.to_be_bytes(), &[proposal_bump]], &program) else {
        return Err(ProgramError::InvalidSeeds);
    };

    // require that the proposal passed in is at the right address
    if *proposal.key != proposal_addr {
        return Err(ProgramError::InvalidAccountData);
    }

    // ensure that the proposal isn't initialized yet
    if !proposal.data_is_empty() {
        return Err(ProgramError::AccountAlreadyInitialized);
    }

    // create proposal
    invoke_signed(
        &system_instruction::create_account(
            &user.key,
            &proposal_addr,
            Rent::minimum_balance(&Rent::default(), PROPOSAL_SIZE),
            PROPOSAL_SIZE as u64,
            &program,
        ),
        &[user.clone(), proposal.clone()],
        &[&[
            "PROPOSAL".as_bytes(),
            &proposal_id.to_be_bytes(),
            &[proposal_bump],
        ]],
    )?;

    // save proposal data
    let proposal_data = Proposal {
        discriminator: Types::Proposal,
        creator: *user.key,
        balance: 0,
        proposal_id,
    };

    proposal_data
        .serialize(&mut &mut (*proposal.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

fn vote(
    program: &Pubkey,
    accounts: &[AccountInfo],
    proposal_id: u8,
    lamports: u64,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let config = next_account_info(account_iter)?;
    let vault = next_account_info(account_iter)?;
    let proposal = next_account_info(account_iter)?;

    // ensure that the user signed this
    if !user.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // positive amount
    if lamports <= 0 {
        return Err(ProgramError::InvalidArgument);
    }

    // require that the config is correct
    if config.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;
    if config_data.discriminator != Types::Config {
        return Err(ProgramError::InvalidAccountData);
    }

    // require that the vault is correct
    if vault.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    let vault_data = &mut Vault::deserialize(&mut &(*vault.data).borrow_mut()[..])?;
    if vault_data.discriminator != Types::Vault {
        return Err(ProgramError::InvalidAccountData);
    }

    // ensure the proposal is valid
    if proposal.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    let proposal_data = &mut Proposal::deserialize(&mut &(*proposal.data).borrow_mut()[..])?;
    if proposal_data.discriminator != Types::Proposal {
        return Err(ProgramError::InvalidAccountData);
    }

    // check that proposal is at the correct address
    let (proposal_addr, _) = Pubkey::find_program_address(
        &["PROPOSAL".as_bytes(), &proposal_id.to_be_bytes()],
        &program,
    );
    if *proposal.key != proposal_addr {
        return Err(ProgramError::InvalidAccountData);
    }

    // transfer money to vault
    invoke(
        &system_instruction::transfer(&user.key, &vault.key, lamports.into()),
        &[user.clone(), vault.clone()],
    )?;

    // update the proposal balance
    proposal_data.balance = proposal_data.balance.checked_add(lamports).unwrap();
    proposal_data
        .serialize(&mut &mut (*proposal.data).borrow_mut()[..])
        .unwrap();

    // update the config total balance
    config_data.total_balance = config_data.total_balance.checked_add(lamports).unwrap() - 100; // keep some for rent
    config_data
        .serialize(&mut &mut (*config.data).borrow_mut()[..])
        .unwrap();

    Ok(())
}

fn withdraw(program: &Pubkey, accounts: &[AccountInfo], lamports: u64) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let user = next_account_info(account_iter)?;
    let config = next_account_info(account_iter)?;
    let vault = next_account_info(account_iter)?;

    // ensure that the user signed this
    if !user.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    // positive amount
    if lamports <= 0 {
        return Err(ProgramError::InvalidArgument);
    }

    // require that the config is correct
    if config.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    let config_data = &mut Config::deserialize(&mut &(*config.data).borrow_mut()[..])?;
    if config_data.discriminator != Types::Config {
        return Err(ProgramError::InvalidAccountData);
    }

    // check that the config has enough balance
    if config_data.total_balance < lamports {
        return Err(ProgramError::InsufficientFunds);
    }

    // require that the user is an admin
    if *user.key != config_data.admin {
        return Err(ProgramError::IllegalOwner);
    }

    // require that the vault is correct
    if vault.owner != program {
        return Err(ProgramError::InvalidAccountData);
    }

    let vault_data = &mut Vault::deserialize(&mut &(*vault.data).borrow_mut()[..])?;
    if vault_data.discriminator != Types::Vault {
        return Err(ProgramError::InvalidAccountData);
    }

    // withdraw safely
    let mut vault_lamports = vault.lamports.borrow_mut();
    **vault_lamports = (**vault_lamports).checked_sub(lamports).unwrap();
    let mut user_lamports = user.lamports.borrow_mut();
    **user_lamports = (**user_lamports).checked_add(lamports).unwrap();

    Ok(())
}
