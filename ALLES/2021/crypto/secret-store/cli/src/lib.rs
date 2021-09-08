use std::process;

use solana_core::test_validator::TestValidatorGenesis;
use solana_program::{clock::Epoch, program_pack::Pack};
use solana_sdk::{
    account::{Account, AccountSharedData},
    native_loader,
    native_token::sol_to_lamports,
    program_option::COption,
    pubkey::Pubkey,
    system_program,
};
use solana_streamer::socket::SocketAddrSpace;
use spl_associated_token_account::get_associated_token_address;
use spl_token::state::AccountState;

pub mod store_program {
    use solana_sdk::declare_id;
    declare_id!("Secret1111111111111111111111111111111111111");
}

pub mod flag_mint {
    use solana_program::declare_id;
    declare_id!("F1agMint11111111111111111111111111111111111");
}

pub mod flag_program {
    use solana_program::declare_id;
    declare_id!("F1ag111111111111111111111111111111111111111");
}

pub struct GenesisSetup {
    genesis: TestValidatorGenesis,
}

impl GenesisSetup {
    pub fn new() -> Self {
        let mut genesis = TestValidatorGenesis::default();
        genesis.ledger_path("ledger/");
        GenesisSetup { genesis }
    }

    #[allow(dead_code)]
    pub fn add_account_with_sol(&mut self, pubkey: Pubkey, sol: f64) -> &mut Self {
        self.genesis.add_account(
            pubkey,
            AccountSharedData::new(sol_to_lamports(sol), 0, &system_program::ID),
        );
        self
    }

    pub fn add_program(&mut self, pubkey: Pubkey, name: &str) -> &mut Self {
        self.genesis.add_program(name, pubkey);
        self
    }

    pub fn add_rent_excempt(&mut self, pubkey: Pubkey, data: Vec<u8>, owner: Pubkey) -> &mut Self {
        self.genesis.add_account(
            pubkey,
            AccountSharedData::from(Account {
                lamports: self.genesis.rent.minimum_balance(data.len()),
                data,
                owner,
                executable: false,
                rent_epoch: Epoch::default(),
            }),
        );
        self
    }

    pub fn add_rent_excempt_executable(
        &mut self,
        pubkey: Pubkey,
        data: Vec<u8>,
        owner: Pubkey,
    ) -> &mut Self {
        self.genesis.add_account(
            pubkey,
            AccountSharedData::from(Account {
                lamports: self.genesis.rent.minimum_balance(data.len()),
                data,
                owner,
                executable: true,
                rent_epoch: Epoch::default(),
            }),
        );
        self
    }

    pub fn add_packable_rent_excempt<P: Pack>(
        &mut self,
        pubkey: Pubkey,
        packable: P,
        owner: Pubkey,
    ) -> &mut Self {
        let mut data = vec![0u8; P::get_packed_len()];
        packable.pack_into_slice(&mut data);
        self.add_rent_excempt(pubkey, data, owner);
        self
    }

    #[allow(dead_code)]
    pub fn add_serializable_rent_excempt<S: borsh::BorshSerialize>(
        &mut self,
        pubkey: Pubkey,
        serializable: S,
        owner: Pubkey,
    ) -> &mut Self {
        let data = borsh::to_vec(&serializable).unwrap();
        self.add_rent_excempt(pubkey, data, owner);
        self
    }

    pub fn add_native_program(&mut self, pubkey: Pubkey, name: &str) -> &mut Self {
        let data = name.as_bytes().to_vec();
        self.add_rent_excempt_executable(pubkey, data, native_loader::ID);
        self
    }

    pub fn add_mint(&mut self, pubkey: Pubkey, supply: u64, decimals: u8) -> &mut Self {
        let mint = spl_token::state::Mint {
            mint_authority: COption::None,
            supply,
            decimals,
            is_initialized: true,
            freeze_authority: COption::None,
        };
        self.add_packable_rent_excempt(pubkey, mint, spl_token::ID);
        self
    }

    pub fn add_token_account(
        &mut self,
        pubkey: Pubkey,
        tokens: u64,
        owner: Pubkey,
        mint: Pubkey,
    ) -> &mut Self {
        let account = spl_token::state::Account {
            mint,
            owner,
            amount: tokens,
            delegate: COption::None,
            state: AccountState::Initialized,
            is_native: COption::None,
            delegated_amount: 0,
            close_authority: COption::None,
        };
        self.add_packable_rent_excempt(pubkey, account, spl_token::ID);
        self
    }

    pub fn add_associated_token_account(
        &mut self,
        owner: Pubkey,
        mint: Pubkey,
        amount: u64,
    ) -> &mut Self {
        self.add_token_account(
            get_associated_token_address(&owner, &mint),
            amount,
            owner,
            mint,
        )
    }

    pub fn add_flag_depot(&mut self, owner: Pubkey, amount: u64) -> &mut Self {
        self.add_associated_token_account(owner, flag_mint::ID, amount)
    }

    pub fn add_flag_mint(&mut self, supply: u64) -> &mut Self {
        self.add_mint(flag_mint::ID, supply, 0);
        self
    }

    pub fn add_flag_program(&mut self) -> &mut Self {
        self.add_native_program(flag_program::ID, "flagloader_program")
    }

    // ugly hack because the required function is private ._.
    pub fn init_and_exit(&self, mint_address: Pubkey) {
        self.genesis
            .start_with_mint_address(mint_address, SocketAddrSpace::Unspecified)
            .unwrap();
        process::exit(0);
    }
}
