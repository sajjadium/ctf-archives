#![cfg(not(feature = "no-entrypoint"))]

use crate::processor::{self, SailorInstruction};
use borsh::BorshDeserialize;
use solana_program::{
    account_info::AccountInfo, entrypoint, entrypoint::ProgramResult, pubkey::Pubkey,
};

entrypoint!(process_instruction);
fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let ins = SailorInstruction::try_from_slice(instruction_data)?;
    match ins {
        SailorInstruction::CreateUnion(bal) => processor::create_union(program_id, accounts, bal),
        SailorInstruction::PayDues(amt) => processor::pay_dues(program_id, accounts, amt),
        SailorInstruction::StrikePay(amt) => processor::strike_pay(program_id, accounts, amt),
        SailorInstruction::RegisterMember(member) => processor::register_member(program_id, accounts, member)
    }
}
