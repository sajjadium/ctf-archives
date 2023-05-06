mod entrypoint;
mod processor;

use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_program,
};

pub const BASE_PRICE: u64 = 200;
pub const LOSS_RATIO: u64 = 80;
pub const MAX_CHARACTERS: u64 = 10;

#[derive(BorshSerialize, BorshDeserialize)]
pub enum GachaInstruction {
    CreateUserAccount {
        account_name: String,
        account_bump: u8,
    },
    BuyPrimos {
        amount: u64,
        vault_bump: u8,
    },
    BuyCharacter {
        character_id: u8,
        character_bump: u8,
        vault_bump: u8,
    },
    SellAccount {
        vault_bump: u8,
    },
}

#[derive(BorshSerialize, BorshDeserialize)]
pub struct UserAccount {
    pub primos: u64,
    pub characters: Vec<u8>,
    pub owner: Pubkey,
}

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct Character {
    pub stars: u64,
    pub name: String,
    pub id: u8,
    pub owner: Pubkey,
}

pub fn get_useraccount(program: Pubkey, user: Pubkey, name: &str) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"ACCOUNT", &user.to_bytes(), name.as_bytes()], &program)
}

pub fn get_character(program: Pubkey, useraccount: Pubkey, character_id: u8) -> (Pubkey, u8) {
    Pubkey::find_program_address(
        &[b"CHARACTER", &useraccount.to_bytes(), &[character_id]],
        &program,
    )
}

pub fn get_vault(program: Pubkey) -> (Pubkey, u8) {
    Pubkey::find_program_address(&[b"VAULT"], &program)
}

pub fn create_useraccount(program: Pubkey, user: Pubkey, account_name: &str) -> Instruction {
    let (useraccount, useraccount_bump) = get_useraccount(program, user, &account_name);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(useraccount, false),
            AccountMeta::new(user, true),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: GachaInstruction::CreateUserAccount {
            account_name: account_name.to_string(),
            account_bump: useraccount_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}

pub fn buy_primos(program: Pubkey, user: Pubkey, account_name: &str, amount: u64) -> Instruction {
    let (useraccount, _) = get_useraccount(program, user, &account_name);
    let (vault, vault_bump) = get_vault(program);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(useraccount, false),
            AccountMeta::new(user, true),
            AccountMeta::new(vault, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: GachaInstruction::BuyPrimos { amount, vault_bump }
            .try_to_vec()
            .unwrap(),
    }
}

pub fn buy_character(
    program: Pubkey,
    user: Pubkey,
    account_name: &str,
    character_id: u8,
) -> Instruction {
    let (useraccount, _) = get_useraccount(program, user, account_name);
    let (character, character_bump) = get_character(program, useraccount, character_id);
    let (vault, vault_bump) = get_vault(program);
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(useraccount, false),
            AccountMeta::new(user, true),
            AccountMeta::new(character, false),
            AccountMeta::new(vault, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: GachaInstruction::BuyCharacter {
            character_id,
            character_bump,
            vault_bump,
        }
        .try_to_vec()
        .unwrap(),
    }
}

pub fn sell_account(
    program: Pubkey,
    user: Pubkey,
    account_name: &str,
    characters: &[u8],
) -> Instruction {
    let (useraccount, _) = get_useraccount(program, user, account_name);
    let (vault, vault_bump) = get_vault(program);

    let mut accounts = vec![
        AccountMeta::new(useraccount, false),
        AccountMeta::new(user, true),
        AccountMeta::new(vault, false),
    ];

    for &c in characters {
        let (character, _) = get_character(program, useraccount, c);
        accounts.push(AccountMeta::new(character, false));
    }

    accounts.push(AccountMeta::new_readonly(system_program::id(), false));

    Instruction {
        program_id: program,
        accounts: accounts,
        data: GachaInstruction::SellAccount { vault_bump }
            .try_to_vec()
            .unwrap(),
    }
}
