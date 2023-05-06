use setup::GenesisSetup;
use solana_sdk::{signature::read_keypair_file, signer::Signer};

fn main() {
    let rich_boi = read_keypair_file("keys/rich-boi.json").unwrap();

    GenesisSetup::new()
        .add_flag_mint(0)
        .add_flag_program()
        .init_and_exit(rich_boi.pubkey());
}
