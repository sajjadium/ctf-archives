use borsh::BorshSerialize;

use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    instruction::{AccountMeta, Instruction},
    program::invoke,
    pubkey::Pubkey,
    system_program,
};

use utility_payment::ServiceInstruction;

pub fn process_instruction(
    _program: &Pubkey,
    accounts: &[AccountInfo],
    _data: &[u8],
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let utility_program = next_account_info(account_iter)?;
    let user = next_account_info(account_iter)?;
    let reserve = next_account_info(account_iter)?;
    let escrow_account = next_account_info(account_iter)?;
    let sys_prog_account = next_account_info(account_iter)?;

    invoke(
        &Instruction {
            program_id: *utility_program.key,
            accounts: vec![
                AccountMeta::new(*user.key, true),
                AccountMeta::new(*reserve.key, false),
                AccountMeta::new(*escrow_account.key, false),
                AccountMeta::new_readonly(system_program::id(), false),
            ],
            data: ServiceInstruction::Init { }
                .try_to_vec()
                .unwrap(),
        },
        &[
            reserve.clone(),
            escrow_account.clone(),
            user.clone(),
            sys_prog_account.clone(),
        ],
    )?;
    
    // TODO

    Ok(())
}
