use std::{path::PathBuf, str::FromStr};

use bank::{Bank, BankInstruction, UserAccount};
use bank_cli::{bank_program, flag_mint, GenesisSetup};
use borsh::{BorshDeserialize, BorshSerialize};
use clap::Clap;
use solana_client::{rpc_client::RpcClient, rpc_config::RpcSendTransactionConfig};
use solana_sdk::{
    commitment_config::CommitmentConfig,
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    signature::{read_keypair_file, Keypair},
    signer::Signer,
    system_instruction, system_program,
    sysvar::{clock, rent},
    transaction::Transaction,
};
use spl_associated_token_account::get_associated_token_address;

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
    Show,
    Withdraw(WithdrawArgs),
    Deposit(DepositArgs),
    GetFlag(GetFlagArgs),
}

/// Initialize the challenge
#[derive(Debug, Clap)]
struct SetupArgs {
    /// Keypair for the owner of the flag depot
    flag_depot: PathBuf,
    /// Keypair of the bank manager
    bank_manager: PathBuf,
}

#[derive(Clap, Debug)]
struct WithdrawArgs {
    /// Keypair identifying the bank account
    account_keypair: PathBuf,

    /// SPL token account to which the withdrawn tokens are transferred
    dest_pubkey: String,

    /// Amount to withdraw
    amount: u64,
}

#[derive(Clap, Debug)]
struct DepositArgs {
    /// Public key of the token account from which to transfer tokens into the bank
    src_token_pubkey: String,

    /// Public key identifying the user bank account
    /// The secret key for this public key is required to withdraw tokens from the bank account again
    account_pubkey: PathBuf,

    /// Amount to deposit
    amount: u64,

    /// Path to a keypair that is authorized to transfer tokens from the SPL account
    /// Defaults to the fee payer keypair.
    #[clap(short = 'a')]
    authority: Option<PathBuf>,
}

#[derive(Clap, Debug)]
pub struct GetFlagArgs {
    /// SPL token account holding flag tokens
    pub token_account: String,

    /// Path to a keypair that is authorized to transfer flag tokens from the SPL account
    /// Defaults to the fee payer keypair.
    #[clap(short = 'a', default_value = "~/.config/solana/id.json")]
    pub authority: String,
}

fn initialize_ledger() {
    const TOKEN_SUPPLY: u64 = 16;
    let flag_depot = read_keypair_file("keys/flag-depot.json").unwrap();
    let rich_boi = read_keypair_file("keys/rich-boi.json").unwrap();
    let bank_manager = read_keypair_file("keys/bank-manager.json").unwrap();

    GenesisSetup::new()
        .add_flag_mint(TOKEN_SUPPLY)
        .add_flag_depot(flag_depot.pubkey(), TOKEN_SUPPLY)
        .add_flag_program()
        .add_program(bank_program::ID, "bank")
        .add_account_with_sol(bank_manager.pubkey(), 100.0)
        .init_and_exit(rich_boi.pubkey());
}

