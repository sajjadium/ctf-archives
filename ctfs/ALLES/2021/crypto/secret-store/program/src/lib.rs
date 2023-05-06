use borsh::{BorshDeserialize, BorshSerialize};
use solana_program::{entrypoint};

/// General information about a single bank
#[derive(Debug, BorshSerialize, BorshDeserialize)]
pub struct Store {
    // simple secret
    pub secret: u64,
}
pub const STORE_LEN: u64 = 8;

/// Instructions that this program supports
#[derive(Debug, BorshDeserialize, BorshSerialize)]
pub enum StoreInstruction {
    /// Initialize the Store
    ///
    /// To protect from scams, only a single bank is supported.
    /// Thus, the address of the bank account must be the program-derived address with empty seed.
    ///
    /// Passed accounts:
    ///
    /// (1) Store account
    /// (2) Flag account, pays for creation of secret account (must sign)
    /// (3) Rent sysvar
    Initialize { secret: u64 },
    /// Get the Flag
    ///
    /// Gives you flag if you give secret :)
    ///
    /// Passed accounts:
    ///
    /// (1) Store account
    GetFlag { secret: u64 },
}

pub mod processor;

use processor::process_instruction;
entrypoint!(process_instruction);
