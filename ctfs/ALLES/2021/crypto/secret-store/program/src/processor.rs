use arrayref::array_ref;
use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{account_info::AccountInfo, entrypoint::ProgramResult, program::{invoke, invoke_signed}, program_error::ProgramError, program_pack::Pack, pubkey::Pubkey, rent::Rent, system_instruction, sysvar::Sysvar};

use crate::{Store, StoreInstruction, STORE_LEN};

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    match StoreInstruction::try_from_slice(instruction_data)? {
        StoreInstruction::Initialize { secret } => initialize(program_id, accounts, secret),
        StoreInstruction::GetFlag { secret } => getflag(program_id, accounts, secret),
    }
}

/// See struct StoreInstruction for docs
fn initialize(program_id: &Pubkey, accounts: &[AccountInfo], secret: u64) -> ProgramResult {
    let [store_info, fee_payer, flag_depot, flag_depot_owner, rent_info, _system_program, token_program] =
        array_ref![accounts, 0, 7];

    let (store_address, store_seed) = Pubkey::find_program_address(&[], program_id);
    if *store_info.key != store_address {
        return Err(ProgramError::InvalidArgument);
    }

    if !flag_depot_owner.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }

    if store_info.data_len() == STORE_LEN as usize {
        //already initialized
        return Err(ProgramError::InvalidArgument);
    }

    if token_program.key != &spl_token::id() {
        return Err(ProgramError::InvalidArgument);
    }

    let ix = &spl_token::instruction::set_authority(
        token_program.key,
        flag_depot.key,
        Some(&store_address),
        spl_token::instruction::AuthorityType::AccountOwner,
        &flag_depot_owner.key,
        &[&flag_depot_owner.key],
    )?;

    invoke(
        &ix,
        &[
            flag_depot.clone(),
            flag_depot_owner.clone(),
            token_program.clone(),
        ],
    )?;

    let rent = Rent::from_account_info(rent_info)?;

    let store = Store { secret: secret };

    invoke_signed(
        &system_instruction::create_account(
            &fee_payer.key,
            &store_address,
            rent.minimum_balance(STORE_LEN as usize),
            STORE_LEN,
            &program_id,
        ),
        &[fee_payer.clone(), store_info.clone()],
        &[&[&[store_seed]]],
    )?;

    store
        .serialize(&mut &mut store_info.data.borrow_mut()[..])
        .unwrap();

    Ok(())
}

fn getflag(program_id: &Pubkey, accounts: &[AccountInfo], secret: u64) -> ProgramResult {
    let [store_info, flag_depot, user_account, token_program] = array_ref![accounts, 0, 4];
    let (store_address, store_seed) = Pubkey::find_program_address(&[], program_id);

    if *store_info.key != store_address {
        return Err(ProgramError::InvalidArgument);
    }
    
    let store = Store::try_from_slice(&store_info.data.borrow()).unwrap();

    if store.secret != secret {
        return Err(ProgramError::InvalidArgument);
    }

    if token_program.key != &spl_token::id() {
        return Err(ProgramError::InvalidArgument);
    }

    

    if *flag_depot.owner != spl_token::ID {
        return Err(ProgramError::InvalidArgument);
    }

    let account = spl_token::state::Account::unpack(
        &flag_depot.data.borrow(),
    )
    .map_err(|_| ProgramError::InvalidAccountData)?;

    if account.owner != *store_info.key {
        return Err(ProgramError::InvalidArgument);
    }

    let ix = &spl_token::instruction::set_authority(
        token_program.key,
        flag_depot.key,
        Some(user_account.key),
        spl_token::instruction::AuthorityType::AccountOwner,
        &store_info.key,
        &[&store_info.key],
    )?;

    invoke_signed(
        &ix,
        &[
            flag_depot.clone(),
            store_info.clone(),
            token_program.clone(),
        ],
        &[&[&[store_seed]]],
    )?;

    Ok(())
}
