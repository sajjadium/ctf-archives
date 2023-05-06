use borsh::{BorshDeserialize, BorshSerialize};
use std::collections::HashSet;

use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint::ProgramResult,
    program::{invoke, invoke_signed},
    pubkey::Pubkey,
    system_instruction, msg,
};

use crate::{Character, GachaInstruction, UserAccount, BASE_PRICE, LOSS_RATIO};

struct CharacterInfo {
    stars: u8,
    name: &'static str,
}

#[rustfmt::skip]
const CHARACTERS: &'static [CharacterInfo] = &[
    CharacterInfo { stars: 4, name: "Amber" },
    CharacterInfo { stars: 4, name: "Chongyun" },
    CharacterInfo { stars: 4, name: "Fischl" },
    CharacterInfo { stars: 4, name: "Collei" },
    CharacterInfo { stars: 4, name: "Dori" },
    CharacterInfo { stars: 5, name: "Tartaglia" },
    CharacterInfo { stars: 5, name: "Xiao" },
    CharacterInfo { stars: 5, name: "Yae Miko" },
    CharacterInfo { stars: 5, name: "Diluc" },
    CharacterInfo { stars: 5, name: "Qiqi" },
];

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    mut instruction_data: &[u8],
) -> ProgramResult {
    match GachaInstruction::deserialize(&mut instruction_data)? {
        GachaInstruction::CreateUserAccount {
            account_name,
            account_bump,
        } => create_useraccount(program_id, accounts, &account_name, account_bump),
        GachaInstruction::BuyPrimos { amount, vault_bump } => {
            buy_primos(program_id, accounts, amount, vault_bump)
        }
        GachaInstruction::BuyCharacter {
            character_id,
            character_bump,
            vault_bump,
        } => buy_character(
            program_id,
            accounts,
            character_id,
            character_bump,
            vault_bump,
        ),
        GachaInstruction::SellAccount { vault_bump } => {
            sell_account(program_id, accounts, vault_bump)
        }
    }
}

fn create_useraccount(
    program: &Pubkey,
    accounts: &[AccountInfo],
    account_name: &str,
    account_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let useraccount_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;

    let useraccount_address = Pubkey::create_program_address(
        &[
            b"ACCOUNT",
            &user_info.key.to_bytes(),
            &account_name.as_bytes(),
            &[account_bump],
        ],
        program,
    )?;

    assert_eq!(*useraccount_info.key, useraccount_address);
    assert!(useraccount_info.data_is_empty());
    assert!(user_info.is_signer);

    // probably good enough /shrug
    const ACCOUNT_SIZE: u64 = 512;

    invoke_signed(
        &system_instruction::create_account(
            user_info.key,
            useraccount_info.key,
            10,
            ACCOUNT_SIZE,
            program,
        ),
        &[user_info.clone(), useraccount_info.clone()],
        &[&[
            b"ACCOUNT",
            &user_info.key.to_bytes(),
            &account_name.as_bytes(),
            &[account_bump],
        ]],
    )?;

    let new_account = UserAccount {
        primos: 0,
        characters: Vec::new(),
        owner: *user_info.key,
    };

    new_account.serialize(&mut &mut useraccount_info.data.borrow_mut()[..])?;

    Ok(())
}

fn buy_primos(
    program: &Pubkey,
    accounts: &[AccountInfo],
    amount: u64,
    vault_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let useraccount_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let vault_info = next_account_info(account_iter)?;
    let mut useraccount = UserAccount::deserialize(&mut &useraccount_info.data.borrow()[..])?;

    let vault_address = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], program)?;

    assert_eq!(*vault_info.key, vault_address);
    assert_eq!(useraccount_info.owner, program);
    assert_eq!(vault_info.owner, program);

    // no need to check account owner, since we can let users buy primos for each other
    assert!(user_info.is_signer);

    // 1:1 ratio between lamports:primos
    invoke(
        &system_instruction::transfer(user_info.key, vault_info.key, amount),
        &[user_info.clone(), vault_info.clone()],
    )?;

    useraccount.primos += amount;
    useraccount.serialize(&mut &mut useraccount_info.data.borrow_mut()[..])?;

    Ok(())
}

