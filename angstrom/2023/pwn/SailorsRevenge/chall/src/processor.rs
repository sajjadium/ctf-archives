use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    msg,
    program::invoke_signed,
    program_error::ProgramError,
    pubkey::Pubkey,
    system_instruction, system_program,
    sysvar::rent::Rent,
    sysvar::Sysvar,
};

#[derive(Debug, Clone, BorshDeserialize, PartialEq, Eq, PartialOrd, Ord)]
pub enum SailorInstruction {
    CreateUnion(u64),
    PayDues(u64),
    StrikePay(u64),
    RegisterMember([u8; 32]),
}

#[derive(Debug, Clone, BorshSerialize, BorshDeserialize, PartialEq, Eq, PartialOrd, Ord)]
pub struct SailorUnion {
    available_funds: u64,
    authority: [u8; 32],
}

#[derive(Debug, Clone, BorshSerialize, BorshDeserialize, PartialEq, Eq, PartialOrd, Ord)]
pub struct Registration {
    balance: i64,
    member: [u8; 32],
}

fn transfer<'a>(
    from: &AccountInfo<'a>,
    to: &AccountInfo<'a>,
    amt: u64,
    signers: &[&[&[u8]]],
) -> ProgramResult {
    if from.lamports() >= amt {
        invoke_signed(
            &system_instruction::transfer(from.key, to.key, amt),
            &[from.clone(), to.clone()],
            signers,
        )?;
    }
    Ok(())
}

pub fn create_union(program_id: &Pubkey, accounts: &[AccountInfo], bal: u64) -> ProgramResult {
    msg!("creating union {}", bal);

    let iter = &mut accounts.iter();

    let sailor_union = next_account_info(iter)?;
    assert!(!sailor_union.is_signer);
    assert!(sailor_union.is_writable);

    let authority = next_account_info(iter)?;
    assert!(authority.is_signer);
    assert!(authority.is_writable);
    assert!(authority.owner == &system_program::ID);

    let (sailor_union_addr, sailor_union_bump) =
        Pubkey::find_program_address(&[b"union", authority.key.as_ref()], program_id);
    assert!(sailor_union.key == &sailor_union_addr);

    let (vault_addr, _) = Pubkey::find_program_address(&[b"vault"], program_id);
    let vault = next_account_info(iter)?;
    assert!(!vault.is_signer);
    assert!(vault.is_writable);
    assert!(vault.owner == &system_program::ID);
    assert!(vault.key == &vault_addr);

    let system = next_account_info(iter)?;
    assert!(system.key == &system_program::ID);

    if authority.lamports() >= bal {
        transfer(&authority, &vault, bal, &[])?;
        let data = SailorUnion {
            available_funds: 0,
            authority: authority.key.to_bytes(),
        };
        let ser_data = data.try_to_vec()?;

        invoke_signed(
            &system_instruction::create_account(
                &authority.key,
                &sailor_union_addr,
                Rent::get()?.minimum_balance(ser_data.len()),
                ser_data.len() as u64,
                program_id,
            ),
            &[authority.clone(), sailor_union.clone()],
            &[&[b"union", authority.key.as_ref(), &[sailor_union_bump]]],
        )?;

        sailor_union.data.borrow_mut().copy_from_slice(&ser_data);
        Ok(())
    } else {
        msg!(
            "insufficient funds, have {} but need {}",
            authority.lamports(),
            bal
        );
        Err(ProgramError::InsufficientFunds)
    }
}

