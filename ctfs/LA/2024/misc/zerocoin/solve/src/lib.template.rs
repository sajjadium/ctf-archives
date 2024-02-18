#[cfg(not(feature = "no-entrypoint"))]
pub mod entrypoint {
    use anchor_lang::prelude::*;
    use solana_program::{
        account_info::AccountInfo, entrypoint, entrypoint::ProgramResult
    };
    use zerocoin::cpi;

    entrypoint!(process_instruction);

    pub fn process_instruction(
        _program_id: &Pubkey,
        _accounts: &[AccountInfo],
        _instruction_data: &[u8],
    ) -> ProgramResult {
        Ok(())
    }
}