fn buy_character(
    program: &Pubkey,
    accounts: &[AccountInfo],
    character_id: u8,
    character_bump: u8,
    vault_bump: u8,
) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let useraccount_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let character_info = next_account_info(account_iter)?;
    let vault_info = next_account_info(account_iter)?;
    let mut useraccount = UserAccount::deserialize(&mut &useraccount_info.data.borrow()[..])?;

    let character_address = Pubkey::create_program_address(
        &[
            b"CHARACTER",
            &useraccount_info.key.to_bytes(),
            &[character_id],
            &[character_bump],
        ],
        program,
    )?;

    msg!("{}", character_address);

    let vault_address = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], program)?;

    assert_eq!(*character_info.key, character_address);
    assert_eq!(*vault_info.key, vault_address);
    assert_eq!(useraccount_info.owner, program);
    assert_eq!(vault_info.owner, program);
    assert!(character_info.data_is_empty());

    assert!(user_info.is_signer);
    assert_eq!(useraccount.owner, *user_info.key);

    // prevent buying the same character twice
    for &c in &useraccount.characters {
        assert_ne!(character_id, c);
    }

    let stats = &CHARACTERS[character_id as usize];
    let character = Character {
        id: character_id,
        stars: stats.stars as u64,
        name: stats.name.to_string(),
        owner: *useraccount_info.key,
    };

    let price = (character.stars as u64) * BASE_PRICE;
    assert!(useraccount.primos >= price);

    // probably good enough /shrug
    const CHARACTER_SIZE: u64 = 128;

    invoke_signed(
        &system_instruction::create_account(
            user_info.key,
            character_info.key,
            10,
            CHARACTER_SIZE,
            program,
        ),
        &[user_info.clone(), character_info.clone()],
        &[&[
            b"CHARACTER",
            &useraccount_info.key.to_bytes(),
            &[character_id],
            &[character_bump],
        ]],
    )?;

    useraccount.primos -= price;
    useraccount.characters.push(character_id);

    useraccount.serialize(&mut &mut useraccount_info.data.borrow_mut()[..])?;
    character.serialize(&mut &mut character_info.data.borrow_mut()[..])?;

    Ok(())
}

// monkaTOS
fn sell_account(program: &Pubkey, accounts: &[AccountInfo], vault_bump: u8) -> ProgramResult {
    let account_iter = &mut accounts.iter();
    let useraccount_info = next_account_info(account_iter)?;
    let user_info = next_account_info(account_iter)?;
    let vault_info = next_account_info(account_iter)?;

    // further accounts passed are all the characters that the user owns

    let mut useraccount = UserAccount::deserialize(&mut &useraccount_info.data.borrow()[..])?;

    let vault_address = Pubkey::create_program_address(&[b"VAULT", &[vault_bump]], program)?;

    assert_eq!(*vault_info.key, vault_address);
    assert_eq!(useraccount_info.owner, program);
    assert_eq!(vault_info.owner, program);

    assert!(user_info.is_signer);
    assert_eq!(useraccount.owner, *user_info.key);

    let mut price = 0;
    let mut sold = HashSet::new();
    for character_info in account_iter.take(useraccount.characters.len()) {
        let character = Character::deserialize(&mut &character_info.data.borrow()[..])?;

        assert_eq!(character_info.owner, program);
        assert_eq!(character.owner, *useraccount_info.key);

        // haha nice try
        assert!(!sold.contains(&character.id));

        price += (character.stars as u64 * BASE_PRICE * LOSS_RATIO) / 100;
        sold.insert(character.id);
    }

    **vault_info.lamports.borrow_mut() -= price;
    **user_info.lamports.borrow_mut() += price;

    useraccount.owner = *program;
    useraccount.serialize(&mut &mut useraccount_info.data.borrow_mut()[..])?;

    Ok(())
}
