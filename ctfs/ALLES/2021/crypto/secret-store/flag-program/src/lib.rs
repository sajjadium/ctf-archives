use std::{env, str::FromStr};

use solana_sdk::{
    account::ReadableAccount, ic_msg, instruction::InstructionError,
    keyed_account::keyed_account_at_index, process_instruction::InvokeContext, pubkey::Pubkey,
};
use spl_token::solana_program::program_pack::Pack;

fn assert_eq<T: Eq>(t1: T, t2: T) -> Result<(), InstructionError> {
    if t1 != t2 {
        Err(InstructionError::InvalidArgument)
    } else {
        Ok(())
    }
}

/// Accounts:
/// - flag_account: spl-token account containing at least one flag token
/// - flag_account_owner: owner of the previous account. must sign.
#[no_mangle]
extern "C" fn flagloader_program(
    _program_id: &Pubkey,
    _instruction_data: &[u8],
    ctx: &dyn InvokeContext,
) -> Result<(), InstructionError> {
    let keyed_accounts = ctx.get_keyed_accounts()?;
    let keyed_account = keyed_account_at_index(keyed_accounts, 0)?;
    let keyed_account_owner = keyed_account_at_index(keyed_accounts, 1)?;

    
    let flag_mint = Pubkey::from_str("F1agMint11111111111111111111111111111111111")?;
    let flag = env::var("FLAG").map_err(|_| InstructionError::GenericError)?;

    
    assert_eq(keyed_account.owner()?, spl_token::ID)?;

    let account = spl_token::state::Account::unpack(
        keyed_account
            .account
            .try_borrow()
            .map_err(|_| InstructionError::GenericError)?
            .data(),
    )
    .map_err(|_| InstructionError::GenericError)?;

    assert_eq(account.mint, flag_mint)?;

    if account.amount == 0 {
        return Err(InstructionError::InsufficientFunds);
    }

    assert_eq(
        Some(account.owner).as_ref(),
        keyed_account_owner.signer_key(),
    )?;
    

    ic_msg!(ctx, flag.as_str());
    
    Ok(())
}