fn setup(client: &RpcClient, fee_payer: Keypair, args: SetupArgs) {
    let flag_depot_owner = read_keypair_file(args.flag_depot).expect("read mint keypair");
    let flag_depot = get_associated_token_address(&flag_depot_owner.pubkey(), &flag_mint::ID);
    let manager = read_keypair_file(args.bank_manager).expect("read bank manager keypair");

    // initialize bank
    let (bank_address, _) = Pubkey::find_program_address(&[], &bank_program::ID);
    let (vault_address, _) =
        Pubkey::find_program_address(&[bank_address.as_ref()], &bank_program::ID);
    let (vault_authority_address, _) =
        Pubkey::find_program_address(&[vault_address.as_ref()], &bank_program::ID);

    let ix_transfer_fee_to_manager =
        system_instruction::transfer(&fee_payer.pubkey(), &manager.pubkey(), 100_000_000);
    let ix_init_bank = Instruction {
        program_id: bank_program::id(),
        data: bank::BankInstruction::Initialize { reserve_rate: 10 }
            .try_to_vec()
            .expect("serialize init bank ix"),
        accounts: vec![
            AccountMeta::new(bank_address, false),
            AccountMeta::new(manager.pubkey(), true),
            AccountMeta::new(vault_address, false),
            AccountMeta::new_readonly(vault_authority_address, false),
            AccountMeta::new_readonly(flag_mint::ID, false),
            AccountMeta::new_readonly(rent::ID, false),
            AccountMeta::new_readonly(system_program::ID, false),
            AccountMeta::new_readonly(spl_token::ID, false),
        ],
    };

    let tx = Transaction::new_signed_with_payer(
        &[ix_transfer_fee_to_manager, ix_init_bank],
        Some(&fee_payer.pubkey()),
        &vec![&fee_payer, &manager],
        client
            .get_recent_blockhash()
            .expect("get recent blockhash")
            .0,
    );
    client
        .send_and_confirm_transaction_with_spinner(&tx)
        .expect("send init tx");

    // deposit some funds into the bank
    let mut instructions = Vec::new();
    let mut signers = vec![];
    for i in 1..4 {
        let amount = ((i * 7 - 2) % 10) as u64;
        let keypair = Keypair::new();
        let (user_account, _) =
            Pubkey::find_program_address(&[&keypair.pubkey().to_bytes()], &bank_program::ID);
        instructions.push(system_instruction::transfer(
            &fee_payer.pubkey(),
            &keypair.pubkey(),
            100_000_000,
        ));
        instructions.push(Instruction {
            program_id: bank_program::ID,
            accounts: vec![
                AccountMeta::new(user_account, false),
                AccountMeta::new(keypair.pubkey(), true),
                AccountMeta::new_readonly(system_program::ID, false),
            ],
            data: BankInstruction::Open.try_to_vec().unwrap(),
        });
        instructions.push(Instruction {
            program_id: bank_program::ID,
            accounts: vec![
                AccountMeta::new(bank_address, false),
                AccountMeta::new(vault_address, false),
                AccountMeta::new(user_account, false),
                AccountMeta::new(flag_depot, false),
                AccountMeta::new_readonly(flag_depot_owner.pubkey(), true),
                AccountMeta::new_readonly(spl_token::ID, false),
                AccountMeta::new_readonly(clock::ID, false),
            ],
            data: BankInstruction::Deposit { amount }.try_to_vec().unwrap(),
        });
        signers.push(keypair);
    }
    let signers: Vec<_> = vec![&fee_payer, &flag_depot_owner]
        .into_iter()
        .chain(signers.iter())
        .collect();
    let tx = Transaction::new_signed_with_payer(
        &instructions,
        Some(&fee_payer.pubkey()),
        &signers,
        client
            .get_recent_blockhash()
            .expect("get recent blockhash")
            .0,
    );
    client
        .send_and_confirm_transaction_with_spinner(&tx)
        .expect("send deposit tx");

    println!("setup complete");
    println!("  bank pubkey: {}", bank_address);
    println!("  manager pubkey: {}", manager.pubkey());
    println!("  vault pubkey: {}", vault_address);
}

fn show(client: &RpcClient) {
    let (bank_address, _) = Pubkey::find_program_address(&[], &bank_program::ID);
    let accounts = client
        .get_program_accounts(&bank_program::id())
        .expect("get bank accounts");

    let (_, bank_account) = accounts
        .iter()
        .filter(|x| x.0 == bank_address)
        .next()
        .expect("have bank account");

    let bank = Bank::deserialize(&mut &bank_account.data[..]).expect("deserialize bank account");

    println!("bank info (pubkey {})", bank_address);
    println!("  reserve rate: {}%", bank.reserve_rate);
    println!("  total deposit: {}", bank.total_deposit);
    println!(
        "  manager key: {}",
        Pubkey::new_from_array(bank.manager_key)
    );

    for (pk, acc) in accounts.into_iter() {
        if pk == bank_address {
            continue;
        }

        let user = match UserAccount::deserialize(&mut &acc.data[..]) {
            Err(e) => {
                println!("user account {} cannot be deserialized: {}", pk, e);
                continue;
            }
            Ok(v) => v,
        };

        let naive_date = chrono::NaiveDateTime::from_timestamp(user.interest_paid_time, 0);
        println!(
            "user account {}: balance {}, annual interest rate {}%, interest last paid at {} UTC",
            pk, user.balance, user.interest_rate, naive_date
        );
    }
}

fn get_flag(client: &RpcClient, fee_payer: &Keypair, args: GetFlagArgs) {
    let account_pubkey = Pubkey::from_str(&args.token_account).expect("public key is valid");
    let authority_key =
        read_keypair_file(expand_path(&args.authority)).expect("read authority keypair");
    let ix = Instruction {
        program_id: flag_program::id(),
        accounts: vec![
            AccountMeta {
                pubkey: account_pubkey,
                is_signer: false,
                is_writable: false,
            },
            AccountMeta {
                pubkey: authority_key.pubkey(),
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
        &[fee_payer],
        blockhash,
    );
    client
        .send_and_confirm_transaction_with_spinner_and_config(
            &tx,
            CommitmentConfig::finalized(),
            RpcSendTransactionConfig {
                skip_preflight: true,
                ..Default::default()
            },
        )
        .expect("send flag tx");
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
        Cmd::Show => show(&client),
        Cmd::Withdraw(_) => todo!(),
        Cmd::Deposit(_) => todo!(),
        Cmd::GetFlag(args) => get_flag(&client, &fee_payer, args),
    }
}
