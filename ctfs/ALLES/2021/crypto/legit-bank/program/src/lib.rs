use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{clock::UnixTimestamp, entrypoint};

/// General information about a single bank
#[derive(Debug, BorshSerialize, BorshDeserialize)]
pub struct Bank {
    /// manager may withdraw user funds to invest them
    pub manager_key: [u8; 32],

    /// address of the token vault (program-derived key)
    pub vault_key: [u8; 32],

    /// address of the token vault authority (program-derived key)
    pub vault_authority: [u8; 32],

    /// seed for the vault authority
    pub vault_authority_seed: u8,

    /// percentage of total deposits that must be held as reserve in the vault at all times
    pub reserve_rate: u8,

    /// total amount of deposits
    pub total_deposit: u64,
}
pub const BANK_LEN: u64 = 106;

pub const DEFAULT_INTEREST_RATE: u8 = 1;

/// State for each user who holds funds in a bank account
#[derive(Debug, BorshDeserialize, BorshSerialize)]
pub struct UserAccount {
    /// current account balance
    pub balance: u64,

    /// in percent per year (effective)
    pub interest_rate: u8,

    /// last unix time at which interest was paid out
    pub interest_paid_time: UnixTimestamp,
}

pub const USER_ACCOUNT_LEN: u64 = 10;
pub const SECONDS_PER_YEAR: u64 = 60 * 60 * 24 * 365;

impl UserAccount {
    pub fn pay_interest(&mut self, current_time: UnixTimestamp) -> u64 {
        let passed_seconds = current_time - self.interest_paid_time;

        let effective_interest_rate = (1.0 + self.interest_rate as f32 / 100.0)
            * (passed_seconds as f32 / SECONDS_PER_YEAR as f32);
        let new_balance = ((self.balance as f32) * effective_interest_rate as f32) as u64;
        let interest = new_balance - self.balance;

        self.balance = new_balance;
        self.interest_paid_time = current_time;

        interest
    }
}

/// Instructions that this program supports
#[derive(Debug, BorshDeserialize, BorshSerialize)]
pub enum BankInstruction {
    /// Initialize the bank
    ///
    /// To protect from scams, only a single bank is supported.
    /// Thus, the address of the bank account must be the program-derived address with empty seed.
    ///
    /// Passed accounts:
    ///
    /// (1) Bank account
    /// (2) Manager's account, pays for creation of bank account (must sign)
    /// (3) Vault account
    /// (4) Vault authority
    /// (5) Mint
    /// (6) Rent sysvar
    /// (7) System program
    /// (8) spl-token program
    Initialize { reserve_rate: u8 },

    /// Open a new user account with the bank
    ///
    /// Passed accounts:
    ///
    /// (1) User account to open
    /// (2) Withdrawer account (a signature from this account is required for withdraw)
    /// (3) System program
    ///
    /// The withdrawer account needs enough SOL to pay for the rent of the new account, and must sign the transaction
    /// to open the account.
    Open,

    /// Transfer money into bank account
    ///
    /// Passed accounts:
    ///
    /// (1) Bank account
    /// (2) Vault account
    /// (3) User account for deposit
    /// (4) Source token account to transfer money from
    /// (5) Source token account authority (must sign)
    /// (6) spl-token program
    /// (7) Solana Clock sysvar
    Deposit { amount: u64 },

    /// Withdraw money from bank account
    ///
    /// Passed accounts:
    ///
    /// (1) Bank account
    /// (2) Vault account
    /// (3) Vault authority account
    /// (4) User account to withdraw from
    /// (5) Token account where withdrawed money will be transfered to
    /// (6) Withdrawer account. Must sign and match the withdrawer specified when the account was opened.
    /// (7) spl-token program
    /// (8) Solana Clock sysvar
    Withdraw { amount: u64 },

    /// (Manager only) take money for investing
    ///
    /// The manager should transfer the invested money back into the vault
    /// if the vault runs low. This function ensures that there at least
    /// the percentage given by reserve_rate remains in the vault.
    ///
    /// Passed accounts:
    ///
    /// (1) Bank account
    /// (2) Vault account
    /// (3) Vault authority account
    /// (4) Destination token account
    /// (5) Manager's account (requires signature)
    /// (6) SPL token program
    Invest { amount: u64 },
}

pub mod processor;

use processor::process_instruction;
entrypoint!(process_instruction);
