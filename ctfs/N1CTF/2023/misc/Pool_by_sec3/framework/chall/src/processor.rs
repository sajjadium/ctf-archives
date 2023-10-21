use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, pubkey::Pubkey};

use crate::instructions::{
    management::init_pool,
    user::{deposit, withdraw},
};

#[derive(BorshSerialize, BorshDeserialize)]
pub enum PoolInstruction {
    /// Initialize a new pool
    InitPool(u64),
    /// Deposit into the pool
    Deposit(u64, Vec<u8>),
    /// Withdraw from the pool
    Withdraw(u64, Vec<u8>),
}

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    input: &[u8],
) -> ProgramResult {
    let instruction = PoolInstruction::try_from_slice(input)?;
    match instruction {
        // Admin instructions
        PoolInstruction::InitPool(args) => init_pool(program_id, accounts, args),

        // User instructions
        PoolInstruction::Deposit(amount, account_name) => deposit(program_id, accounts, amount, account_name),
        PoolInstruction::Withdraw(amount, account_name) => withdraw(program_id, accounts, amount, account_name),
    }
}