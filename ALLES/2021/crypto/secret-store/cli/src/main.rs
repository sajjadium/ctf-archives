use std::{path::PathBuf, str::FromStr};

use borsh::BorshSerialize;
use clap::Clap;
use solana_client::{rpc_client::RpcClient, rpc_config::RpcSendTransactionConfig};
use solana_sdk::{
    commitment_config::CommitmentConfig,
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    signature::{read_keypair_file, Keypair},
    signer::Signer,
    system_program,
    sysvar::rent,
    transaction::Transaction,
};
use spl_associated_token_account::get_associated_token_address;
use store_cli::{flag_mint, store_program, GenesisSetup};

use solana_transaction_status::UiTransactionEncoding;

pub mod flag_program {
    use solana_sdk::declare_id;

    declare_id!("F1ag111111111111111111111111111111111111111");
}

#[derive(Debug, Clap)]
struct Opts {
    /// RPC URL of the solana cluster to connect to
    #[clap(short = 'u', long, default_value = "http://localhost:1024")]
    rpc_url: String,

    /// Keypair paying the transaction fees
    #[clap(short = 'k', long, default_value = "~/.config/solana/id.json")]
    fee_payer: String,

    #[clap(subcommand)]
    cmd: Cmd,
}

#[derive(Debug, Clap)]
enum Cmd {
    InitializeLedger,
    Setup(SetupArgs),
    GetFlag(GetFlagArgs),
}

/// Initialize the challenge
#[derive(Debug, Clap)]
struct SetupArgs {
    /// Keypair for the owner of the flag depot
    flag_depot: PathBuf,

    secret: u64,
}

// GetFlag
#[derive(Debug, Clap)]
struct GetFlagArgs {
    token_account: String,
    /// Keypair for the owner of the flag depot
    secret: u64,
    //token account
}

fn initialize_ledger() {
    const TOKEN_SUPPLY: u64 = 16;
    let flag_depot = read_keypair_file("keys/flag-depot.json").unwrap();
    let rich_boi = read_keypair_file("keys/rich-boi.json").unwrap();

    GenesisSetup::new()
        .add_flag_mint(TOKEN_SUPPLY)
        .add_flag_depot(flag_depot.pubkey(), TOKEN_SUPPLY)
        .add_flag_program()
        .add_program(store_program::ID, "store")
        .init_and_exit(rich_boi.pubkey());
}

fn setup(client: &RpcClient, fee_payer: Keypair, args: SetupArgs) {
    let flag_depot_owner = read_keypair_file(args.flag_depot).expect("read mint keypair");
    let flag_depot = get_associated_token_address(&flag_depot_owner.pubkey(), &flag_mint::ID);
    // initialize store
    let (store_address, _) = Pubkey::find_program_address(&[], &store_program::ID);

    let ix_init_store = Instruction {
        program_id: store_program::id(),
        data: store::StoreInstruction::Initialize {
            secret: args.secret,
        }
        .try_to_vec()
        .expect("serialize init store ix"),
        accounts: vec![
            AccountMeta::new(store_address, false),
            AccountMeta::new_readonly(fee_payer.pubkey(), true),
            AccountMeta::new(flag_depot, false),
            AccountMeta::new_readonly(flag_depot_owner.pubkey(), true),
            AccountMeta::new_readonly(rent::ID, false),
            AccountMeta::new_readonly(system_program::ID, false),
            AccountMeta::new_readonly(spl_token::ID, false),
        ],
    };

    let tx = Transaction::new_signed_with_payer(
        &[ix_init_store],
        Some(&fee_payer.pubkey()),
        &vec![&fee_payer, &flag_depot_owner],
        client
            .get_recent_blockhash()
            .expect("get recent blockhash")
            .0,
    );

    client
        .send_and_confirm_transaction_with_spinner(&tx)
        .expect("send init tx");

    println!("setup complete");
}

fn get_flag(client: &RpcClient, fee_payer: Keypair, args: GetFlagArgs) {
    let account_pubkey = Pubkey::from_str(&args.token_account).expect("public key is valid");
    let (store_address, _) = Pubkey::find_program_address(&[], &store_program::ID);

    let ix_init_store = Instruction {
        program_id: store_program::id(),
        data: store::StoreInstruction::GetFlag {
            secret: args.secret,
        }
        .try_to_vec()
        .expect("serialize init store ix"),
        accounts: vec![
            AccountMeta::new_readonly(store_address, false),
            AccountMeta::new(account_pubkey, false),
            AccountMeta::new_readonly(fee_payer.pubkey(), true),
            AccountMeta::new_readonly(spl_token::ID, false),
        ],
    };

    let tx = Transaction::new_signed_with_payer(
        &[ix_init_store],
        Some(&fee_payer.pubkey()),
        &vec![&fee_payer],
        client
            .get_recent_blockhash()
            .expect("get recent blockhash")
            .0,
    );

    client
        .send_and_confirm_transaction_with_spinner(&tx)
        .expect("send init tx");

    let ix = Instruction {
        program_id: flag_program::id(),
        accounts: vec![
            AccountMeta {
                pubkey: account_pubkey,
                is_signer: false,
                is_writable: false,
            },
            AccountMeta {
                pubkey: fee_payer.pubkey(),
                is_signer: true,
                is_writable: false,
            },
        ],
        data: Vec::new(),
    };
    let blockhash = client.get_recent_blockhash().expect("get blockhash").0;
    let tx = Transaction::new_signed_with_payer(
        &[ix],
        Some(&fee_payer.pubkey()),
        &[&fee_payer],
        blockhash,
    );
    let sig = client
        .send_and_confirm_transaction_with_spinner_and_config(
            &tx,
            CommitmentConfig::finalized(),
            RpcSendTransactionConfig {
                skip_preflight: true,
                ..Default::default()
            },
        )
        .expect("send flag tx");

    let tt = client
        .get_transaction(&sig, UiTransactionEncoding::Json)
        .unwrap();
    dbg!(tt.transaction.meta.unwrap().log_messages);
}

/// Simple function to replace ~ by homedir (hacky)
fn expand_path(path: &str) -> PathBuf {
    #[allow(deprecated)]
    PathBuf::from(path.replace("~", &std::env::home_dir().unwrap().to_string_lossy()))
}

fn main() {
    let opts: Opts = Opts::parse();
    let fee_payer =
        read_keypair_file(expand_path(&opts.fee_payer)).expect("read fee payer keypair");
    let client = RpcClient::new(opts.rpc_url);

    match opts.cmd {
        Cmd::InitializeLedger => initialize_ledger(),
        Cmd::Setup(args) => setup(&client, fee_payer, args),
        Cmd::GetFlag(args) => get_flag(&client, fee_payer, args),
    }
}
