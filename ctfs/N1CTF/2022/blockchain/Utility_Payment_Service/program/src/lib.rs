mod entrypoint;
pub mod processor;

use borsh::{BorshDeserialize, BorshSerialize};

use solana_program::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    system_program,
};

use std::mem::size_of;

#[derive(BorshDeserialize, BorshSerialize)]
pub enum ServiceInstruction {
    Init {},
    DepositEscrow { amount: u16 },
    WithdrawEscrow {},
    Pay { amount: u16 },
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize)]
pub struct Escrow {
    pub user: Pubkey,
    pub amount: u16,
    pub bump: u8,
}

pub const ESCROW_ACCOUNT_SIZE: usize = size_of::<Escrow>();

pub fn init(program: Pubkey, user: Pubkey, reserve: Pubkey, escrow_account: Pubkey) -> Instruction {
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(reserve, false),
            AccountMeta::new(escrow_account, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: ServiceInstruction::Init {}.try_to_vec().unwrap(),
    }
}

pub fn deposit_escrow(
    program: Pubkey,
    user: Pubkey,
    reserve: Pubkey,
    escrow_account: Pubkey,
    amount: u16,
) -> Instruction {
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(reserve, false),
            AccountMeta::new(escrow_account, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: ServiceInstruction::DepositEscrow { amount }
            .try_to_vec()
            .unwrap(),
    }
}

pub fn withdraw_escrow(
    program: Pubkey,
    user: Pubkey,
    reserve: Pubkey,
    escrow_account: Pubkey,
) -> Instruction {
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(reserve, false),
            AccountMeta::new(escrow_account, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: ServiceInstruction::WithdrawEscrow {}.try_to_vec().unwrap(),
    }
}

pub fn pay_utility_fees(
    program: Pubkey,
    user: Pubkey,
    reserve: Pubkey,
    escrow_account: Pubkey,
    amount: u16,
) -> Instruction {
    Instruction {
        program_id: program,
        accounts: vec![
            AccountMeta::new(user, true),
            AccountMeta::new(reserve, false),
            AccountMeta::new(escrow_account, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
        data: ServiceInstruction::Pay { amount }.try_to_vec().unwrap(),
    }
}