pub fn pay_dues(program_id: &Pubkey, accounts: &[AccountInfo], amt: u64) -> ProgramResult {
    msg!("paying dues {}", amt);

    let iter = &mut accounts.iter();

    let sailor_union = next_account_info(iter)?;
    assert!(!sailor_union.is_signer);
    assert!(sailor_union.is_writable);
    assert!(sailor_union.owner == program_id);

    let member = next_account_info(iter)?;
    assert!(member.is_signer);
    assert!(member.is_writable);
    assert!(member.owner == &system_program::ID);

    let (vault_addr, _) = Pubkey::find_program_address(&[b"vault"], program_id);
    let vault = next_account_info(iter)?;
    assert!(!vault.is_signer);
    assert!(vault.is_writable);
    assert!(vault.owner == &system_program::ID);
    assert!(vault.key == &vault_addr);

    let system = next_account_info(iter)?;
    assert!(system.key == &system_program::ID);

    if member.lamports() >= amt {
        let mut data = SailorUnion::try_from_slice(&sailor_union.data.borrow())?;
        data.available_funds += amt;
        data.serialize(&mut &mut *sailor_union.data.borrow_mut())?;
        transfer(&member, &vault, amt, &[])?;
        Ok(())
    } else {
        msg!(
            "insufficient funds, have {} but need {}",
            member.lamports(),
            amt
        );
        Err(ProgramError::InsufficientFunds)
    }
}

pub fn strike_pay(program_id: &Pubkey, accounts: &[AccountInfo], amt: u64) -> ProgramResult {
    msg!("strike pay {}", amt);

    let iter = &mut accounts.iter();

    let sailor_union = next_account_info(iter)?;
    assert!(!sailor_union.is_signer);
    assert!(sailor_union.is_writable);
    assert!(sailor_union.owner == program_id);

    let member = next_account_info(iter)?;
    assert!(member.is_writable);
    assert!(member.owner == &system_program::ID);

    let authority = next_account_info(iter)?;
    assert!(authority.is_signer);
    assert!(authority.owner == &system_program::ID);

    let (vault_addr, vault_bump) = Pubkey::find_program_address(&[b"vault"], program_id);
    let vault = next_account_info(iter)?;
    assert!(!vault.is_signer);
    assert!(vault.is_writable);
    assert!(vault.owner == &system_program::ID);
    assert!(vault.key == &vault_addr);

    let system = next_account_info(iter)?;
    assert!(system.key == &system_program::ID);

    let mut data = SailorUnion::try_from_slice(&sailor_union.data.borrow())?;
    assert!(&data.authority == authority.key.as_ref());

    if data.available_funds >= amt {
        data.available_funds -= amt;
        transfer(&vault, &member, amt, &[&[b"vault", &[vault_bump]]])?;
        data.serialize(&mut &mut *sailor_union.data.borrow_mut())?;
        Ok(())
    } else {
        msg!(
            "insufficient funds, have {} but need {}",
            data.available_funds,
            amt
        );
        Err(ProgramError::InsufficientFunds)
    }
}

pub fn register_member(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    member: [u8; 32],
) -> ProgramResult {
    msg!("register member {:?}", member);

    let iter = &mut accounts.iter();

    let registration = next_account_info(iter)?;
    assert!(!registration.is_signer);
    assert!(registration.is_writable);

    let sailor_union = next_account_info(iter)?;
    assert!(!sailor_union.is_signer);
    assert!(!sailor_union.is_writable);
    assert!(sailor_union.owner == program_id);

    let authority = next_account_info(iter)?;
    assert!(authority.is_signer);
    assert!(authority.is_writable);
    assert!(authority.owner == &system_program::ID);

    let (registration_addr, registration_bump) = Pubkey::find_program_address(
        &[
            b"registration",
            authority.key.as_ref(),
            &member,
        ],
        program_id,
    );
    assert!(registration.key == &registration_addr);

    let system = next_account_info(iter)?;
    assert!(system.key == &system_program::ID);

    let data = SailorUnion::try_from_slice(&sailor_union.data.borrow())?;
    assert!(&data.authority == authority.key.as_ref());

    let ser_data = Registration {
        balance: -100,
        member,
        // sailor_union: sailor_union.key.to_bytes(),
    }
    .try_to_vec()?;

    invoke_signed(
        &system_instruction::create_account(
            &authority.key,
            &registration_addr,
            Rent::get()?.minimum_balance(ser_data.len()),
            ser_data.len() as u64,
            program_id,
        ),
        &[authority.clone(), registration.clone()],
        &[&[
            b"registration",
            authority.key.as_ref(),
            &member,
            &[registration_bump],
        ]],
    )?;

    registration.data.borrow_mut().copy_from_slice(&ser_data);

    Ok(())
}
