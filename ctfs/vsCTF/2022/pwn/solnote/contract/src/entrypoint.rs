// taken from https://github.com/otter-sec/sol-ctf-framework/blob/main/examples/moar-horse-5/program/src/entrypoint.rs
#![cfg(not(feature = "no-entrypoint"))]

use solana_program::{
    account_info::AccountInfo, entrypoint, entrypoint::ProgramResult, pubkey::Pubkey,
};

entrypoint!(start);
fn start(program_id: &Pubkey, accounts: &[AccountInfo], instruction_data: &[u8]) -> ProgramResult {
    crate::processor::process_instruction(program_id, accounts, instruction_data)
}
