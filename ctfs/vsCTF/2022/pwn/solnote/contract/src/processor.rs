use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    pubkey::Pubkey,
    system_instruction,
};

use crate::{Note, NoteInstruction, NotePad, BUY_PRICE, DEFAULT_FEE, MAX_NOTE_SIZE, SELL_PRICE };

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    mut instruction_data: &[u8],
) -> ProgramResult {
    match NoteInstruction::deserialize(&mut instruction_data)? {
        NoteInstruction::CreatePad { pad_bump } => create_pad(program_id, accounts, pad_bump),
        NoteInstruction::AddNote {
            note_seed,
            note_bump,
        } => add_note(program_id, accounts, note_seed, note_bump),
        NoteInstruction::BuyNote { vault_bump } => buy_note(program_id, accounts, vault_bump),
        NoteInstruction::SellNote { vault_bump } => sell_note(program_id, accounts, vault_bump),
        NoteInstruction::EditNote { contents } => edit_note(program_id, accounts, contents),
    }
}

fn create_pad(program: &Pubkey, accounts: &[AccountInfo], pad_bump: u8) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let pad_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;

    let pad_address =
        Pubkey::create_program_address(&[b"PAD", &user_info.key.to_bytes(), &[pad_bump]], program)?;

    assert_eq!(*pad_info.key, pad_address);
    assert!(pad_info.data_is_empty());
    assert!(user_info.is_signer);

    // good enough!
    const PAD_SIZE: u64 = 64;

    invoke_signed(
        &system_instruction::create_account(user_info.key, pad_info.key, 5, PAD_SIZE, program),
        &[user_info.clone(), pad_info.clone()],
        &[&[b"PAD", &user_info.key.to_bytes(), &[pad_bump]]],
    )?;

    let pad = NotePad {
        royalty: DEFAULT_FEE,
        owner: *user_info.key,
    };

    pad.serialize(&mut &mut pad_info.data.borrow_mut()[..])?;

    Ok(())
}

fn add_note(
    program: &Pubkey,
    accounts: &[AccountInfo],
    note_seed: Vec<u8>,
    note_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let pad_info = next_account_info(account_iter)?;
    let note_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let pad = NotePad::deserialize(&mut &pad_info.data.borrow_mut()[..])?;

    let note_address = Pubkey::create_program_address(
        &[b"NOTE", &pad_info.key.to_bytes(), &note_seed, &[note_bump]],
        program,
    )?;

    assert_eq!(*note_info.key, note_address);
    assert_eq!(pad_info.owner, program);
    assert!(note_info.data_is_empty());

    // only the pad owner can add notes to their pad
    assert_eq!(pad.owner, *user_info.key);
    assert!(user_info.is_signer);

    invoke_signed(
        &system_instruction::create_account(user_info.key, note_info.key, 10, MAX_NOTE_SIZE, program),
        &[user_info.clone(), note_info.clone()],
        &[&[b"NOTE", &pad_info.key.to_bytes(), &note_seed, &[note_bump]]],
    )?;

    // notes start off "owned" by the pad before they're bought by a user
    // this lets us determine whether a note is owned without special cases
    let note_data = Note {
        contents: String::new(),
        writer: *pad_info.key,
        pad: *pad_info.key,
    };

    note_data.serialize(&mut &mut note_info.data.borrow_mut()[..])?;
    pad.serialize(&mut &mut pad_info.data.borrow_mut()[..])?;

    Ok(())
}

fn buy_note(program: &Pubkey, accounts: &[AccountInfo], vault_bump: u8) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let pad_info = next_account_info(account_iter)?;
    let note_info = next_account_info(account_iter)?;
    let vault_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let pad_owner_info = next_account_info(account_iter)?;
    let pad = NotePad::deserialize(&mut &pad_info.data.borrow_mut()[..])?;
    let mut note = Note::deserialize(&mut &note_info.data.borrow_mut()[..])?;

    let vault_address = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], program)?;

    assert_eq!(*vault_info.key, vault_address);
    assert_eq!(pad_info.owner, program);
    assert_eq!(note_info.owner, program);
    assert_eq!(vault_info.owner, program);

    assert_eq!(pad.owner, *pad_owner_info.key);

    assert!(user_info.is_signer);

    // make sure the note belongs to the pad
    assert_eq!(note.pad, *pad_info.key);

    // make sure note is unowned
    assert_eq!(note.writer, *pad_info.key);

    note.writer = *user_info.key;

    // transfer full note cost to vault first
    invoke(
        &system_instruction::transfer(user_info.key, vault_info.key, BUY_PRICE),
        &[user_info.clone(), vault_info.clone()],
    )?;

    // calculate royalty fee and transfer from vault to the jar owner
    let tip = pad.royalty * BUY_PRICE / 100;
    **vault_info.lamports.borrow_mut() -= tip;
    **pad_owner_info.lamports.borrow_mut() += tip;

    pad.serialize(&mut &mut pad_info.data.borrow_mut()[..])?;
    note.serialize(&mut &mut note_info.data.borrow_mut()[..])?;

    Ok(())
}

// basically the same as write except the other way around
fn sell_note(program: &Pubkey, accounts: &[AccountInfo], vault_bump: u8) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let pad_info = next_account_info(account_iter)?;
    let note_info = next_account_info(account_iter)?;
    let vault_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let pad_owner_info = next_account_info(account_iter)?;
    let pad = NotePad::deserialize(&mut &pad_info.data.borrow_mut()[..])?;
    let mut note = Note::deserialize(&mut &note_info.data.borrow_mut()[..])?;

    let vault_address = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], program)?;

    assert_eq!(*vault_info.key, vault_address);
    assert_eq!(pad_info.owner, program);
    assert_eq!(note_info.owner, program);
    assert_eq!(vault_info.owner, program);

    assert_eq!(pad.owner, *pad_owner_info.key);

    assert!(user_info.is_signer);

    // make sure the note belongs to the pad
    assert_eq!(note.pad, *pad_info.key);

    // make sure note is actually owned by user
    assert_eq!(note.writer, *user_info.key);
    note.writer = *pad_info.key;

    // transfer sell price to user
    // the pad owner's royalty fee is not refunded
    **vault_info.lamports.borrow_mut() -= SELL_PRICE;
    **user_info.lamports.borrow_mut() += SELL_PRICE;

    pad.serialize(&mut &mut pad_info.data.borrow_mut()[..])?;
    note.serialize(&mut &mut note_info.data.borrow_mut()[..])?;

    Ok(())
}

fn edit_note(program: &Pubkey, accounts: &[AccountInfo], contents: String) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let note_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let mut note = Note::deserialize(&mut &note_info.data.borrow_mut()[..])?;

    assert_eq!(note_info.owner, program);
    assert_eq!(note.writer, *user_info.key);

    assert!(user_info.is_signer);

    // we confirmed user owns this note, so we can now write their contents to it
    note.contents = contents;
    note.serialize(&mut &mut note_info.data.borrow_mut()[..])?;

    Ok(())
}