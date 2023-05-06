mod entrypoint;
pub mod processor;

use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_program,
};

pub const MAX_NOTE_SIZE: u64 = 512;
pub const BUY_PRICE: u64 = 100;
pub const SELL_PRICE: u64 = 50;
pub const DEFAULT_FEE: u64 = 15;

#[derive(BorshSerialize, BorshDeserialize)]
pub enum NoteInstruction {
    CreatePad { pad_bump: u8 },
    AddNote { note_seed: Vec<u8>, note_bump: u8 },
    BuyNote { vault_bump: u8 },
    SellNote { vault_bump: u8 },
    EditNote { contents: String },
}

#[derive(BorshSerialize, BorshDeserialize)]
pub struct NotePad {
    // credit the pad owner with a portion of profits
    // no floating point due to **imprecision**
    pub royalty: u64,
    pub owner: Pubkey,
}

#[derive(BorshSerialize, BorshDeserialize)]
pub struct Note {
    pub contents: String,

    pub writer: Pubkey,
    pub pad: Pubkey,
}

pub fn get_note(program: Pubkey, pad: Pubkey, seed: &[u8]) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"NOTE", &pad.to_bytes(), seed], &program)
}

pub fn get_pad(program: Pubkey, user: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"PAD", &user.to_bytes()], &program)
}

pub fn get_vault(program: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"VAULT"], &program)
}

pub fn create_pad(program: Pubkey, user: Pubkey) -> Instruction {
    let (pad, pad_bump) = get_pad(program, user);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(pad, false),
            AccountMeta::new(user, true),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: NoteInstruction::CreatePad {
            pad_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}

pub fn add_note(program: Pubkey, pad_owner: Pubkey, note_seed: Vec<u8>) -> Instruction {
    let (pad, _) = get_pad(program, pad_owner);
    let (note, note_bump) = get_note(program, pad, &note_seed);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(pad, false),
            AccountMeta::new(note, false),
            AccountMeta::new(pad_owner, true),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: NoteInstruction::AddNote {
            note_seed,
            note_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}

pub fn buy_note(
    program: Pubkey,
    pad_owner: Pubkey,
    user: Pubkey,
    note_seed: Vec<u8>,
) -> Instruction {
    let (pad, _) = get_pad(program, pad_owner);
    let (note, _) = get_note(program, pad, &note_seed);
    let (vault, vault_bump) = get_vault(program);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(pad, false),
            AccountMeta::new(note, false),
            AccountMeta::new(vault, false),
            AccountMeta::new(user, true),
            AccountMeta::new(pad_owner, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: NoteInstruction::BuyNote {
            vault_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}

pub fn sell_note(
    program: Pubkey,
    pad_owner: Pubkey,
    user: Pubkey,
    note_seed: Vec<u8>,
) -> Instruction {
    let (pad, _) = get_pad(program, pad_owner);
    let (note, _) = get_note(program, pad, &note_seed);
    let (vault, vault_bump) = get_vault(program);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(pad, false),
            AccountMeta::new(note, false),
            AccountMeta::new(vault, false),
            AccountMeta::new(user, true),
            AccountMeta::new(pad_owner, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: NoteInstruction::SellNote {
            vault_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}


pub fn edit_note(
    program: Pubkey,
    pad_owner: Pubkey,
    user: Pubkey,
    note_seed: Vec<u8>,
    contents: String,
) -> Instruction {
    let (pad, _) = get_pad(program, pad_owner);
    let (note, _) = get_note(program, pad, &note_seed);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(note, false),
            AccountMeta::new(user, true),
        ],
        data: NoteInstruction::EditNote {
            contents,
        }
        .try_to_vec()
        .unwrap(),
    }
}