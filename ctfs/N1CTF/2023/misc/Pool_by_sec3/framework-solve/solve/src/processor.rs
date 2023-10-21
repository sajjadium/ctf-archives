use borsh::{BorshSerialize, BorshDeserialize};

use solana_program::{
    account_info::{
        next_account_info,
        AccountInfo,
    },
    entrypoint::ProgramResult,
    instruction::{
        AccountMeta,
        Instruction,
    },
    program::invoke,
    pubkey::Pubkey,
};

pub fn process_instruction(_program: &Pubkey, accounts: &[AccountInfo], _data: &[u8]) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let admin = next_account_info(accounts_iter)?;
    let user = next_account_info(accounts_iter)?;
    let user_token_account = next_account_info(accounts_iter)?;
    let pool = next_account_info(accounts_iter)?;
    let mint = next_account_info(accounts_iter)?;
    let chall_id = next_account_info(accounts_iter)?;
    let rent = next_account_info(accounts_iter)?;
    let token_program = next_account_info(accounts_iter)?;
    let associated_token_program = next_account_info(accounts_iter)?;
    let system_program = next_account_info(accounts_iter)?;

    // your code goes here

    Ok(())
}