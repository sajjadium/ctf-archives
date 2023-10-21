use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::pubkey::Pubkey;

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize, PartialEq, Debug, Clone)]
pub struct Pool {
    /// Withdrawal fee in basis points
    pub withdrawal_fee: u64,
    /// LP token mint
    pub lp_token_mint: Pubkey,
}

impl Pool {
    pub const SEED_PREFIX: &'static str = "POOOOOOL";
    pub const LEN: usize = 0x2000; // I'm too lazy to calculate this
}

#[repr(C)]
#[derive(BorshSerialize, BorshDeserialize, PartialEq, Debug, Clone)]
pub struct DepositRecord {
    /// Deposit amount
    pub amount: u64,
    /// LP token amount
    pub lp_token_amount: u64,
    /// Pool address
    pub pool: Pubkey,
    /// User address
    pub user: Pubkey,
}

impl DepositRecord {
    pub const SEED_PREFIX: &'static str = "RECOOORD";
    pub const LEN: usize = 0x2000; // I'm too lazy to calculate this
}